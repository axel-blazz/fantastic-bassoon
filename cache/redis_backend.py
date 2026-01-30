from .base import CacheBackend
from .redis_client import redis_client
from typing import Optional

class RedisCacheBackend(CacheBackend):

    def get(self, key: str):
        return redis_client.get(key)

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        if ttl:
            redis_client.setex(key, ttl, value)
        else:
            redis_client.set(key, value)

    def delete(self, key: str) -> None:
        redis_client.delete(key)
    
    def exists(self, key: str) -> bool:
        return redis_client.get(key) is not None