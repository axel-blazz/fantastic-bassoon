import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime as dt, timezone

from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum("ADMIN", "ENGINEER", "VIEWER", name="user_roles"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: dt.now(timezone.utc))