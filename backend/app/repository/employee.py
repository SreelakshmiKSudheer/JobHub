from uuid import UUID
from sqlalchemy.orm import Session, joinedload

from app.core.skills_utils import merge_skills
from app.models.employee import Employee
from app.schemas.employee import EmployeeUpdate


def get_employee_by_user_id(db: Session, user_id: UUID) -> Employee | None:
    return db.query(Employee).options(joinedload(Employee.user)).filter(Employee.id == user_id).one_or_none()


def update_employee(db: Session, employee: Employee, payload: EmployeeUpdate) -> Employee:
    update_data = payload.model_dump(exclude_unset=True)
    if "skills" in update_data:
        new_skills = update_data["skills"]
        update_data["skills"] = merge_skills(employee.skills, new_skills)

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee
