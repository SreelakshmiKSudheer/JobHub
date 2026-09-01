from sqlalchemy.orm import Session

from app.models.department import Department


def get_departments(db: Session):
    return db.query(Department).all()