from db.session import SessionLocal
from models.user import User as UserDB

db = SessionLocal()

user = UserDB(email="test@example.com", password_hash="hashed", role="ENGINEER")

db.add(user)
db.commit()
db.refresh(user)

print(user.id)

db.close()
