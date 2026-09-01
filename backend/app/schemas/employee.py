from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import EMPLOYEE_CODE_MAX_LENGTH, NAME_MAX_LENGTH
from app.models.enums import SkillLevel, UserRole
from app.schemas.user import UserBase, UserCreate, UserResponse, UserUpdate


class EmployeeBase(UserBase):
    full_name: str = Field(..., description="The full name of the employee", max_length=NAME_MAX_LENGTH)
    employee_code: str = Field(..., description="The unique code of the employee", max_length=EMPLOYEE_CODE_MAX_LENGTH)
    department_id: UUID = Field(..., description="The unique identifier of the department the employee belongs to")
    designation_id: UUID = Field(..., description="The unique identifier of the designation of the employee")
    experience_years: Decimal = Field(..., description="The experience of the employee in years", ge=0)
    skills: list[dict[UUID, int]] | None = Field(default=[], description="The skills of the employee with their levels")


class EmployeeCreate(EmployeeBase, UserCreate):
    pass


class EmployeeUpdate(BaseModel):
    experience_years: Decimal | None = Field(default=None, description="The experience of the employee in years", ge=0)
    skills: list[dict[UUID, int]] | None = Field(default=None, description="The skills of the employee with their levels")


class EmployeeResponse(UserResponse, EmployeeBase):
    id: UUID = Field(..., description="The unique identifier of the employee")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
