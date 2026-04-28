"""Repository for storing Discord guild state in Redis."""

import logging
from typing import cast

from redis.asyncio import Redis

from src.infra.redis.repository.base import BaseRepository

logger = logging.getLogger(__name__)

__all__ = ("UserGuildsRepository",)


class UserGuildsRepository(BaseRepository):
    """Persist and retrieve Discord guild state from Redis."""

    def __init__(self, redis: Redis):
        super().__init__(redis)

    def _user_guilds_key(self, user_id: int) -> str:
        return f"nightcore:discord_state:user:{user_id}:guilds"

    async def get_user_guilds(self, user_id: int) -> list[str]:
        res = await self.redis.smembers(self._user_guilds_key(user_id))  # type: ignore

        res = cast(set[str], res)

        return list(res)
