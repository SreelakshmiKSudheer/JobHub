from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ApplicationStatus


class ApplicationBase(BaseModel):
    job_posting_id: UUID = Field(..., description="The unique identifier of the job posting")
    
    employee_id: UUID = Field(..., description="The unique identifier of the employee")


class ApplicationCreate(ApplicationBase):
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED, description="The status of the application")



class ApplicationUpdate(BaseModel):
    status: ApplicationStatus | None = Field(None, description="The status of the application")


class ApplicationResponse(ApplicationBase):
    """Properties returned to the client."""
    id: UUID
    status: ApplicationStatus = Field(..., description="The status of the application")
    created_at: datetime
    updated_at: datetime

    # Enables Pydantic to read data directly from the SQLAlchemy model instance
    model_config = ConfigDict(from_attributes=True)