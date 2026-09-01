from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user, require_role
from app.schemas.department import DepartmentResponse
from app.schemas.response import APIResponse
from app.services.department import DepartmentService
from app.db.session import get_db

department_router = APIRouter(prefix="/departments", tags=["Departments"])

@department_router.get("", response_model=APIResponse[list[DepartmentResponse]] ,dependencies=[Depends(get_current_user)])
def get_departments(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    
    data = DepartmentService.get_departments(db)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Departments retrieved successfully",
        data=data,
        error=None
    )