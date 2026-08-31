
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.base_class import Base
from app.models.Mixins import CreatedAtMixin, PKMixin, UpdatedAtMixin
from app.db.types import ShortTextType, LongTextType, EmployeeCodeType    
from app.models.enums import EmploymentType, ApplicationStatus, SkillLevel
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models.notification import Notification
    from app.models.job_posting import JobPosting
    from app.models.employee import Employee

class Application(Base, PKMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "applications"

    
    job_posting_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("job_postings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    employee_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status", native_enum=True),
        nullable=False,
        default=ApplicationStatus.APPLIED,
        index=True
    )
    
    # --- relationships ---
    job_posting: Mapped["JobPosting"] = relationship(
        back_populates="applications",
        foreign_keys=[job_posting_id],
    )
    employee: Mapped["Employee"] = relationship(
        back_populates="applications",
        foreign_keys=[employee_id],
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )
    
    
    
    