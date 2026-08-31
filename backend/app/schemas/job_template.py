from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.core.constants import LONG_TEXT_MAX_LENGTH, SHORT_TEXT_MAX_LENGTH
from app.models.enums import EmploymentType, JobPostingStatus

class JobTemplateBase(BaseModel):
    name: str = Field(..., description="The name of the job template", max_length=SHORT_TEXT_MAX_LENGTH)
    title: str = Field(..., description="The title of the job posting", max_length=SHORT_TEXT_MAX_LENGTH)
    description: str | None = Field(default=None, description="The description of the job posting", max_length=LONG_TEXT_MAX_LENGTH)
    designation_id: UUID = Field(..., description="The unique identifier of the designation for the job posting")
    employment_type: EmploymentType | None = Field(..., description="The employment type for the job posting")    
    experience_years: Decimal | None = Field(..., description="The required years of experience for the job posting")
    skills: list[dict[UUID, str]] | None = Field(..., description="The skills required for the job posting")
    salary: Decimal | None = Field(default=None, description="The salary offered for the job posting")    
    
class JobTemplateCreate(JobTemplateBase):
    created_by: UUID = Field(..., description="The unique identifier of the user who created the job posting")
        
class JobTemplateUpdate(BaseModel):
    name: str | None = Field(default=None, description="The name of the job template", max_length=SHORT_TEXT_MAX_LENGTH)
    title: str | None = Field(default=None, description="The title of the job posting", max_length=SHORT_TEXT_MAX_LENGTH)
    description: str | None = Field(default=None, description="The description of the job posting", max_length=LONG_TEXT_MAX_LENGTH)
    designation_id: UUID | None = Field(default=None, description="The unique identifier of the designation for the job posting")
    employment_type: EmploymentType | None = Field(default=None, description="The employment type for the job posting")    
    experience_years: Decimal | None = Field(default=None, description="The required years of experience for the job posting")
    skills: list[dict[UUID, str]] | None = Field(default=None, description="The skills required for the job posting")
    salary: Decimal | None = Field(default=None, description="The salary offered for the job posting")    
    
class JobTemplateResponse(JobTemplateBase):
    id: UUID = Field(..., description="The unique identifier of the job posting")
    created_by: UUID | None = Field(default=None, description="The unique identifier of the user who created the job posting")
    
    
    created_at: datetime = Field(..., description="The creation time of the job posting")
    updated_at: datetime = Field(..., description="The last update time of the job posting")
    deleted_at: datetime | None = Field(default=None, description="The deletion time of the job posting")
    
    model_config = ConfigDict(from_attributes=True)