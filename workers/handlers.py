from loguru import logger

def handle_incident_created(event: dict) -> None:
    logger.info(f"[Handler] Incident Created | incident_id : {event.get('incident_id')} | title: {event.get('title')}")

def handle_log_attached(event: dict) -> None:
    logger.info(f"[Handler] Log Attached | incident_id : {event.get('incident_id')} | log_id: {event.get('log_id')}")

def handle_analysis_requested(event: dict) -> None:
    logger.info(f"[Handler] Analysis Requested | incident_id : {event.get('incident_id')} | reason: {event.get('reason')}")