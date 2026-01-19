from datetime import datetime as dt, timezone
import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base


class IncidentLogDB(Base):
    __tablename__ = "incident_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False)
    message = Column(String(2000), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: dt.now(timezone.utc)
    )
