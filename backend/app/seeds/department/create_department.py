from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.department import Department
from app.models.enums import UserRole
from app.schemas import employee


def seed_create_department(db: Session):
    name = "Mobility"

    existing = (
        db.query(Department)
        .filter(Department.name == name)
        .first()
    )

    if existing:
        print("Department already exists.")
        return

    department = Department(
        name=name,
    )

    db.add(department)
    db.commit()

    print("Department created.")
