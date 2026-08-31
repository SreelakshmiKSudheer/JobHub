from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

from app.core.constants import SHORT_TEXT_MAX_LENGTH

class SkillBase(BaseModel):
    name: str = Field(..., description="The name of the skill", max_length=SHORT_TEXT_MAX_LENGTH)
    
class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, description="The name of the skill", max_length=SHORT_TEXT_MAX_LENGTH)
    
class SkillResponse(SkillBase):
    id: UUID = Field(..., description="The unique identifier of the skill")
    
    model_config = ConfigDict(from_attributes=True)