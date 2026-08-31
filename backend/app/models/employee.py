import uuid
from uuid import UUID, uuid4
from sqlalchemy import (
    UUID as PG_UUID,
    ForeignKey
)
from decimal import Decimal
from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from typing import TYPE_CHECKING

from app.db.base_class import Base
from app.db.types import NameType, EmployeeCodeType
from app.models.enums import SkillLevel


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.application import Application
    from app.models.designation import Designation
    from app.models.department import Department

class Employee(Base):
    __tablename__ = "employees"
    
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        NameType,
        nullable=False,
    )
    employee_code: Mapped[str] = mapped_column(
        EmployeeCodeType,
        nullable=False,
        unique=True
    )
    
    department_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    designation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("designations.id", ondelete="RESTRICT"),
        nullable=False
    )
    
    experience_years: Mapped[Decimal] = mapped_column(
        DECIMAL(2, 2),
        nullable=False,
        default=0
    )
    
    skills: Mapped[list[dict[UUID, SkillLevel]]] = mapped_column(
        JSONB,
        nullable=True,
        default=[]
    )
    
    # --- relationships ---
    user: Mapped["User"] = relationship(
        back_populates="employee",
        foreign_keys=[id],
    )
    department: Mapped["Department"] = relationship(
        back_populates="employees",
        foreign_keys=[department_id],
    )
    designation: Mapped["Designation"] = relationship(
        back_populates="employees",
        foreign_keys=[designation_id],
    )
    applications: Mapped[list["Application"]] = relationship(
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    