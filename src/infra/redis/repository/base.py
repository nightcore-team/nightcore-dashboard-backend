"""Base repository for storing objects in Redis."""

import asyncio
import json
import logging
from typing import TypeVar

from redis.asyncio import Redis
from redis.exceptions import ConnectionError, TimeoutError

from src.core._global import config

logger = logging.getLogger(__name__)

T = TypeVar("T")

ModelT = TypeVar("ModelT")


class BaseRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    @property
    def _ready_key(self) -> str:
        return "nightcore:discord_state:ready"

    async def connect(self) -> None:
        """Ensure the Redis connection is available."""
        attempts = max(1, config.redis.REDIS_CONNECT_RETRIES)
        delay_seconds = max(
            0.0,
            config.redis.REDIS_CONNECT_RETRY_DELAY_SECONDS,
        )

        for attempt in range(1, attempts + 1):
            try:
                await self.redis.ping()  # type: ignore
                if attempt > 1:
                    logger.info(
                        "[redis] Connection restored on attempt %d/%d",
                        attempt,
                        attempts,
                    )
                return
            except (ConnectionError, TimeoutError) as exc:
                if attempt == attempts:
                    logger.error(
                        "[redis] Failed to connect after %d attempts",
                        attempts,
                    )
                    raise

                logger.warning(
                    "[redis] Connect attempt %d/%d failed: %s. "
                    "Retrying in %.2fs",
                    attempt,
                    attempts,
                    exc,
                    delay_seconds,
                )
                await asyncio.sleep(delay_seconds)

    async def close(self) -> None:
        """Close the Redis connection."""

        await self.redis.aclose()

    async def is_ready(self) -> bool:
        """Return whether the cached Discord state is ready."""

        return await self.redis.get(self._ready_key) == "1"

    def _loads(self, value: str, type_: type[T]) -> T:
        return type_(**json.loads(value))
