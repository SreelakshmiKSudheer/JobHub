from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.skill import Skill


def seed_create_skill(db: Session):
    name = "PostgreSQL"

    existing = (
        db.query(Skill)
        .filter(Skill.name == name)
        .first()
    )

    if existing:
        print("Skill already exists.")
        return

    skill = Skill(
        name=name,
    )

    db.add(skill)
    db.commit()

    print("Skill created.")
