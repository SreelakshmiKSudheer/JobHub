from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repository.employee import get_employee_by_user_id, update_employee
from app.schemas.employee import EmployeeUpdate


class EmployeeService:

    @staticmethod
    def get_employee_profile(db: Session, user_id: UUID) -> Employee:
        employee = get_employee_by_user_id(db, user_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee profile not found")
        return employee

    @staticmethod
    def update_employee_profile(db: Session, user_id: UUID, payload: EmployeeUpdate) -> Employee:
        employee = get_employee_by_user_id(db, user_id)
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee profile not found")
        return update_employee(db, employee, payload)
