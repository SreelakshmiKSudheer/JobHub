from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.designation import DesignationResponse
from app.db.session import get_db
from app.schemas.response import APIResponse
from app.services.designation import DesignationService

designation_router = APIRouter(prefix="/designations", tags=["Designations"])

@designation_router.get("", response_model=APIResponse[list[DesignationResponse]], dependencies=[Depends(get_current_user)])
def get_designations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = DesignationService.get_designations(db)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Designations retrieved successfully",
        data=data,
        error=None
    )
