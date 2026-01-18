from schemas.user import UserIn, UserOut, UserRole
from models.user import User as UserDB
from core.security import hash_password

def user_in_to_db(user_in: UserIn) -> UserDB:
    return UserDB(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role=user_in.role
    )

def user_db_to_user_out(user_db: UserDB) -> UserOut:
    return UserOut(
        id=user_db.id,
        email=user_db.email,
        role=UserRole(user_db.role),
        created_at=user_db.created_at
    )