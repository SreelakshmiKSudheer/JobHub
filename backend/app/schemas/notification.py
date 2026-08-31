from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import NotificationType
from backend.app.core.constants import LONG_TEXT_MAX_LENGTH, SHORT_TEXT_MAX_LENGTH


class NotificationBase(BaseModel):
    recipient_id: UUID
    notification_type: NotificationType
    title: str = Field(..., description="The title of the notification", max_length=SHORT_TEXT_MAX_LENGTH)
    message: str = Field(..., description="The message of the notification", max_length=LONG_TEXT_MAX_LENGTH)
    application_id: UUID | None = None
    job_posting_id: UUID | None = None


class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    read_at: datetime | None = Field(default=None, description="The time when the notification was read")

class NotificationResponse(NotificationBase):
    id: UUID = Field(..., description="The unique identifier of the notification")
    created_at: datetime
    read_at: datetime | None = Field(default=None, description="The time when the notification was read")

    model_config = ConfigDict(from_attributes=True)