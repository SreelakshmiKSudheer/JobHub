import app.db.base  # Registers all models

from app.db.session import SessionLocal
from app.seeds.admin.create_admin import seed_create_admin
from app.seeds.employee.create_employee import seed_create_employee 
from app.seeds.department.create_department import seed_create_department

def run():
    db = SessionLocal()
    try:
        # seed_create_admin(db)
        # seed_create_employee(db)
        seed_create_department(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()