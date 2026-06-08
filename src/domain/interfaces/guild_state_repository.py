from src.domain.interfaces.base_redis_repo import IBaseRedisRepository
from src.infra.redis.models import (
    ChannelCacheEntry,
    GuildCacheEntry,
    MemberCacheEntry,
    RoleCacheEntry,
)


class IGuildStateRepository(IBaseRedisRepository):
    async def get_roles(self, guild_id: int) -> list[RoleCacheEntry]:
        """Return cached roles for a guild."""
        ...

    async def get_role(
        self, guild_id: int, role_id: int
    ) -> RoleCacheEntry | None:
        """Return a cached guild by ID."""

        ...

    async def get_channel(
        self, guild_id: int, channel_id: int
    ) -> ChannelCacheEntry | None:
        """Return a cached channel by ID."""

        ...

    async def get_channels(self, guild_id: int) -> list[ChannelCacheEntry]:
        """Return cached channels for a guild."""

        ...

    async def get_member(
        self, guild_id: int, user_id: int
    ) -> MemberCacheEntry | None:
        """Return cached member for a guild."""

        ...

    async def get_guilds(
        self, guild_ids: list[str]
    ) -> list[GuildCacheEntry]: ...

    async def get_roles_by_ids(
        self, role_ids: list[str]
    ) -> list[RoleCacheEntry]: ...
