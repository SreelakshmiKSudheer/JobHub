import app.db.base  # Registers all models

from app.db.session import SessionLocal
from app.seeds.admin.create_admin import seed_create_admin
from app.seeds.employee.create_employee import seed_create_employee 
from app.seeds.department.create_department import seed_create_department
from app.seeds.designation.create_designation import seed_create_designation
from app.seeds.skill.create_skill import seed_create_skill

def run():
    db = SessionLocal()
    try:
        # seed_create_admin(db)
        # seed_create_employee(db)
        # seed_create_department(db)
        # seed_create_designation(db)
        seed_create_skill(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()