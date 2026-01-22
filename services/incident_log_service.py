from datetime import timezone, datetime
from uuid import uuid4
from events.incident_events import LogAttachedEvent
from schemas.incident_log import IncidentLogIn, IncidentLogOut
from models.incident_logs import IncidentLogDB

def incident_log_db_to_out(log: IncidentLogDB) -> IncidentLogOut:
    return IncidentLogOut(
        id=log.id,
        incident_id=log.incident_id,
        message=log.message,
        created_at=log.created_at,
    )


def incident_log_db_to_attached_event(log: IncidentLogDB) -> LogAttachedEvent:
    return LogAttachedEvent(
        event_id=uuid4(),
        event_type="LogAttached",
        occurred_at=datetime.now(timezone.utc),
        source="incident_log_service",
        incident_id=log.incident_id,
        log_id=log.id,
        message_preview=log.message[:100],
    )
