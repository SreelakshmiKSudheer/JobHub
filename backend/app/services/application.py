from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.enums import ApplicationStatus, JobPostingStatus, NotificationType, UserRole
from app.models.user import User
from app.repository.application import (
    count_withdrawn_applications_for_employee,
    create_application,
    get_active_application_for_employee,
    get_application_by_id,
    get_applications_by_employee,
    get_applications_by_job_posting,
    update_application_status,
)
from app.repository.employee import get_employee_by_user_id
from app.repository.job_posting import get_job_posting_by_id
from app.services.audit_log import AuditLogService
from app.services.notification import NotificationService

ALLOWED_TRANSITIONS: dict[ApplicationStatus, list[ApplicationStatus]] = {
    ApplicationStatus.APPLIED: [ApplicationStatus.UNDER_REVIEW, ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED],
    ApplicationStatus.UNDER_REVIEW: [ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED],
    ApplicationStatus.SHORTLISTED: [ApplicationStatus.UNDER_REVIEW, ApplicationStatus.INTERVIEWED, ApplicationStatus.REJECTED],
    ApplicationStatus.INTERVIEWED: [ApplicationStatus.SELECTED, ApplicationStatus.REJECTED],
    ApplicationStatus.SELECTED: [],
    ApplicationStatus.REJECTED: [],
    ApplicationStatus.WITHDRAWN: [],
}

ALLOWED_WITHDRAWAL_STATUSES: set[ApplicationStatus] = {
    ApplicationStatus.APPLIED,
    ApplicationStatus.UNDER_REVIEW,
    ApplicationStatus.SHORTLISTED,
}


class ApplicationService:

    @staticmethod
    def apply_to_job(db: Session, job_posting_id: UUID, current_user: User) -> Application:
        employee = get_employee_by_user_id(db, current_user.id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only registered employees can submit applications")

        posting = get_job_posting_by_id(db, job_posting_id)
        if not posting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        # Business Rule: Job posting must be OPEN
        if posting.status != JobPostingStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot apply to a job posting with status '{posting.status.value}'",
            )

        # Business Rule: Job posting deadline must not have passed
        now = datetime.now(timezone.utc)
        if posting.deadline < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application deadline for this job posting has passed",
            )

        # Business Rule: Duplicate active application check
        active_app = get_active_application_for_employee(db, employee_id=employee.id, job_posting_id=job_posting_id)
        if active_app:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already have an active application for this job posting",
            )

        # Business Rule: Reapplication limit (max 2 reapplications after withdrawal)
        withdrawn_count = count_withdrawn_applications_for_employee(db, employee_id=employee.id, job_posting_id=job_posting_id)
        if withdrawn_count >= 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum reapplication limit (2 reapplications) reached for this job posting",
            )

        application = create_application(db, employee_id=employee.id, job_posting_id=job_posting_id)

        # Audit Log
        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="application",
            entity_id=application.id,
            action="SUBMIT_APPLICATION",
            new_value={"job_posting_id": str(job_posting_id), "status": application.status.value},
        )

        return application

    @staticmethod
    def withdraw_application(db: Session, application_id: UUID, current_user: User) -> Application:
        application = get_application_by_id(db, application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        # Employee authorization: can only withdraw own application
        if current_user.role == UserRole.USER and application.employee_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        # Business Rule: Can only withdraw if in APPLIED, UNDER_REVIEW, SHORTLISTED
        if application.status not in ALLOWED_WITHDRAWAL_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot withdraw an application in status '{application.status.value}'",
            )

        old_status = application.status.value
        updated_app = update_application_status(db, application=application, new_status=ApplicationStatus.WITHDRAWN)

        # Audit Log
        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="application",
            entity_id=updated_app.id,
            action="WITHDRAW_APPLICATION",
            old_value={"status": old_status},
            new_value={"status": ApplicationStatus.WITHDRAWN.value},
        )

        return updated_app

    @staticmethod
    def update_status(
        db: Session, application_id: UUID, new_status: ApplicationStatus, current_user: User
    ) -> Application:
        application = get_application_by_id(db, application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        current_status = application.status

        # Business Rule: Validate state machine transition
        valid_next_states = ALLOWED_TRANSITIONS.get(current_status, [])
        if new_status not in valid_next_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from '{current_status.value}' to '{new_status.value}'",
            )

        updated_app = update_application_status(db, application=application, new_status=new_status)

        # Audit Log
        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="application",
            entity_id=updated_app.id,
            action="UPDATE_APPLICATION_STATUS",
            old_value={"status": current_status.value},
            new_value={"status": new_status.value},
        )

        # Employee notification triggers
        job_title = application.job_posting.title if application.job_posting else "job posting"
        employee_user_id = application.employee_id  # Employee table primary key maps to user.id

        notif_map = {
            ApplicationStatus.SHORTLISTED: (
                NotificationType.APPLICATION_SHORTLISTED,
                "Application Shortlisted",
                f"Your application for '{job_title}' has been shortlisted!",
            ),
            ApplicationStatus.INTERVIEWED: (
                NotificationType.APPLICATION_SHORTLISTED,
                "Application Moving to Interview",
                f"Your application for '{job_title}' has progressed to the interview stage.",
            ),
            ApplicationStatus.SELECTED: (
                NotificationType.APPLICATION_SELECTED,
                "Application Selected!",
                f"Congratulations! Your application for '{job_title}' has been selected.",
            ),
            ApplicationStatus.REJECTED: (
                NotificationType.APPLICATION_REJECTED,
                "Application Status Update",
                f"Your application for '{job_title}' has been rejected.",
            ),
        }

        if new_status in notif_map:
            notif_type, title, msg = notif_map[new_status]
            NotificationService.send_notification(
                db=db,
                recipient_id=employee_user_id,
                notification_type=notif_type,
                title=title,
                message=msg,
                application_id=updated_app.id,
                job_posting_id=updated_app.job_posting_id,
            )

        return updated_app

    @staticmethod
    def get_my_applications(
        db: Session, current_user: User, page: int = 1, page_size: int = 20
    ) -> tuple[list[Application], int]:
        skip = (page - 1) * page_size
        return get_applications_by_employee(db=db, employee_id=current_user.id, skip=skip, limit=page_size)

    @staticmethod
    def get_job_applications(
        db: Session, job_posting_id: UUID, page: int = 1, page_size: int = 20, status_filter: ApplicationStatus | None = None
    ) -> tuple[list[Application], int]:
        skip = (page - 1) * page_size
        return get_applications_by_job_posting(
            db=db, job_posting_id=job_posting_id, skip=skip, limit=page_size, status_filter=status_filter
        )

    @staticmethod
    def get_application_by_id(db: Session, application_id: UUID, current_user: User) -> Application:
        application = get_application_by_id(db, application_id)
        if not application:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

        # Employee authorization: can only view own application
        if current_user.role == UserRole.USER and application.employee_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return application
