from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import UserRole
from app.core.security import get_password_hash


def seed_create_admin(db: Session):
    email = "admin@jobhub.com"
    password = "Admin@123"

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        print("Admin already exists.")
        return

    admin = User(
        email=email,
        password_hash=get_password_hash(password),
        role=UserRole.ADMIN,
    )

    db.add(admin)
    db.commit()

    print("Admin created.")