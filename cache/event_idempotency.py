from typing import Optional
from .factory import get_cache_backend
from .namespace_cache import NamespaceCache

IDEMPOTENCY_PREFIX = "event_processed"
TTL_SECONDS = 24 * 60 * 60  # 24 hours

class EventIdempotencyStore:

    def __init__(self):
        self.cache = NamespaceCache(
            prefix=IDEMPOTENCY_PREFIX,
            backend=get_cache_backend()
        )
    
    
    def has_processed(self, event_id: str) -> bool:
        return self.cache.exists(event_id)
    
    def mark_processed(self, event_id: str) -> None:
        self.cache.set(
            key=event_id,
            value="1",
            ttl=TTL_SECONDS,
        )
    
    def clear(self, event_id: str) -> None:
        self.cache.delete(event_id)
