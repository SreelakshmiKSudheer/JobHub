from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.core.constants import LONG_TEXT_MAX_LENGTH, SHORT_TEXT_MAX_LENGTH
from app.models.enums import EmploymentType, JobPostingStatus

class JobPostingBase(BaseModel):
    title: str = Field(..., description="The title of the job posting", max_length=SHORT_TEXT_MAX_LENGTH)
    description: str = Field(..., description="The description of the job posting", max_length=LONG_TEXT_MAX_LENGTH)
    department_id: UUID = Field(..., description="The unique identifier of the department for the job posting")
    designation_id: UUID = Field(..., description="The unique identifier of the designation for the job posting")
    employment_type: EmploymentType = Field(..., description="The employment type for the job posting")    
    experience_years: Decimal = Field(..., description="The required years of experience for the job posting")
    skills: list[dict[UUID, str | int]] = Field(..., description="The skills required for the job posting")
    deadline: datetime = Field(..., description="The application deadline for the job posting")
    
    
class JobPostingCreate(JobPostingBase):
    location: str | None = Field(default=None, description="The location of the job posting")
    salary: Decimal | None = Field(default=None, description="The salary offered for the job posting")
    deadline_reminder_at: datetime | None = Field(default=None, description="The reminder time for the application deadline")
    status: JobPostingStatus = Field(default=JobPostingStatus.DRAFT, description="The status of the job posting")
    
class JobPostingUpdate(BaseModel):
    title: str | None = Field(default=None, description="The title of the job posting", max_length=SHORT_TEXT_MAX_LENGTH)
    description: str | None = Field(default=None, description="The description of the job posting", max_length=LONG_TEXT_MAX_LENGTH)
    department_id: UUID | None = Field(default=None, description="The unique identifier of the department for the job posting")
    designation_id: UUID | None = Field(default=None, description="The unique identifier of the designation for the job posting")
    location: str | None = Field(default=None, description="The location of the job posting")
    employment_type: EmploymentType | None = Field(default=None, description="The employment type for the job posting")    
    experience_years: Decimal | None = Field(default=None, description="The required years of experience for the job posting")
    skills: list[dict[UUID, str | int]] | None = Field(default=None, description="The skills required for the job posting")
    salary: Decimal | None = Field(default=None, description="The salary offered for the job posting")
    deadline: datetime | None = Field(default=None, description="The application deadline for the job posting")
    deadline_reminder_at: datetime | None = Field(default=None, description="The reminder time for the application deadline")
    status: JobPostingStatus | None = Field(default=None, description="The status of the job posting")
    
    
class JobPostingResponse(JobPostingBase):
    id: UUID = Field(..., description="The unique identifier of the job posting")
    location: str | None = Field(default=None, description="The location of the job posting")
    salary: Decimal | None = Field(default=None, description="The salary offered for the job posting")
    deadline_reminder_at: datetime | None = Field(default=None, description="The reminder time for the application deadline")
    status: JobPostingStatus = Field(..., description="The status of the job posting")
    created_by: UUID | None = Field(default=None, description="The unique identifier of the user who created the job posting")
    
    
    created_at: datetime = Field(..., description="The creation time of the job posting")
    updated_at: datetime = Field(..., description="The last update time of the job posting")
    deleted_at: datetime | None = Field(default=None, description="The deletion time of the job posting")
    
    model_config = ConfigDict(from_attributes=True)