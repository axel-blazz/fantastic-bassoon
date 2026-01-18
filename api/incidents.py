from uuid import UUID
from core.auth import get_current_user, require_roles
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from schemas.incidents import IncidentOut, IncidentIn, IncidentPatch
from services.incident_service import (
    incident_in_to_db,
    incident_db_to_incident_out,
    apply_incident_patch,
)
from models.incidents import IncidentDB


router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
async def create_incident(
    payload: IncidentIn,
    db: Session = Depends(get_db),
    _=Depends(require_roles("ENGINEER", "ADMIN")),
):
    incident_db = incident_in_to_db(payload)
    try:
        db.add(incident_db)
        db.commit()
        db.refresh(incident_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Incident creation failed: {e}")
    return incident_db_to_incident_out(incident_db)


@router.patch("/{incident_id}", response_model=IncidentOut)
async def update_incident(
    incident_id: UUID,
    payload: IncidentPatch,
    db: Session = Depends(get_db),
    _=Depends(require_roles("ENGINEER", "ADMIN")),
):
    incident_db = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not incident_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    try:
        incident_db = apply_incident_patch(incident_db, payload)
        db.commit()
        db.refresh(incident_db)
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Incident update failed: {e}")
    return incident_db_to_incident_out(incident_db)


@router.get("/{incident_id}", response_model=IncidentOut)
async def get_incident(
    incident_id: UUID, db: Session = Depends(get_db), _=Depends(get_current_user)
):
    incident_db = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not incident_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident_db_to_incident_out(incident_db)


@router.get("/", response_model=list[IncidentOut])
async def list_incidents(db: Session = Depends(get_db), _=Depends(get_current_user)):
    incidents_db = db.query(IncidentDB).all()
    return [incident_db_to_incident_out(inc) for inc in incidents_db]


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(
    incident_id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("ADMIN"))
):
    incident_db = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    if not incident_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    try:
        db.delete(incident_db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Incident deletion failed: {e}")
    return {"status": "success", "detail": "Incident deleted successfully"}
