from uuid import UUID
from core.auth import get_current_user, require_roles
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from schemas.incidents import IncidentOut, IncidentIn, IncidentPatch
from schemas.incident_log import IncidentLogIn, IncidentLogOut
from services.incident_log_service import incident_log_db_to_out
from services.incident_service import (
    add_incident_log_service,
    delete_incident_service,
    get_incident_service,
    incident_in_to_db,
    incident_db_to_incident_out,
    apply_incident_patch,
    create_incident_service,
    list_incidents_service,
    update_incident_service,
)
from models.incidents import IncidentDB
from models.incident_logs import IncidentLogDB


router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
async def create_incident(
    payload: IncidentIn,
    db: Session = Depends(get_db),
    _=Depends(require_roles("ENGINEER", "ADMIN")),
):
    try:
        incident_db = create_incident_service(db, payload)
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
    try:
        incident_db = update_incident_service(db, incident_id, payload)
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
    try:
        incident_db = get_incident_service(db, incident_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    return incident_db_to_incident_out(incident_db)


@router.get("/", response_model=list[IncidentOut])
async def list_incidents(db: Session = Depends(get_db), _=Depends(get_current_user)):
    incidents_db = list_incidents_service(db)
    return [incident_db_to_incident_out(inc) for inc in incidents_db]


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_incident(
    incident_id: UUID, db: Session = Depends(get_db), _=Depends(require_roles("ADMIN"))
):
    
    try:
        delete_incident_service(db, incident_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Incident deletion failed: {e}")
    return None


@router.post("/{incident_id}/logs", status_code=status.HTTP_201_CREATED)
async def add_incident_log(
    incident_id: UUID,
    payload: IncidentLogIn,
    db: Session = Depends(get_db),
    _=Depends(require_roles("ENGINEER", "ADMIN")),
):
    try:
        log = add_incident_log_service(db, incident_id, payload.message)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Adding log failed: {e}")

    return incident_log_db_to_out(log)
