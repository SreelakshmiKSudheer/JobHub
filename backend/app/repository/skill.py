from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


def get_skills(db: Session) -> list[Skill]:
    return db.query(Skill).filter(Skill.deleted_at.is_(None)).order_by(Skill.name).all()


def get_skill_by_id(db: Session, skill_id: UUID) -> Skill | None:
    return db.query(Skill).filter(Skill.id == skill_id, Skill.deleted_at.is_(None)).one_or_none()


def get_skill_by_name(db: Session, name: str) -> Skill | None:
    return db.query(Skill).filter(Skill.name.ilike(name), Skill.deleted_at.is_(None)).first()


def create_skill(db: Session, payload: SkillCreate) -> Skill:
    skill = Skill(name=payload.name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def update_skill(db: Session, skill: Skill, payload: SkillUpdate) -> Skill:
    if payload.name is not None:
        skill.name = payload.name
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill) -> None:
    skill.deleted_at = datetime.now(timezone.utc)
    db.add(skill)
    db.commit()