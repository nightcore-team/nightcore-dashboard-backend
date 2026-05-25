"""Access service implementation."""

from src.domain.interfaces.user_guilds_repository import IUserGuildsRepository
from src.infra.postgres.models._enums import ConfigTypeEnum
from src.infra.postgres.operations import (
    get_available_guild_configs,
    has_guild_config_access,
)
from src.infra.postgres.uow import UnitOfWork
from src.infra.redis.models import MemberCacheEntry


class AccessService:
    def __init__(
        self,
        user_guilds_repo: IUserGuildsRepository,
        uow: UnitOfWork,
    ) -> None:
        self._user_guilds_repo = user_guilds_repo
        self._uow = uow

    async def get_user_guilds(self, user_id: int) -> list[str]:
        """Get the guilds that the user belongs to."""

        return await self._user_guilds_repo.get_user_guilds(user_id)

    async def get_available_configurations(
        self, guild_id: int, member: MemberCacheEntry
    ) -> list[str]:
        """Get user-accessible configs for a specific guild."""

        async with self._uow.start() as session:
            return await get_available_guild_configs(
                session, guild_id=guild_id, roles=member.roles
            )

    async def has_config_access(
        self,
        guild_id: int,
        member: MemberCacheEntry,
        config_type: ConfigTypeEnum,
    ) -> bool:
        """Check whether the user has access to a specific config in a guild."""  # noqa: E501
        if config_type == ConfigTypeEnum.ACCESS:
            return member.administrator

        async with self._uow.start() as session:
            return await has_guild_config_access(
                session,
                guild_id=guild_id,
                roles=member.roles,
                config_type=config_type,
            )
