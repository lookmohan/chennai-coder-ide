"""Fixed-window rate limiting. Redis-backed when reachable, in-process otherwise.

The in-process fallback is per-worker and only meant for development/tests or
as a degraded mode if Redis is briefly unavailable (a warning is logged).
"""
import logging
import threading
import time
from collections.abc import Callable
from functools import lru_cache
from typing import Protocol

from fastapi import Request

from app.core.config import Settings, get_settings
from app.core.errors import AppError

logger = logging.getLogger("app.rate_limit")


class Backend(Protocol):
    def hit(self, key: str, limit: int, window: int) -> tuple[bool, int]: ...


class MemoryBackend:
    def __init__(self) -> None:
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def hit(self, key: str, limit: int, window: int) -> tuple[bool, int]:
        now = time.monotonic()
        with self._lock:
            recent = [t for t in self._hits.get(key, []) if t > now - window]
            if len(recent) >= limit:
                self._hits[key] = recent
                return False, int(recent[0] + window - now) + 1
            recent.append(now)
            self._hits[key] = recent
            return True, 0

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


class RedisBackend:
    def __init__(self, client) -> None:
        self._client = client

    def hit(self, key: str, limit: int, window: int) -> tuple[bool, int]:
        redis_key = f"rl:{key}"
        pipe = self._client.pipeline()
        pipe.incr(redis_key)
        pipe.ttl(redis_key)
        count, ttl = pipe.execute()
        if ttl == -1:
            self._client.expire(redis_key, window)
            ttl = window
        if count > limit:
            return False, max(int(ttl), 1)
        return True, 0


_memory = MemoryBackend()


@lru_cache
def _redis_backend() -> RedisBackend | None:
    settings = get_settings()
    if settings.env == "test":
        return None
    try:
        import redis

        client = redis.Redis.from_url(settings.redis_url, socket_connect_timeout=1, socket_timeout=1)
        client.ping()
        return RedisBackend(client)
    except Exception:
        logger.warning("redis_unavailable_using_memory_rate_limiter")
        return None


def reset_rate_limits() -> None:
    _memory.reset()


def enforce_rate_limit(key: str, limit: int, window: int) -> None:
    backend = _redis_backend()
    try:
        allowed, retry_after = (backend or _memory).hit(key, limit, window)
    except Exception:
        logger.warning("rate_limit_backend_error_falling_back")
        allowed, retry_after = _memory.hit(key, limit, window)
    if not allowed:
        raise AppError(
            "RATE_LIMITED",
            "Too many requests. Please try again later.",
            429,
            details={"retry_after_seconds": retry_after},
            headers={"Retry-After": str(retry_after)},
        )


def client_ip(request: Request) -> str:
    # Behind a proxy, run uvicorn with --proxy-headers and a restricted
    # --forwarded-allow-ips so request.client reflects the real client.
    return request.client.host if request.client else "unknown"


def rate_limit(scope: str, limit_for: Callable[[Settings], int], window: int):
    """FastAPI dependency factory: per-IP limit read from settings at call time."""

    def dependency(request: Request) -> None:
        enforce_rate_limit(f"{scope}:{client_ip(request)}", limit_for(get_settings()), window)

    return dependency
