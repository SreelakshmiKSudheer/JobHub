from decimal import Decimal

from sqlalchemy import DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from app.db.base_class import Base
from app.models.Mixins import CreatedAtMixin, PKMixin, SoftDeleteMixin, UpdatedAtMixin
from app.db.types import ShortTextType, LongTextType, EmployeeCodeType    
from app.models.enums import EmploymentType, SkillLevel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.designation import Designation
    from app.models.user import User


class JobTemplate(Base, PKMixin, CreatedAtMixin, UpdatedAtMixin, SoftDeleteMixin):
    __tablename__ = "job_templates"


    name: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False,
        unique=True
    )
    
    title: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        LongTextType,
        nullable=True,
        default=None
    )
    
    designation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="RESTRICT"),
        nullable=False,
    )
    
    employment_type: Mapped[EmploymentType | None] = mapped_column(
        Enum(EmploymentType, name="employment_type", native_enum=True),
        nullable=True,
        default=None
    )
    
    experience_years: Mapped[Decimal | None] = mapped_column(
        DECIMAL(2, 2),
        nullable=True,
        default=None
    )
    
    skills: Mapped[list[dict[UUID, SkillLevel]] | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None
    )
    
    salary: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
        default=None
    )
    
    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # --- relationships ---
    designation: Mapped["Designation"] = relationship(
        back_populates="job_templates",
        foreign_keys=[designation_id],
    )
    created_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="job_templates",
        foreign_keys=[created_by],
    )
    
    