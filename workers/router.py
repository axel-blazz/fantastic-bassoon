from loguru import logger
from handlers import (
    handle_incident_created,
    handle_log_attached,
    handle_analysis_requested,
)

EVENT_HANDLER_MAP = {
    "IncidentCreated": handle_incident_created,
    "LogAttached": handle_log_attached,
    "AnalysisRequested": handle_analysis_requested,
}

def route_event(event: dict) -> bool:
    event_type = event.get("event_type")
    handler = EVENT_HANDLER_MAP.get(event_type)
    if handler:
        handler(event)
        return True
    else:
        logger.warning(f"No handler found for event type: {event_type}")
        return False