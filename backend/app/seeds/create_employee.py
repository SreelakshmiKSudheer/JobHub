from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import UserRole
from app.core.security import get_password_hash


def seed_create_employee(db: Session):
    email = "tony@jobhub.com"
    password = "tony@123"

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        print("Employee already exists.")
        return

    employee = User(
        email=email,
        password_hash=get_password_hash(password),
        role=UserRole.USER,
    )

    db.add(employee)
    db.commit()

    print("Employee created.")