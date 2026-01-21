from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from models.incidents import IncidentDB
from typing import Optional

def get_by_id(db: Session, incident_id: UUID) -> Optional[IncidentDB]:
    return db.query(IncidentDB).options(selectinload(IncidentDB.logs)).filter(IncidentDB.id == incident_id).first()

def list_all(db: Session) -> list[IncidentDB]:
    return db.query(IncidentDB).all()

def save(db: Session, incident: IncidentDB) -> IncidentDB:
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

def delete(db: Session, incident: IncidentDB) -> None:
    db.delete(incident)
    db.commit()

