from sqlalchemy.orm import Session
from models.incident_logs import IncidentLogDB


def save_log(db: Session, log: IncidentLogDB) -> IncidentLogDB:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
