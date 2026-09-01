from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.repository.skill import (
    create_skill,
    delete_skill,
    get_skill_by_id,
    get_skill_by_name,
    get_skills,
    update_skill,
)
from app.schemas.skill import SkillCreate, SkillUpdate


class SkillService:

    @staticmethod
    def get_skills(db: Session) -> list[Skill]:
        return get_skills(db)

    @staticmethod
    def get_skill_by_id(db: Session, skill_id: UUID) -> Skill:
        skill = get_skill_by_id(db, skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        return skill

    @staticmethod
    def create_skill(db: Session, payload: SkillCreate) -> Skill:
        existing = get_skill_by_name(db, payload.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Skill with name '{payload.name}' already exists",
            )
        return create_skill(db, payload)

    @staticmethod
    def update_skill(db: Session, skill_id: UUID, payload: SkillUpdate) -> Skill:
        skill = get_skill_by_id(db, skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        
        if payload.name and payload.name.lower() != skill.name.lower():
            existing = get_skill_by_name(db, payload.name)
            if existing and existing.id != skill_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Skill with name '{payload.name}' already exists",
                )
        return update_skill(db, skill, payload)

    @staticmethod
    def delete_skill(db: Session, skill_id: UUID) -> None:
        skill = get_skill_by_id(db, skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
        delete_skill(db, skill)