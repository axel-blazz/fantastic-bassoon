from schemas.incidents import *
from models.incidents import IncidentDB
from services.incident_log_service import incident_log_db_to_out

VALID_STATUS_TRANSITIONS = {
    IncidentStatus.OPEN: {IncidentStatus.IN_PROGRESS, IncidentStatus.CLOSED},
    IncidentStatus.IN_PROGRESS: {IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: {IncidentStatus.CLOSED},
    IncidentStatus.CLOSED: set(),
}

def is_valid_status_transition(current_status: IncidentStatus, new_status: IncidentStatus) -> bool:
    allowed_transitions = VALID_STATUS_TRANSITIONS.get(current_status, set())
    return new_status in allowed_transitions

def incident_in_to_db(incident_in: IncidentIn) -> IncidentDB:
    return IncidentDB(
        title=incident_in.title,
        description=incident_in.description,
        status=IncidentStatus.OPEN.value
    )

def incident_db_to_incident_out(incident_db: IncidentDB) -> IncidentOut:
    return IncidentOut(
        id=incident_db.id,
        title=incident_db.title,
        description=incident_db.description,
        status=IncidentStatus(incident_db.status),
        created_at=incident_db.created_at,
        updated_at=incident_db.updated_at,
        logs=[incident_log_db_to_out(log) for log in incident_db.logs]
    )

def apply_incident_patch(incident_db: IncidentDB, incident_patch: IncidentPatch) -> IncidentDB:
    if incident_patch.status is None:
        raise ValueError("No fields provided for update")
    if incident_patch.status:
        if not is_valid_status_transition(IncidentStatus(incident_db.status), incident_patch.status):
            raise ValueError(f"Invalid status transition from {incident_db.status} to {incident_patch.status.value}")
        incident_db.status = incident_patch.status.value
    return incident_db

