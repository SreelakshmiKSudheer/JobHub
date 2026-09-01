from sqlalchemy.orm import Session

from app.models.designation import Designation


def get_designations(db: Session):
    return db.query(Designation).all()