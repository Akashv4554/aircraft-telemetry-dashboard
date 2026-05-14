"""Redis client placeholder — lazy connection, optional in all environments."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flask import Flask

logger = logging.getLogger(__name__)


class RedisExtension:
    """Flask extension pattern for optional Redis."""

    def __init__(self) -> None:
        self._client: Any | None = None
        self._app: Flask | None = None

    def init_app(self, app: Flask) -> None:
        self._app = app
        app.extensions["redis"] = self
        url = app.config.get("REDIS_URL") or ""
        if not url:
            logger.info("REDIS_URL not set - Redis features disabled")
            return
        try:
            import redis  # type: ignore[import-untyped]

            self._client = redis.from_url(
                url,
                decode_responses=True,
                socket_connect_timeout=5,
            )
            self._client.ping()
            logger.info("Redis connected")
        except Exception as exc:  # noqa: BLE001 — surface misconfiguration without crashing app
            logger.warning("Redis unavailable (%s); continuing without cache", exc)
            self._client = None

    @property
    def client(self) -> Any | None:
        return self._client

    def ping(self) -> bool:
        if self._client is None:
            return False
        try:
            return bool(self._client.ping())
        except Exception:  # noqa: BLE001
            return False
