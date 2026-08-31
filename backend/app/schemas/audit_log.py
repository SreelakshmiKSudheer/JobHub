from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import PaginatedResponse


class AuditLog(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the audit log entry")
    user_id: UUID | None = Field(default=None, description="The unique identifier of the user who performed the action")
    entity_type: str = Field(..., description="The type of the entity being audited")
    entity_id: UUID = Field(..., description="The unique identifier of the entity being audited")
    action: str = Field(..., description="The action that was performed on the entity")
    old_value: Any | None = Field(default=None, description="The old value of the entity before the action was performed")
    new_value: Any | None = Field(default=None, description="The new value of the entity after the action was performed")
    timestamp: datetime = Field(..., description="The timestamp when the action was performed")

    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(PaginatedResponse[AuditLog]):
    pass
