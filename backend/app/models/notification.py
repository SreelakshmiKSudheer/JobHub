
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime
from datetime import datetime

import uuid
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base_class import Base
from app.models.Mixins import CreatedAtMixin, PKMixin, UpdatedAtMixin
from app.db.types import ShortTextType, LongTextType, EmployeeCodeType    
from app.models.enums import  NotificationType

if TYPE_CHECKING:
    from app.models.job_posting import JobPosting
    from app.models.user import User
    from app.models.application import Application


class Notification(Base, PKMixin, CreatedAtMixin):
    __tablename__ = "notifications"
    
    recipient_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type", native_enum=True),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False,
    )
    
    message: Mapped[str] = mapped_column(
        LongTextType,
        nullable=False,
    )
    
    application_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=True,
    )
    
    job_posting_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=True,
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )
    
    # --- relationships ---
    recipient: Mapped["User"] = relationship(
        back_populates="notifications",
        foreign_keys=[recipient_id],
    )
    application: Mapped[Optional["Application"]] = relationship(
        back_populates="notifications",
        foreign_keys=[application_id],
    )
    job_posting: Mapped[Optional["JobPosting"]] = relationship(
        back_populates="notifications",
        foreign_keys=[job_posting_id],
    )
    
    