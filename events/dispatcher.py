from events.base import BaseEvent
from loguru import logger

class EventDispatcher:
    def emit(self, event: BaseEvent) -> None:
        logger.info(f"Emitting event | {event.event_type} | ID: {event.event_id} | payload: {event.json()}")
        