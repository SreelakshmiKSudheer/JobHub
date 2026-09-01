from sqlalchemy.orm import Session

from app.models.department import Department
from app.repository.department import get_departments


class DepartmentService:

    @staticmethod
    def get_departments(db: Session):
        return get_departments(db)
