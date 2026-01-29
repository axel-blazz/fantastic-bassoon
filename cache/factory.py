from .base import CacheBackend
from .redis_backend import RedisCacheBackend

_cache_backend: CacheBackend | None = None

def get_cache_backend() -> CacheBackend:
    global _cache_backend
    if _cache_backend is None:
        _cache_backend = RedisCacheBackend()
    return _cache_backend