from typing import Any
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: UUID | None,
    entity_type: str,
    entity_id: UUID,
    action: str,
    old_value: Any | None = None,
    new_value: Any | None = None,
) -> AuditLog:
    log_entry = AuditLog(
        user_id=user_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    entity_type: str | None = None,
    entity_id: UUID | None = None,
) -> tuple[list[AuditLog], int]:
    query = db.query(AuditLog)
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)

    total = query.count()
    items = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return items, total
