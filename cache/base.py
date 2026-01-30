from abc import ABC, abstractmethod
from typing import Optional

class CacheBackend(ABC):

    @abstractmethod
    def get(self, key: str):
        """Retrieve a value from the cache by key."""
        pass

    @abstractmethod
    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with an optional time-to-live (ttl)."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a value from the cache by key."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        pass