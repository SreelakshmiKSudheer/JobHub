from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.skill import SkillResponse
from app.db.session import get_db
from app.schemas.response import APIResponse
from app.services.skill import SkillService

skill_router = APIRouter(prefix="/skills", tags=["Skills"])

@skill_router.get("", response_model=APIResponse[list[SkillResponse]], dependencies=[Depends(get_current_user)])
def get_skills(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = SkillService.get_skills(db)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Skills retrieved successfully",
        data=data,
        error=None
    )
