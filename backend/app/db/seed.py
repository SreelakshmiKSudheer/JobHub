import app.db.base  # Registers all models

from app.db.session import SessionLocal
from app.seeds.create_admin import seed_create_admin
from app.seeds.create_employee import seed_create_employee 

def run():
    db = SessionLocal()
    try:
        # seed_create_admin(db)
        seed_create_employee(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()