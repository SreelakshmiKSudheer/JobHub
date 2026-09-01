from datetime import datetime, timezone
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import ApplicationStatus, JobPostingStatus, NotificationType, UserRole
from app.models.job_posting import JobPosting
from app.models.user import User
from app.repository.job_posting import (
    create_job_posting,
    get_job_posting_by_id,
    get_job_postings,
    soft_delete_job_posting,
    update_job_posting,
)

from app.repository.job_template import get_job_template_by_id
from app.schemas.job_posting import JobPostingCreate, JobPostingUpdate
from app.services.audit_log import AuditLogService
from app.services.notification import NotificationService


class JobPostingService:

    @staticmethod
    def create_job_posting(db: Session, payload: JobPostingCreate, current_user: User, template_id: Optional[UUID] = None) -> JobPosting:
        # Template pre-population if requested
        if template_id:
            template = get_job_template_by_id(db, template_id)
            if template:
                if not payload.title:
                    payload.title = template.title
                if not payload.description:
                    payload.description = template.description
                if not payload.designation_id:
                    payload.designation_id = template.designation_id
                if not payload.employment_type and template.employment_type:
                    payload.employment_type = template.employment_type
                if not payload.experience_years and template.experience_years:
                    payload.experience_years = template.experience_years
                if not payload.skills and template.skills:
                    payload.skills = template.skills
                if not payload.salary and template.salary:
                    payload.salary = template.salary

        # Business Rule: Open posting must have a valid deadline
        now = datetime.now(timezone.utc)
        if payload.status == JobPostingStatus.OPEN:
            if not payload.deadline:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="A deadline is mandatory for open job postings",
                )
            if payload.deadline <= now:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Deadline must be in the future for open job postings",
                )

        posting = create_job_posting(db=db, payload=payload, created_by=current_user.id)

        # Audit Log
        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="job_posting",
            entity_id=posting.id,
            action="CREATE_JOB_POSTING",
            new_value={"title": posting.title, "status": posting.status.value},
        )
        return posting

    @staticmethod
    def get_job_postings(
        db: Session,
        current_user: User,
        page: int = 1,
        page_size: int = 20,
        q: Optional[str] = None,
        department_id: Optional[UUID] = None,
        designation_id: Optional[UUID] = None,
        skill_id: Optional[UUID] = None,
        due_before: Optional[datetime] = None,
        status_filter: Optional[JobPostingStatus] = None,
        sort_by: Optional[str] = "deadline_asc",
    ) -> tuple[list[JobPosting], int]:
        skip = (page - 1) * page_size

        # Trigger auto-closure check for expired deadlines
        JobPostingService.auto_close_expired_postings(db)

        # Employee role can only discover OPEN postings with deadline >= now
        only_open = current_user.role == UserRole.USER

        items, total = get_job_postings(
            db=db,
            skip=skip,
            limit=page_size,
            q=q,
            department_id=department_id,
            designation_id=designation_id,
            skill_id=skill_id,
            due_before=due_before,
            status=status_filter,
            only_open_active=only_open,
            sort_by=sort_by,
        )

        return items, total

    @staticmethod
    def get_job_posting_by_id(db: Session, job_posting_id: UUID, current_user: User) -> JobPosting:
        posting = get_job_posting_by_id(db, job_posting_id)
        if not posting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        # Employee cannot view draft postings
        if current_user.role == UserRole.USER and posting.status == JobPostingStatus.DRAFT:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        return posting

    @staticmethod
    def update_job_posting(
        db: Session, job_posting_id: UUID, payload: JobPostingUpdate, current_user: User
    ) -> JobPosting:
        posting = get_job_posting_by_id(db, job_posting_id)
        if not posting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        old_status = posting.status
        old_value = {"status": old_status.value, "title": posting.title}

        # Check status transition rules
        now = datetime.now(timezone.utc)
        if payload.status is not None:
            new_status = payload.status

            # Reopening or opening requires valid deadline
            if new_status == JobPostingStatus.OPEN:
                target_deadline = payload.deadline or posting.deadline
                if not target_deadline or target_deadline <= now:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot open or reopen posting without a valid future deadline",
                    )

            # Completing requires all associated applications to be in terminal states
            if new_status == JobPostingStatus.COMPLETED:
                active_apps = [
                    app for app in posting.applications
                    if app.status not in (ApplicationStatus.SELECTED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN)
                ]
                if active_apps:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot mark posting as COMPLETED while active applications exist. All applications must be in terminal state (SELECTED, REJECTED, WITHDRAWN).",
                    )

        updated = update_job_posting(db=db, posting=posting, payload=payload)

        # Audit Log
        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="job_posting",
            entity_id=updated.id,
            action="UPDATE_JOB_POSTING",
            old_value=old_value,
            new_value={"status": updated.status.value, "title": updated.title},
        )
        return updated

    @staticmethod
    def delete_job_posting(db: Session, job_posting_id: UUID, current_user: User) -> None:
        posting = get_job_posting_by_id(db, job_posting_id)
        if not posting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        # Business Rule: TA can only delete DRAFT postings
        if posting.status != JobPostingStatus.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only draft job postings can be deleted",
            )

        soft_delete_job_posting(db, posting)

        AuditLogService.log_action(
            db=db,
            user_id=current_user.id,
            entity_type="job_posting",
            entity_id=posting.id,
            action="DELETE_JOB_POSTING",
            old_value={"title": posting.title, "status": posting.status.value},
        )

    @staticmethod
    def auto_close_expired_postings(db: Session) -> None:
        now = datetime.now(timezone.utc)
        expired_postings = (
            db.query(JobPosting)
            .filter(
                JobPosting.deleted_at.is_(None),
                JobPosting.status == JobPostingStatus.OPEN,
                JobPosting.deadline < now,
            )
            .all()
        )

        for posting in expired_postings:
            posting.status = JobPostingStatus.CLOSED
            db.commit()

            # Audit Log
            AuditLogService.log_action(
                db=db,
                user_id=posting.created_by,
                entity_type="job_posting",
                entity_id=posting.id,
                action="AUTO_CLOSE_JOB_POSTING",
                old_value={"status": JobPostingStatus.OPEN.value},
                new_value={"status": JobPostingStatus.CLOSED.value},
            )

            # Notification to TA creator
            if posting.created_by:
                NotificationService.send_notification(
                    db=db,
                    recipient_id=posting.created_by,
                    notification_type=NotificationType.JOB_POSTING_CLOSED,
                    title="Job Posting Closed",
                    message=f"The job posting '{posting.title}' has automatically closed as its deadline passed.",
                    job_posting_id=posting.id,
                )