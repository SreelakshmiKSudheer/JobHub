from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ApplicationStatus
from app.schemas.job_posting import JobPostingResponse


class ApplicationBase(BaseModel):
    job_posting_id: UUID = Field(..., description="The unique identifier of the job posting")
    employee_id: UUID = Field(..., description="The unique identifier of the employee")


class ApplicationCreate(BaseModel):
    job_posting_id: UUID = Field(..., description="The unique identifier of the job posting")


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus = Field(..., description="The status of the application")


class ApplicationResponse(ApplicationBase):
    id: UUID
    status: ApplicationStatus = Field(..., description="The status of the application")
    created_at: datetime
    updated_at: datetime
    withdraw_allowed: bool = Field(default=False)
    job_posting: Optional[JobPostingResponse] = None

    model_config = ConfigDict(from_attributes=True)