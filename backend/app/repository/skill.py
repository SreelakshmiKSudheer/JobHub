from sqlalchemy.orm import Session

from app.models.skill import Skill


def get_skills(db: Session):
    return db.query(Skill).all()