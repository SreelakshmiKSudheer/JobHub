from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from app.models.application import Application
from app.models.enums import ApplicationStatus


def get_application_by_id(db: Session, application_id: UUID) -> Application | None:
    return (
        db.query(Application)
        .options(joinedload(Application.job_posting), joinedload(Application.employee))
        .filter(Application.id == application_id)
        .one_or_none()
    )


def get_active_application_for_employee(db: Session, employee_id: UUID, job_posting_id: UUID) -> Application | None:
    return (
        db.query(Application)
        .filter(
            Application.employee_id == employee_id,
            Application.job_posting_id == job_posting_id,
            Application.status.not_in([ApplicationStatus.WITHDRAWN, ApplicationStatus.REJECTED]),
        )
        .first()
    )


def count_withdrawn_applications_for_employee(db: Session, employee_id: UUID, job_posting_id: UUID) -> int:
    return (
        db.query(Application)
        .filter(
            Application.employee_id == employee_id,
            Application.job_posting_id == job_posting_id,
            Application.status == ApplicationStatus.WITHDRAWN,
        )
        .count()
    )


def create_application(db: Session, employee_id: UUID, job_posting_id: UUID) -> Application:
    application = Application(
        employee_id=employee_id,
        job_posting_id=job_posting_id,
        status=ApplicationStatus.APPLIED,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def get_applications_by_employee(
    db: Session, employee_id: UUID, skip: int = 0, limit: int = 50
) -> tuple[list[Application], int]:
    query = (
        db.query(Application)
        .options(joinedload(Application.job_posting))
        .filter(Application.employee_id == employee_id)
    )
    total = query.count()
    apps = query.order_by(Application.created_at.desc()).offset(skip).limit(limit).all()
    return apps, total


def get_applications_by_job_posting(
    db: Session, job_posting_id: UUID, skip: int = 0, limit: int = 50, status_filter: ApplicationStatus | None = None
) -> tuple[list[Application], int]:
    query = (
        db.query(Application)
        .options(joinedload(Application.employee), joinedload(Application.job_posting))
        .filter(Application.job_posting_id == job_posting_id)
    )
    if status_filter:
        query = query.filter(Application.status == status_filter)

    total = query.count()
    apps = query.order_by(Application.created_at.desc()).offset(skip).limit(limit).all()
    return apps, total


def update_application_status(db: Session, application: Application, new_status: ApplicationStatus) -> Application:
    application.status = new_status
    db.commit()
    db.refresh(application)
    return application
