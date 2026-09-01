from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.dependencies import get_current_user
from app.db.session import get_db
from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import EmployeeResponse, EmployeeUpdate
from app.schemas.response import APIResponse
from app.services.employee import EmployeeService

employee_router = APIRouter(prefix="/employee", tags=["Employee Profile"])


def build_employee_response(emp: Employee) -> EmployeeResponse:
    return EmployeeResponse(
        id=emp.id,
        email=emp.user.email,
        role=emp.user.role,
        created_at=emp.user.created_at,
        updated_at=emp.user.updated_at,
        full_name=emp.full_name,
        employee_code=emp.employee_code,
        department_id=emp.department_id,
        designation_id=emp.designation_id,
        experience_years=emp.experience_years,
        skills=emp.skills or [],
    )


@employee_router.get("/me", response_model=APIResponse[EmployeeResponse], dependencies=[Depends(get_current_user)])
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    emp = EmployeeService.get_employee_profile(db, user_id=current_user.id)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Employee profile retrieved successfully",
        data=build_employee_response(emp),
        error=None,
    )


@employee_router.put("/me", response_model=APIResponse[EmployeeResponse], dependencies=[Depends(get_current_user)])
def update_my_profile(
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    emp = EmployeeService.update_employee_profile(db, user_id=current_user.id, payload=payload)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Employee profile updated successfully",
        data=build_employee_response(emp),
        error=None,
    )
