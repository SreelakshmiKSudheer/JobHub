from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.skill import SkillCreate, SkillResponse, SkillUpdate
from app.services.skill import SkillService

skill_router = APIRouter(prefix="/skills", tags=["Skills"])


@skill_router.get("", response_model=APIResponse[list[SkillResponse]], dependencies=[Depends(get_current_user)])
def get_skills(db: Session = Depends(get_db)):
    data = SkillService.get_skills(db)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Skills retrieved successfully",
        data=data,
        error=None,
    )


@skill_router.get("/{skill_id}", response_model=APIResponse[SkillResponse], dependencies=[Depends(get_current_user)])
def get_skill(skill_id: UUID, db: Session = Depends(get_db)):
    data = SkillService.get_skill_by_id(db, skill_id)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Skill retrieved successfully",
        data=data,
        error=None,
    )


@skill_router.post("", response_model=APIResponse[SkillResponse], status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_skill(payload: SkillCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    data = SkillService.create_skill(db, payload)
    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="Skill created successfully",
        data=data,
        error=None,
    )


@skill_router.put("/{skill_id}", response_model=APIResponse[SkillResponse], dependencies=[Depends(require_admin)])
def update_skill(skill_id: UUID, payload: SkillUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    data = SkillService.update_skill(db, skill_id, payload)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Skill updated successfully",
        data=data,
        error=None,
    )


@skill_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_skill(skill_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    SkillService.delete_skill(db, skill_id)
    return None
