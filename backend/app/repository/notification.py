from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.enums import NotificationType
from app.models.notification import Notification


def create_notification(
    db: Session,
    recipient_id: UUID,
    notification_type: NotificationType,
    title: str,
    message: str,
    application_id: UUID | None = None,
    job_posting_id: UUID | None = None,
) -> Notification:
    notification = Notification(
        recipient_id=recipient_id,
        notification_type=notification_type,
        title=title,
        message=message,
        application_id=application_id,
        job_posting_id=job_posting_id,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_user_notifications(db: Session, user_id: UUID, skip: int = 0, limit: int = 50) -> tuple[list[Notification], int]:
    query = db.query(Notification).filter(Notification.recipient_id == user_id)
    total = query.count()
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications, total


def get_notification_by_id(db: Session, notification_id: UUID) -> Notification | None:
    return db.query(Notification).filter(Notification.id == notification_id).one_or_none()


def mark_notification_as_read(db: Session, notification: Notification) -> Notification:
    if notification.read_at is None:
        notification.read_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(notification)
    return notification


def mark_all_notifications_as_read(db: Session, user_id: UUID) -> int:
    now = datetime.now(timezone.utc)
    updated_count = (
        db.query(Notification)
        .filter(Notification.recipient_id == user_id, Notification.read_at.is_(None))
        .update({Notification.read_at: now}, synchronize_session=False)
    )
    db.commit()
    return updated_count
