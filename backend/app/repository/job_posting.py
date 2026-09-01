from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session

from app.core.skills_utils import merge_skills
from app.models.enums import JobPostingStatus
from app.models.job_posting import JobPosting
from app.schemas.job_posting import JobPostingCreate, JobPostingUpdate


def get_job_posting_by_id(db: Session, job_posting_id: UUID) -> JobPosting | None:
    return db.query(JobPosting).filter(JobPosting.id == job_posting_id, JobPosting.deleted_at.is_(None)).one_or_none()


def get_job_postings(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    q: Optional[str] = None,
    department_id: Optional[UUID] = None,
    designation_id: Optional[UUID] = None,
    skill_id: Optional[UUID] = None,
    due_before: Optional[datetime] = None,
    status: Optional[JobPostingStatus] = None,
    statuses: Optional[list[JobPostingStatus]] = None,
    only_open_active: bool = False,
    sort_by: Optional[str] = "deadline_asc",
) -> tuple[list[JobPosting], int]:
    query = db.query(JobPosting).filter(JobPosting.deleted_at.is_(None))

    now = datetime.now(timezone.utc)
    if only_open_active:
        query = query.filter(JobPosting.status == JobPostingStatus.OPEN, JobPosting.deadline >= now)
    elif status:
        query = query.filter(JobPosting.status == status)
    elif statuses:
        query = query.filter(JobPosting.status.in_(statuses))

    if q:
        search_pattern = f"%{q}%"
        query = query.filter(JobPosting.title.ilike(search_pattern))

    if department_id:
        query = query.filter(JobPosting.department_id == department_id)

    if designation_id:
        query = query.filter(JobPosting.designation_id == designation_id)

    if due_before:
        query = query.filter(JobPosting.deadline <= due_before)

    if skill_id:
        # Postgres JSONB containment search for skill UUID key
        skill_str = str(skill_id)
        query = query.filter(
            func.jsonb_path_exists(JobPosting.skills, f'$[*] ? (exists (@."{skill_str}"))')
        )

    total = query.count()

    # Sorting
    if sort_by == "deadline_desc":
        query = query.order_by(JobPosting.deadline.desc())
    elif sort_by == "created_at_desc":
        query = query.order_by(JobPosting.created_at.desc())
    else:  # default deadline_asc
        query = query.order_by(JobPosting.deadline.asc())

    postings = query.offset(skip).limit(limit).all()
    return postings, total


def create_job_posting(db: Session, payload: JobPostingCreate, created_by: UUID) -> JobPosting:
    formatted_skills = [
        {str(key): str(val) if not isinstance(val, int) else val for key, val in skill_dict.items()}
        for skill_dict in payload.skills
    ]

    deadline_reminder = payload.deadline_reminder_at
    if deadline_reminder is None and payload.deadline is not None:
        from datetime import timedelta
        deadline_reminder = payload.deadline - timedelta(days=1)

    posting = JobPosting(
        title=payload.title,
        description=payload.description,
        department_id=payload.department_id,
        designation_id=payload.designation_id,
        location=payload.location,
        employment_type=payload.employment_type,
        experience_years=payload.experience_years,
        skills=formatted_skills,
        salary=payload.salary,
        deadline=payload.deadline,
        deadline_reminder_at=deadline_reminder,
        status=payload.status,
        created_by=created_by,
    )

    db.add(posting)
    db.commit()
    db.refresh(posting)
    return posting


def update_job_posting(db: Session, posting: JobPosting, payload: JobPostingUpdate) -> JobPosting:
    update_data = payload.model_dump(exclude_unset=True)

    if "skills" in update_data:
        new_skills = update_data["skills"]
        update_data["skills"] = merge_skills(posting.skills, new_skills)

    for key, value in update_data.items():
        setattr(posting, key, value)

    db.commit()
    db.refresh(posting)
    return posting


def soft_delete_job_posting(db: Session, posting: JobPosting) -> None:
    posting.deleted_at = datetime.now(timezone.utc)
    db.add(posting)
    db.commit()