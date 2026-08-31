from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, func, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Any, Optional

from app.core.constants import SHORT_TEXT_MAX_LENGTH
from app.db.base_class import Base
from app.models.Mixins import PKMixin

if TYPE_CHECKING:
    from app.models.user import User

class AuditLog(Base, PKMixin):

    __tablename__ = "audit_logs"

    __table_args__ = (
        Index("ix_audit_logs_user_id", "user_id"),
        Index("ix_audit_logs_entity_type", "entity_type"),
    )

    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id",  ondelete="SET NULL"),
        nullable=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(SHORT_TEXT_MAX_LENGTH),
        nullable=False,
    )

    entity_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(SHORT_TEXT_MAX_LENGTH),
        nullable=False,
    )

    old_value: Mapped[Any | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    new_value: Mapped[Any | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped[Optional["User"]] = relationship(back_populates="audit_logs")

