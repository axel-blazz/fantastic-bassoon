from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class IncidentLogIn(BaseModel):
    message: str = Field(..., min_length=10, max_length=2000)


class IncidentLogOut(BaseModel):
    id: UUID
    incident_id: UUID
    message: str
    created_at: datetime
