import app.db.base  # Registers all models

from app.db.session import SessionLocal
from app.seeds.create_admin import seed_create_admin 

def run():
    db = SessionLocal()
    try:
        seed_create_admin(db)
        
    finally:
        db.close()


if __name__ == "__main__":
    run()