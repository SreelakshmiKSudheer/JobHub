from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.designation import Designation


def seed_create_designation(db: Session):
    name = "Senior Software Engineer"

    existing = (
        db.query(Designation)
        .filter(Designation.name == name)
        .first()
    )

    if existing:
        print("Designation already exists.")
        return

    designation = Designation(
        name=name,
    )

    db.add(designation)
    db.commit()

    print("Designation created.")
