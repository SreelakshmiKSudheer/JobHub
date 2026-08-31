from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

from app.core.constants import SHORT_TEXT_MAX_LENGTH

class DepartmentBase(BaseModel):
    name: str = Field(..., description="The name of the department", max_length=SHORT_TEXT_MAX_LENGTH)
    
class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, description="The name of the department", max_length=SHORT_TEXT_MAX_LENGTH)
    
class DepartmentResponse(DepartmentBase):
    id: UUID = Field(..., description="The unique identifier of the department")
    
    model_config = ConfigDict(from_attributes=True)