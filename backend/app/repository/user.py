from datetime import datetime, timezone

from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).one_or_none()

def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.get(User, user_id)

def update_user_last_login(db: Session, user: User):
    user.last_login = datetime.now(timezone.utc)
    db.commit()

def increment_user_token_version(db: Session, user: User):
    user.token_version += 1
    db.commit()
    
def update_user_password(db: Session, user: User, new_password_hash: str):
    user.password_hash = new_password_hash
    db.commit()