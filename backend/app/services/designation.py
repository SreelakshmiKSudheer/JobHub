from sqlalchemy.orm import Session

from app.models.designation import Designation
from app.repository.designation import get_designations


class DesignationService:
    
    @staticmethod
    def get_designations(db: Session):
        return get_designations(db)