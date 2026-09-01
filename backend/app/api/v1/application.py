import math
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, require_admin, require_role_user
from app.db.session import get_db
from app.models.enums import ApplicationStatus
from app.models.user import User
from app.schemas.application import ApplicationResponse, ApplicationUpdate
from app.schemas.response import APIResponse
from app.services.application import ALLOWED_WITHDRAWAL_STATUSES, ApplicationService

application_router = APIRouter(tags=["Applications"])


def serialize_application(app) -> dict:
    data = ApplicationResponse.model_validate(app).model_dump(mode="json")
    data["withdraw_allowed"] = app.status in ALLOWED_WITHDRAWAL_STATUSES
    return data


@application_router.post(
    "/job-postings/{job_posting_id}/apply",
    response_model=APIResponse[dict],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role_user)],
)
def apply_to_job(
    job_posting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role_user),
):
    app = ApplicationService.apply_to_job(db, job_posting_id=job_posting_id, current_user=current_user)
    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="Application submitted successfully",
        data=serialize_application(app),
        error=None,
    )


@application_router.get(
    "/applications/my-applications",
    response_model=APIResponse[dict],
    dependencies=[Depends(get_current_user)],
)
def get_my_applications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items, total = ApplicationService.get_my_applications(
        db=db, current_user=current_user, page=page, page_size=page_size
    )

    items_data = [serialize_application(item) for item in items]
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="My applications retrieved successfully",
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


@application_router.get(
    "/job-postings/{job_posting_id}/applications",
    response_model=APIResponse[dict],
    dependencies=[Depends(require_admin)],
)
def get_job_applications(
    job_posting_id: UUID,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status_filter: Optional[ApplicationStatus] = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    items, total = ApplicationService.get_job_applications(
        db=db, job_posting_id=job_posting_id, page=page, page_size=page_size, status_filter=status_filter
    )

    items_data = [serialize_application(item) for item in items]
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job applications retrieved successfully",
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


@application_router.get(
    "/applications/{application_id}",
    response_model=APIResponse[dict],
    dependencies=[Depends(get_current_user)],
)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = ApplicationService.get_application_by_id(db, application_id=application_id, current_user=current_user)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Application retrieved successfully",
        data=serialize_application(app),
        error=None,
    )


@application_router.post(
    "/applications/{application_id}/withdraw",
    response_model=APIResponse[dict],
    dependencies=[Depends(get_current_user)],
)
def withdraw_application(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = ApplicationService.withdraw_application(db, application_id=application_id, current_user=current_user)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Application withdrawn successfully",
        data=serialize_application(app),
        error=None,
    )


@application_router.patch(
    "/applications/{application_id}/status",
    response_model=APIResponse[dict],
    dependencies=[Depends(require_admin)],
)
def update_application_status(
    application_id: UUID,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    app = ApplicationService.update_status(
        db, application_id=application_id, new_status=payload.status, current_user=current_user
    )
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message=f"Application status updated to {payload.status.value}",
        data=serialize_application(app),
        error=None,
    )
