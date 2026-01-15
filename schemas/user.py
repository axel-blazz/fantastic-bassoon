from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ENGINEER = "ENGINEER"
    VIEWER = "VIEWER"

class UserIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Password must be at least 8 characters long")
    role: UserRole

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime


class UserPatch(BaseModel):
    role: Optional[UserRole] = None