
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.Mixins import PKMixin
from app.db.types import ShortTextType

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.job_posting import JobPosting

class Department(Base, PKMixin):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(
        ShortTextType,
        nullable=False,
        unique=True
    )
    
    # --- relationships ---
    employees: Mapped[list["Employee"]] = relationship(
        back_populates="department"
    )
    job_postings: Mapped[list["JobPosting"]] = relationship(
        back_populates="department"
    )