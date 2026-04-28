"""Repository for storing Discord guild state in Redis."""

import logging
from typing import cast

from redis.asyncio import Redis

from src.infra.redis.models import (
    ChannelCacheEntry,
    GuildCacheEntry,
    MemberCacheEntry,
    RoleCacheEntry,
)
from src.infra.redis.repository.base import BaseRepository

logger = logging.getLogger(__name__)

__all__ = ("GuildStateRepository",)


class GuildStateRepository(BaseRepository):
    """Persist and retrieve Discord guild state from Redis."""

    def __init__(self, redis: Redis):
        super().__init__(redis)

    @property
    def _guilds_key(self) -> str:
        return "nightcore:discord_state:guilds"

    def _roles_key(self, guild_id: int) -> str:
        return f"nightcore:discord_state:guild:{guild_id}:roles"

    def _channels_key(self, guild_id: int) -> str:
        return f"nightcore:discord_state:guild:{guild_id}:channels"

    def _members_key(self, guild_id: int) -> str:
        return f"nightcore:discord_state:guild:{guild_id}:members"

    async def get_roles(self, guild_id: int) -> list[RoleCacheEntry]:
        """Return cached roles for a guild."""

        values = await self.redis.hvals(self._roles_key(guild_id))  # type: ignore
        values = cast(list[str], values)

        roles = [self._loads(value, RoleCacheEntry) for value in values]

        return sorted(roles, key=lambda role: role.position)

    async def get_role(
        self, guild_id: int, role_id: int
    ) -> RoleCacheEntry | None:
        """Return a cached guild by ID."""

        value = await self.redis.hget(self._roles_key(guild_id), str(role_id))  # type: ignore
        value = cast(str | None, value)

        if value is None:
            return None

        return self._loads(value, RoleCacheEntry)

    async def get_channels(self, guild_id: int) -> list[ChannelCacheEntry]:
        """Return cached channels for a guild."""

        values = await self.redis.hvals(self._channels_key(guild_id))  # type: ignore
        values = cast(list[str], values)

        channels = [self._loads(value, ChannelCacheEntry) for value in values]

        return sorted(
            channels,
            key=lambda channel: (channel.type, channel.name.casefold()),
        )

    async def get_channel(
        self, guild_id: int, channel_id: int
    ) -> ChannelCacheEntry | None:
        """Return a cached channel by ID."""

        value = await self.redis.hget(  # type: ignore
            self._channels_key(guild_id), str(channel_id)
        )
        value = cast(str | None, value)

        if value is None:
            return None

        return self._loads(value, ChannelCacheEntry)

    async def get_member(
        self, guild_id: int, user_id: int
    ) -> MemberCacheEntry | None:
        """Return cached member for a guild."""

        value = await self.redis.hget(  # type: ignore
            self._members_key(guild_id), str(user_id)
        )
        value = cast(str | None, value)

        if value is None:
            return None

        return self._loads(value, MemberCacheEntry)

    async def get_guilds(self, guild_ids: list[str]) -> list[GuildCacheEntry]:
        """Return cached guilds."""

        result: list[GuildCacheEntry] = []

        raw_guilds = await self.redis.hmget(self._guilds_key, guild_ids)  # type: ignore

        for raw_guild in raw_guilds:  # type: ignore
            if raw_guild is None:
                continue

            guild = self._loads(raw_guild, GuildCacheEntry)  # type: ignore

            result.append(guild)

        return result
