from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

from app.core.constants import SHORT_TEXT_MAX_LENGTH

class DesignationBase(BaseModel):
    name: str = Field(..., description="The name of the designation", max_length=SHORT_TEXT_MAX_LENGTH)
    
class DesignationCreate(DesignationBase):
    pass

class DesignationUpdate(BaseModel):
    name: str | None = Field(default=None, description="The name of the designation", max_length=SHORT_TEXT_MAX_LENGTH)
    
class DesignationResponse(DesignationBase):
    id: UUID = Field(..., description="The unique identifier of the designation")
    
    model_config = ConfigDict(from_attributes=True)