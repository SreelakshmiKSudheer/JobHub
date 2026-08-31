from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SkillLevel, UserRole
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse
from app.core.constants import NAME_MAX_LENGTH, EMPLOYEE_CODE_MAX_LENGTH

class EmployeeBase(UserBase):
    full_name: str = Field(..., description="The full name of the employee", max_lenght=NAME_MAX_LENGTH)
    
    employee_code: str = Field(..., description="The unique code of the employee", max_length=EMPLOYEE_CODE_MAX_LENGTH)
    
    department_id: UUID = Field(..., description="The unique identifier of the department the employee belongs to")
    
    designation_id: UUID = Field(..., description="The unique identifier of the designation of the employee")
    
    experience: Decimal = Field(..., description="The experience of the employee in years", ge=0)
    
    skills: list[dict[UUID, SkillLevel]] = Field(..., description="The skills of the employee with their levels")
    
    
class EmployeeCreate(EmployeeBase, UserCreate):
    pass
    
class EmployeeUpdate(UserUpdate):
    full_name: str | None = Field(default=None, description="The full name of the employee", max_length=NAME_MAX_LENGTH)
    
    employee_code: str | None = Field(default=None, description="The unique code of the employee", max_length=EMPLOYEE_CODE_MAX_LENGTH)
    
    department_id: UUID | None = Field(default=None, description="The unique identifier of the department the employee belongs to")
    
    designation_id: UUID | None = Field(default=None, description="The unique identifier of the designation of the employee")
    
    experience: Decimal | None = Field(default=None, description="The experience of the employee in years", ge=0)
    
    skills: list[dict[UUID, SkillLevel]] | None = Field(default=None, description="The skills of the employee with their levels")
    
class EmployeeResponse(UserResponse, EmployeeBase):
    id: UUID = Field(..., description="The unique identifier of the employee")
    
    model_config = ConfigDict(from_attributes=True)
