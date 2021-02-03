from sqlalchemy.orm.session import Session
from app.database import SessionLocal
from app.models.users import User
from app.dependencies import hash_password, get_db


if __name__ == '__main__':
    db = SessionLocal()

    admin = db.query(User).get("admin")
    if admin:
        print("Admin user already exists")
        db.close()
        quit()

    user = User()
    user.active = True
    user.admin = True
    user.username = "admin"
    user.hashed_password = hash_password("admin")
    user.name = "Admin"
    db.add(user)
    db.flush()
    db.commit()

    print("Admin user created")
    db.close()