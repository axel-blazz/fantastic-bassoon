from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BaseEvent(BaseModel):
    event_id: UUID
    event_type: str
    occured_at: datetime
    source: str

    class Config:
        frozen = True  # Make the model immutable
