import uuid
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime as dt, timezone

from db.base import Base


class IncidentDB(Base):
    __tablename__ = "incidents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String(120), nullable=False)
    description = Column(String(2000), nullable=False)
    status = Column(String, nullable=False, default="OPEN")
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: dt.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.now(timezone.utc),
        onupdate=lambda: dt.now(timezone.utc),
    )

    logs = relationship(
        "IncidentLogDB",
        backref="incident",
        order_by="IncidentLogDB.created_at",
        cascade="all, delete-orphan",
    )
