from typing import Final, Union

from sqlalchemy import Boolean, select, type_coerce
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.infra.postgres.models import (
    GuildAccessConfig,
    GuildClansConfig,
    GuildEconomyConfig,
    GuildForumConfig,
    GuildInfomakerConfig,
    GuildLevelsConfig,
    GuildLoggingConfig,
    GuildModerationConfig,
    GuildMultipliersConfig,
    GuildNotificationsConfig,
    GuildPrivateChannelsConfig,
    GuildProposalsConfig,
    GuildRoleRequestConfig,
    GuildRulesConfig,
    GuildTicketsConfig,
)
from src.utils._enums import ConfigTypeEnum

ConfigType = Union[  # noqa: UP007
    GuildClansConfig
    | GuildEconomyConfig
    | GuildLevelsConfig
    | GuildLoggingConfig
    | GuildModerationConfig
    | GuildPrivateChannelsConfig
    | GuildNotificationsConfig
    | GuildTicketsConfig
    | GuildInfomakerConfig
    | GuildAccessConfig
    | GuildRulesConfig
    | GuildMultipliersConfig
    | GuildProposalsConfig
    | GuildRoleRequestConfig
    | GuildForumConfig
]

CONFIG_MODEL_MAP: dict[ConfigTypeEnum, type[ConfigType]] = {
    ConfigTypeEnum.ECONOMY: GuildEconomyConfig,
    ConfigTypeEnum.LEVELS: GuildLevelsConfig,
    ConfigTypeEnum.CLANS: GuildClansConfig,
    ConfigTypeEnum.PRIVATE_CHANNELS: GuildPrivateChannelsConfig,
    ConfigTypeEnum.MODERATION: GuildModerationConfig,
    ConfigTypeEnum.NOTIFICATIONS: GuildNotificationsConfig,
    ConfigTypeEnum.INFOMAKER: GuildInfomakerConfig,
    ConfigTypeEnum.FORUM: GuildForumConfig,
    ConfigTypeEnum.RULES: GuildRulesConfig,
    ConfigTypeEnum.PROPOSALS: GuildProposalsConfig,
    ConfigTypeEnum.MULTIPLERS: GuildMultipliersConfig,
    ConfigTypeEnum.ROLE_REQUEST: GuildRoleRequestConfig,
    ConfigTypeEnum.TICKETS: GuildTicketsConfig,
    ConfigTypeEnum.LOGGING: GuildLoggingConfig,
    ConfigTypeEnum.ACCESS: GuildAccessConfig,
}

_ACCESS_COLUMNS: Final[
    dict[ConfigTypeEnum, InstrumentedAttribute[list[int] | None]]
] = {
    ConfigTypeEnum.LOGGING: GuildAccessConfig.logging_config_access_roles_ids,
    ConfigTypeEnum.ECONOMY: GuildAccessConfig.economy_config_access_roles_ids,
    ConfigTypeEnum.LEVELS: GuildAccessConfig.levels_config_access_roles_ids,
    ConfigTypeEnum.CLANS: GuildAccessConfig.clans_config_access_roles_ids,
    ConfigTypeEnum.PRIVATE_CHANNELS: GuildAccessConfig.private_channels_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.MODERATION: GuildAccessConfig.moderation_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.NOTIFICATIONS: GuildAccessConfig.notifications_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.INFOMAKER: GuildAccessConfig.infomaker_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.FORUM: GuildAccessConfig.forum_config_access_roles_ids,
    ConfigTypeEnum.RULES: GuildAccessConfig.rules_config_access_roles_ids,
    ConfigTypeEnum.PROPOSALS: GuildAccessConfig.proposal_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.MULTIPLERS: GuildAccessConfig.multiplers_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.ROLE_REQUEST: GuildAccessConfig.org_roles_config_access_roles_ids,  # noqa: E501
    ConfigTypeEnum.TICKETS: GuildAccessConfig.tickets_config_access_roles_ids,
}


async def get_or_create_specified_guild_config(
    session: AsyncSession,
    *,
    config_type: type[ConfigType],
    guild_id: int,
) -> ConfigType:
    """Get the guild configuration from the database."""

    stmt = select(config_type).where(config_type.guild_id == guild_id)
    result = await session.execute(stmt)

    if (config := result.scalar_one_or_none()) is None:
        new_config = config_type(guild_id=guild_id)
        session.add(new_config)
        await session.flush()

        return new_config

    return config


async def get_available_guild_configs(
    session: AsyncSession, *, guild_id: int, roles: list[int]
) -> list[str]:

    select_clauses = [
        array(roles).overlap(column).label(config_type.value)
        for config_type, column in _ACCESS_COLUMNS.items()
    ]

    stmt = select(*select_clauses).where(
        GuildAccessConfig.guild_id == guild_id
    )

    result = await session.execute(stmt)
    row = result.mappings().first()

    if row is None:
        return []

    return [key for key, value in row.items() if value]


async def has_guild_config_access(
    session: AsyncSession,
    *,
    guild_id: int,
    roles: list[int],
    config_type: ConfigTypeEnum,
) -> bool:
    target_column = _ACCESS_COLUMNS.get(config_type)
    if target_column is None:
        raise ValueError(f"Unknown config type: {config_type}")

    stmt = select(
        type_coerce(target_column.op("&&")(array(roles)), Boolean)
    ).where(GuildAccessConfig.guild_id == guild_id)

    return bool(await session.scalar(stmt))
