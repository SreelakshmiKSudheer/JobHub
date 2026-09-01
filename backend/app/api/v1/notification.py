import math
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.notification import NotificationResponse
from app.schemas.response import APIResponse
from app.services.notification import NotificationService

notification_router = APIRouter(prefix="/notifications", tags=["Notifications"])


@notification_router.get("", response_model=APIResponse[dict], dependencies=[Depends(get_current_user)])
def get_notifications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    items, total = NotificationService.get_user_notifications(
        db=db, user_id=current_user.id, skip=skip, limit=page_size
    )

    items_data = [NotificationResponse.model_validate(item).model_dump(mode="json") for item in items]
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Notifications retrieved successfully",
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


@notification_router.patch(
    "/{notification_id}/read",
    response_model=APIResponse[NotificationResponse],
    dependencies=[Depends(get_current_user)],
)
def mark_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = NotificationService.mark_as_read(db, notification_id=notification_id, user_id=current_user.id)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Notification marked as read",
        data=data,
        error=None,
    )


@notification_router.post(
    "/read-all",
    response_model=APIResponse[dict],
    dependencies=[Depends(get_current_user)],
)
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = NotificationService.mark_all_as_read(db, user_id=current_user.id)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="All notifications marked as read",
        data={"updated_count": count},
        error=None,
    )
