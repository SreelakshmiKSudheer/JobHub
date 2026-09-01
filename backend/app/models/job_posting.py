from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from datetime import datetime
from app.db.base_class import Base
from app.models.Mixins import CreatedAtMixin, PKMixin, SoftDeleteMixin, UpdatedAtMixin
from app.db.types import ShortTextType, LongTextType, EmployeeCodeType    
from app.models.enums import EmploymentType, JobPostingStatus, SkillLevel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.notification import Notification
    from app.models.department import Department
    from app.models.designation import Designation
    from app.models.user import User
    from app.models.application import Application


class JobPosting(Base, PKMixin, CreatedAtMixin, UpdatedAtMixin, SoftDeleteMixin):
    __tablename__ = "job_postings"

    
    title: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False,
        index=True
    )
    
    description: Mapped[str] = mapped_column(
        LongTextType,
        nullable=False,
        default=None
    )
    
    department_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    designation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    location: Mapped[str | None] = mapped_column(
        ShortTextType,
        nullable=True,
        default=None
    )
    
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType, name="employment_type", native_enum=True),
        nullable=False,
        default=None
    )
    
    experience_years: Mapped[Decimal] = mapped_column(
        DECIMAL(4, 2),
        nullable=False,
        default=None
    )
    
    skills: Mapped[list[dict[UUID, SkillLevel]]] = mapped_column(
        JSONB,
        nullable=False,
    )
    
    salary: Mapped[Decimal | None] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
        default=None
    )
    
    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    
    deadline_reminder_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    
    status: Mapped[JobPostingStatus] = mapped_column(
        Enum(JobPostingStatus, name="job_posting_status", native_enum=True),
        nullable=False,
        default=JobPostingStatus.DRAFT
    )
    
    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # --- relationships ---
    department: Mapped["Department"] = relationship(
        back_populates="job_postings",
        foreign_keys=[department_id],
    )
    designation: Mapped["Designation"] = relationship(
        back_populates="job_postings",
        foreign_keys=[designation_id],
    )
    created_by_user: Mapped[Optional["User"]] = relationship(
        back_populates="job_postings",
        foreign_keys=[created_by],
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="job_posting",
        cascade="all, delete-orphan",
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="job_posting",
        cascade="all, delete-orphan",
    )
    
    