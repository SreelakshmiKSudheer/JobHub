import math
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.audit_log import AuditLog as AuditLogSchema
from app.schemas.common import PaginationMeta
from app.schemas.response import APIResponse
from app.services.audit_log import AuditLogService

audit_log_router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@audit_log_router.get(
    "",
    response_model=APIResponse[dict],
    dependencies=[Depends(require_admin)],
)
def get_audit_logs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    entity_type: Optional[str] = Query(default=None),
    entity_id: Optional[UUID] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    skip = (page - 1) * page_size
    items, total = AuditLogService.get_audit_logs(
        db=db, skip=skip, limit=page_size, entity_type=entity_type, entity_id=entity_id
    )

    items_data = [AuditLogSchema.model_validate(item).model_dump(mode="json") for item in items]
    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Audit logs retrieved successfully",
        data={
            "data": items_data,
            "meta": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": total_pages,
            },
        },
        error=None,
    )
