from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    role: UserRole = Field(..., description="The role of the user")
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="The password of the user")
    
class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, description="The email address of the user")
    password: str | None = Field(None, min_length=8, description="The password of the user")
    role: UserRole | None = Field(default=None, description="The role of the user")
    
class UserResponse(UserBase):
    id: UUID = Field(..., description="The unique identifier of the user")
    last_login: str | None = Field(default=None, description="The last login time of the user")
    created_at: str = Field(..., description="The creation time of the user")
    updated_at: str = Field(..., description="The last update time of the user")
    
    model_config = ConfigDict(from_attributes=True)