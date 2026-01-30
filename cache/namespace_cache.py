from .base import CacheBackend
from typing import Optional

class NamespaceCache(CacheBackend):
    def __init__(self, prefix: str, backend: CacheBackend):
        self.prefix = prefix
        self.backend = backend

    def _namespaced_key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    def get(self, key: str):
        namespaced_key = self._namespaced_key(key)
        return self.backend.get(namespaced_key)

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        namespaced_key = self._namespaced_key(key)
        self.backend.set(namespaced_key, value, ttl)

    def delete(self, key: str) -> None:
        namespaced_key = self._namespaced_key(key)
        self.backend.delete(namespaced_key)
    
    def exists(self, key: str) -> bool:
        return self.get(key) is not None