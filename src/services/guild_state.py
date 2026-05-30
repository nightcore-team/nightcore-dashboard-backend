"""Guild state service implementation."""

from typing import Any, get_args, get_origin, get_type_hints

from fastapi import HTTPException, status

from src.api.schemas.configuration import ChannelID, ConfigModelType, RoleID
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

    async def _get_cached_channel(
        self, guild_id: int, channel_id: int
    ) -> ChannelCacheEntry | None:
        guild_channels = self._channels_cache.setdefault(guild_id, {})

        if channel_id in guild_channels:
            return guild_channels[channel_id]

        channel = await self._guild_state_repo.get_channel(
            guild_id, channel_id
        )
        if channel is not None:
            guild_channels[channel_id] = channel

        return channel

    async def _get_cached_role(
        self, guild_id: int, role_id: int
    ) -> RoleCacheEntry | None:
        guild_roles = self._roles_cache.setdefault(guild_id, {})

        if role_id in guild_roles:
            return guild_roles[role_id]

        role = await self._guild_state_repo.get_role(guild_id, role_id)
        if role is not None:
            guild_roles[role_id] = role

        return role

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

    async def _validate_discord_types(
        self, guild_id: int, dump: dict[str, Any], hints: dict[str, Any]
    ) -> bool:
        for field_name, value in dump.items():
            if value is None:
                continue

            annotation = hints.get(field_name)
            if annotation is None:
                continue

            args = get_args(annotation)
            inner = next((a for a in args if a is not type(None)), annotation)

            metadata = get_args(inner)
            is_list = get_origin(inner) is list

            if is_list:
                item_type = get_args(inner)[0] if get_args(inner) else None
                metadata = get_args(item_type) if item_type else ()

            if any(isinstance(m, ChannelID) for m in metadata):
                values = value if is_list else [value]
                for channel_id in values:
                    if (
                        await self._get_cached_channel(guild_id, channel_id)
                        is None
                    ):
                        return False

            elif any(isinstance(m, RoleID) for m in metadata):
                values = value if is_list else [value]
                for role_id in values:
                    if await self._get_cached_role(guild_id, role_id) is None:
                        return False

        return True

    async def update_config(
        self, guild_id: int, config_type: ConfigTypeEnum, data: ConfigModelType
    ):
        type_ = CONFIG_MODEL_MAP.get(config_type)

        if type_ is None:
            raise ValueError("Unknown config type")

        hints = get_type_hints(type(data), include_extras=True)
        dump = data.model_dump(exclude_unset=True)

        if not await self._validate_discord_types(guild_id, dump, hints):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неизвестный канал или роль в переданных данных",
            )

        async with self._uow.start() as session:
            config = await get_or_create_specified_guild_config(
                session,
                config_type=type_,
                guild_id=guild_id,
            )

            for k, v in dump.items():
                setattr(config, k, v)
