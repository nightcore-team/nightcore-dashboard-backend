from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.postgres.models import (
    GuildClansConfig,
    GuildEconomyConfig,
    GuildInfomakerConfig,
    GuildLevelsConfig,
    GuildLoggingConfig,
    GuildMetaConfig,
    GuildModerationConfig,
    GuildNotificationsConfig,
    GuildPrivateChannelsConfig,
    GuildTicketsConfig,
    MainGuildConfig,
)
from src.infra.postgres.models._enums import MetaConfigAccessTypeEnum

GuildT = TypeVar(
    "GuildT",
    GuildClansConfig,
    GuildEconomyConfig,
    GuildLevelsConfig,
    GuildLoggingConfig,
    GuildModerationConfig,
    GuildPrivateChannelsConfig,
    GuildNotificationsConfig,
    GuildTicketsConfig,
    MainGuildConfig,
    GuildInfomakerConfig,
    GuildMetaConfig,
)


class ConfigRepository:
    async def get_specified_guild_config(
        self,
        session: AsyncSession,
        *,
        config_type: type[GuildT],
        guild_id: int,
    ) -> GuildT | None:
        """Get the guild configuration from the database."""
        stmt = select(config_type).where(config_type.guild_id == guild_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_available_guild_configs(
        self, session: AsyncSession, guild_id: int, roles: list[int]
    ) -> list[str]:
        stmt = select(
            array(roles)
            .overlap(GuildMetaConfig.other_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.OTHER.value),
            array(roles)
            .overlap(GuildMetaConfig.logging_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.LOGGING.value),
            array(roles)
            .overlap(GuildMetaConfig.economy_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.ECONOMY.value),
            array(roles)
            .overlap(GuildMetaConfig.levels_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.LEVELS.value),
            array(roles)
            .overlap(GuildMetaConfig.clans_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.CLANS.value),
            array(roles)
            .overlap(GuildMetaConfig.private_channels_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.PRIVATE_CHANNELS.value),
            array(roles)
            .overlap(GuildMetaConfig.moderation_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.MODERATION.value),
            array(roles)
            .overlap(GuildMetaConfig.notifications_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.NOTIFICATIONS.value),
            array(roles)
            .overlap(GuildMetaConfig.infomaker_config_access_roles_ids)
            .label(MetaConfigAccessTypeEnum.INFOMAKER.value),
        ).where(GuildMetaConfig.guild_id == guild_id)

        result = await session.execute(stmt)
        row = result.first()

        if row is None:
            return []

        return [key for key, value in row.items() if value]
