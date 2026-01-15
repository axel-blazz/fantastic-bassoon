from db.session import SessionLocal
from schemas.user import UserIn, UserRole
from services.user_service import user_in_to_db, user_db_to_user_out

db = SessionLocal()

user_in = UserIn(
    email="day45@example.com", password="strongpassword", role="ENGINEER"
)

user_db = user_in_to_db(user_in)

db.add(user_db)
db.commit()
db.refresh(user_db)

user_out = user_db_to_user_out(user_db)

print(user_out)

db.close()
