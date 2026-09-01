from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repository.audit_log import create_audit_log, get_audit_logs


class AuditLogService:

    @staticmethod
    def log_action(
        db: Session,
        user_id: UUID | None,
        entity_type: str,
        entity_id: UUID,
        action: str,
        old_value: Any | None = None,
        new_value: Any | None = None,
    ) -> AuditLog:
        return create_audit_log(
            db=db,
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
        )

    @staticmethod
    def get_audit_logs(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
    ) -> tuple[list[AuditLog], int]:
        return get_audit_logs(db=db, skip=skip, limit=limit, entity_type=entity_type, entity_id=entity_id)
