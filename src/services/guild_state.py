"""Guild state service implementation."""

import asyncio
from typing import Any

from src.api.schemas.configuration import (
    CONFIG_SCHEMA_MODEL_MAP,
    ChannelInfo,
    RoleInfo,
    ValidationContext,
)
from src.domain.interfaces.guild_state_repository import IGuildStateRepository
from src.infra.postgres.operations import (
    CONFIG_MODEL_MAP,
    ConfigType,
    get_or_create_specified_guild_config,
)
from src.infra.postgres.uow import UnitOfWork
from src.infra.redis.models import (
    ChannelCacheEntry,
    GuildCacheEntry,
    MemberCacheEntry,
    RoleCacheEntry,
)
from src.utils._enums import ConfigTypeEnum


class GuildStateService:
    def __init__(
        self, uow: UnitOfWork, guild_state_repo: IGuildStateRepository
    ) -> None:
        self._guild_state_repo = guild_state_repo
        self._uow = uow
        self._roles_cache: dict[int, dict[int, RoleCacheEntry]] = {}
        self._channels_cache: dict[int, dict[int, ChannelCacheEntry]] = {}

    async def _build_validation_context(
        self, guild_id: int
    ) -> ValidationContext:
        roles_list, channels_list = await asyncio.gather(
            self.get_roles(guild_id),
            self.get_channels(guild_id),
        )

        roles_dict = {
            int(role.id): RoleInfo(
                id=role.id,
                name=role.name,
                color=role.color,
                position=role.position,
                administrator=role.administrator,
            )
            for role in roles_list
        }

        channels_dict = {
            int(channel.id): ChannelInfo(
                id=channel.id,
                name=channel.name,
                type=channel.type,
            )
            for channel in channels_list
        }

        return ValidationContext(
            guild_id=guild_id,
            roles=roles_dict,
            channels=channels_dict,
        )

    async def get_roles(self, guild_id: int) -> list[RoleCacheEntry]:
        return await self._guild_state_repo.get_roles(guild_id)

    async def get_channels(self, guild_id: int) -> list[ChannelCacheEntry]:
        return await self._guild_state_repo.get_channels(guild_id)

    async def get_member(
        self, guild_id: int, user_id: int
    ) -> MemberCacheEntry | None:
        return await self._guild_state_repo.get_member(
            guild_id=guild_id, user_id=user_id
        )

    async def get_config(
        self, guild_id: int, config_type: ConfigTypeEnum
    ) -> ConfigType:
        type_ = CONFIG_MODEL_MAP.get(config_type)

        if type_ is None:
            raise ValueError("Unknown config type")

        async with self._uow.start() as session:
            return await get_or_create_specified_guild_config(
                session,
                config_type=type_,
                guild_id=guild_id,
            )

    async def get_guilds(self, guild_ids: list[str]) -> list[GuildCacheEntry]:
        return await self._guild_state_repo.get_guilds(guild_ids)

    async def update_config(
        self, guild_id: int, config_type: ConfigTypeEnum, data: dict[str, Any]
    ):
        type_ = CONFIG_MODEL_MAP.get(config_type)

        if type_ is None:
            raise ValueError("Unknown config type")

        pydantic_type = CONFIG_SCHEMA_MODEL_MAP.get(config_type)

        if pydantic_type is None:
            raise ValueError("Pydantic model not found for this config type")

        context = await self._build_validation_context(guild_id)
        validated_model = pydantic_type.model_validate(data, context=context)

        dump = validated_model.model_dump(exclude_unset=True)

        async with self._uow.start() as session:
            config = await get_or_create_specified_guild_config(
                session,
                config_type=type_,
                guild_id=guild_id,
            )

            for k, v in dump.items():
                setattr(config, k, v)
