from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import NotificationType
from app.models.notification import Notification
from app.repository.notification import (
    create_notification,
    get_notification_by_id,
    get_user_notifications,
    mark_all_notifications_as_read,
    mark_notification_as_read,
)


class NotificationService:

    @staticmethod
    def send_notification(
        db: Session,
        recipient_id: UUID,
        notification_type: NotificationType,
        title: str,
        message: str,
        application_id: UUID | None = None,
        job_posting_id: UUID | None = None,
    ) -> Notification:
        return create_notification(
            db=db,
            recipient_id=recipient_id,
            notification_type=notification_type,
            title=title,
            message=message,
            application_id=application_id,
            job_posting_id=job_posting_id,
        )

    @staticmethod
    def get_user_notifications(
        db: Session, user_id: UUID, skip: int = 0, limit: int = 50
    ) -> tuple[list[Notification], int]:
        return get_user_notifications(db=db, user_id=user_id, skip=skip, limit=limit)

    @staticmethod
    def mark_as_read(db: Session, notification_id: UUID, user_id: UUID) -> Notification:
        notification = get_notification_by_id(db, notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notification.recipient_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return mark_notification_as_read(db, notification)

    @staticmethod
    def mark_all_as_read(db: Session, user_id: UUID) -> int:
        return mark_all_notifications_as_read(db, user_id)
