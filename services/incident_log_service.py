from schemas.incident_log import IncidentLogIn, IncidentLogOut
from models.incident_logs import IncidentLogDB

def incident_log_db_to_out(log: IncidentLogDB) -> IncidentLogOut:
    return IncidentLogOut(
        id=log.id,
        incident_id=log.incident_id,
        message=log.message,
        created_at=log.created_at,
    )
