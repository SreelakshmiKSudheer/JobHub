import math
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.models.enums import JobPostingStatus
from app.models.user import User
from app.schemas.job_posting import JobPostingCreate, JobPostingResponse, JobPostingUpdate
from app.schemas.response import APIResponse
from app.services.job_posting import JobPostingService

job_posting_router = APIRouter(prefix="/job-postings", tags=["Job Postings"])


@job_posting_router.get("", response_model=APIResponse[dict], dependencies=[Depends(get_current_user)])
def get_job_postings(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    q: Optional[str] = Query(default=None),
    department_id: Optional[UUID] = Query(default=None),
    designation_id: Optional[UUID] = Query(default=None),
    skill_id: Optional[UUID] = Query(default=None),
    due_before: Optional[datetime] = Query(default=None),
    status_filter: Optional[JobPostingStatus] = Query(default=None, alias="status"),
    sort_by: Optional[str] = Query(default="deadline_asc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = JobPostingService.get_job_postings(
        db=db,
        current_user=current_user,
        page=page,
        page_size=page_size,
        q=q,
        department_id=department_id,
        designation_id=designation_id,
        skill_id=skill_id,
        due_before=due_before,
        status_filter=status_filter,
        sort_by=sort_by,
    )

    items_data = [JobPostingResponse.model_validate(item).model_dump(mode="json") for item in items]
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job postings retrieved successfully",
        data={
            "data": items_data,
            "meta": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": total_pages,
            },
        },
        error=None,
    )


@job_posting_router.get("/{job_posting_id}", response_model=APIResponse[JobPostingResponse], dependencies=[Depends(get_current_user)])
def get_job_posting(
    job_posting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = JobPostingService.get_job_posting_by_id(db, job_posting_id, current_user=current_user)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job posting retrieved successfully",
        data=data,
        error=None,
    )


@job_posting_router.post("", response_model=APIResponse[JobPostingResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_job_posting(
    payload: JobPostingCreate,
    template_id: Optional[UUID] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    data = JobPostingService.create_job_posting(db, payload=payload, current_user=current_user, template_id=template_id)
    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="Job posting created successfully",
        data=data,
        error=None,
    )


@job_posting_router.put("/{job_posting_id}", response_model=APIResponse[JobPostingResponse], dependencies=[Depends(require_admin)])
def update_job_posting(
    job_posting_id: UUID,
    payload: JobPostingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    data = JobPostingService.update_job_posting(db, job_posting_id=job_posting_id, payload=payload, current_user=current_user)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job posting updated successfully",
        data=data,
        error=None,
    )


@job_posting_router.delete("/{job_posting_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_job_posting(
    job_posting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    JobPostingService.delete_job_posting(db, job_posting_id=job_posting_id, current_user=current_user)
    return None