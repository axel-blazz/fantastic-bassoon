from uuid import UUID
from events.base import BaseEvent
from datetime import datetime

class IncidentCreatedEvent(BaseEvent):
    incident_id: UUID
    title: str
    status: str

class LogAttachedEvent(BaseEvent):
    incident_id: UUID
    log_id: UUID
    message_preview: str

class AnalysisRequestedEvent(BaseEvent):
    incident_id: UUID
    reason: str
    triggered_by: str # "manual" | "system" | "log_attached"