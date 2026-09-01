from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.repository.skill import get_skills


class SkillService:
    
    @staticmethod
    def get_skills(db: Session):
        return get_skills(db)