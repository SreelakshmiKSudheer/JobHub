from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import Enum, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from app.db.base_class import Base
from app.models.Mixins import PKMixin, CreatedAtMixin, UpdatedAtMixin
from app.models.enums import UserRole
from app.db.types import EmailType


if TYPE_CHECKING:
    from employee import Employee
    from app.models.job_posting import JobPosting
    from app.models.job_template import JobTemplate
    from app.models.notification import Notification

class User(Base, PKMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        EmailType, 
        unique=True, 
        nullable=False
    )
    
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        
    )
    
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole,
        name="user_role", 
        native_enum=True),
        nullable=False, 
    )
    
    last_login: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # --- relationships ---
    employee: Mapped[Optional["Employee"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )
    
    job_postings: Mapped[list["JobPosting"]] = relationship(
        back_populates="created_by_user",
        cascade="all, delete-orphan",
    )
    
    job_templates: Mapped[list["JobTemplate"]] = relationship(
        back_populates="created_by_user",
        cascade="all, delete-orphan",
    )
    
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="recipient",
        cascade="all, delete-orphan",
    )
      