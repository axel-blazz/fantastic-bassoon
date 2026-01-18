from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class IncidentIn(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=2000)


class IncidentOut(BaseModel):
    id: UUID
    title: str
    description: str
    status: IncidentStatus
    created_at: datetime
    updated_at: datetime


class IncidentPatch(BaseModel):
    status: Optional[IncidentStatus] = None
