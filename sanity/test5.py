from db.session import SessionLocal
from models.incidents import IncidentDB
from schemas import user

db = SessionLocal()

incident = IncidentDB(title="Test Incident", description="This is a test incident.")

db.add(incident)
db.commit()
db.refresh(incident)

print(incident.id)

db.close()

