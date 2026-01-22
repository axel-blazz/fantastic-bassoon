from models.incident_logs import IncidentLogDB
from repositories.incident_log_repo import save_log
from schemas.incidents import *
from models.incidents import IncidentDB
from services.incident_log_service import incident_log_db_to_out
from sqlalchemy.orm import Session
from repositories.incident_repo import get_by_id, list_all, save, delete
from events.incident_events import IncidentCreatedEvent
from events import event_dispatcher
from uuid import uuid4
from datetime import datetime, timezone


VALID_STATUS_TRANSITIONS = {
    IncidentStatus.OPEN: {IncidentStatus.IN_PROGRESS, IncidentStatus.CLOSED},
    IncidentStatus.IN_PROGRESS: {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: {IncidentStatus.CLOSED},
    IncidentStatus.CLOSED: set(),
}


def is_valid_status_transition(
    current_status: IncidentStatus, new_status: IncidentStatus
) -> bool:
    allowed_transitions = VALID_STATUS_TRANSITIONS.get(current_status, set())
    return new_status in allowed_transitions


def incident_in_to_db(incident_in: IncidentIn) -> IncidentDB:
    return IncidentDB(
        title=incident_in.title,
        description=incident_in.description,
        status=IncidentStatus.OPEN.value,
    )


def incident_db_to_incident_out(incident_db: IncidentDB) -> IncidentOut:
    return IncidentOut(
        id=incident_db.id,
        title=incident_db.title,
        description=incident_db.description,
        status=IncidentStatus(incident_db.status),
        created_at=incident_db.created_at,
        updated_at=incident_db.updated_at,
        logs=[incident_log_db_to_out(log) for log in incident_db.logs],
    )


def incident_db_to_created_event(incident: IncidentDB) -> IncidentCreatedEvent:
    return IncidentCreatedEvent(
        event_id=uuid4(),
        event_type="IncidentCreated",
        occured_at=datetime.now(timezone.utc),
        source="incident_service",
        incident_id=incident.id,
        title=incident.title,
        status=IncidentStatus(incident.status).value,
    )


def apply_incident_patch(
    incident_db: IncidentDB, incident_patch: IncidentPatch
) -> IncidentDB:
    if incident_patch.status is None:
        raise ValueError("No fields provided for update")
    if incident_patch.status:
        if not is_valid_status_transition(
            IncidentStatus(incident_db.status), incident_patch.status
        ):
            raise ValueError(
                f"Invalid status transition from {incident_db.status} to {incident_patch.status.value}"
            )
        incident_db.status = incident_patch.status.value
    return incident_db


def create_incident_service(db: Session, payload: IncidentIn) -> IncidentDB:
    incident_db = incident_in_to_db(payload)
    incident = save(db, incident_db)
    event = incident_db_to_created_event(incident)
    event_dispatcher.emit(event)
    return incident


def update_incident_service(
    db: Session, incident_id: UUID, payload: IncidentPatch
) -> IncidentDB:
    incident_db = get_by_id(db, incident_id)
    if not incident_db:
        raise ValueError("Incident not found")
    incident_db = apply_incident_patch(incident_db, payload)
    return save(db, incident_db)


def get_incident_service(db: Session, incident_id: UUID) -> IncidentDB:
    incident_db = get_by_id(db, incident_id)
    if not incident_db:
        raise ValueError("Incident not found")
    return incident_db


def list_incidents_service(db: Session) -> list[IncidentDB]:
    return list_all(db)


def delete_incident_service(db: Session, incident_id: UUID) -> None:
    incident_db = get_by_id(db, incident_id)
    if not incident_db:
        raise ValueError("Incident not found")
    delete(db, incident_db)


def add_incident_log_service(
    db: Session, incident_id: UUID, message: str
) -> IncidentLogDB:
    incident = get_by_id(db, incident_id)
    if not incident:
        raise ValueError("Incident not found")
    incident_log_db = IncidentLogDB(incident_id=incident_id, message=message)
    return save_log(db, incident_log_db)
