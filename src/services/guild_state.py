"""Guild state service implementation."""

import typing
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect

from src.domain.interfaces.guild_state_repository import IGuildStateRepository
from src.infra.postgres.models._enums import ConfigTypeEnum
from src.infra.postgres.models._types import (
    DiscordChannelID,
    DiscordRoleID,
    DiscordRoleNoAdmID,
)
from src.infra.postgres.operations import (
    CONFIG_MODEL_MAP,
    get_or_create_specified_guild_config,
)
from src.infra.postgres.uow import UnitOfWork
from src.infra.redis.models import (
    ChannelCacheEntry,
    GuildCacheEntry,
    MemberCacheEntry,
    RoleCacheEntry,
)


class GuildStateService:
    def __init__(
        self, uow: UnitOfWork, guild_state_repo: IGuildStateRepository
    ) -> None:
        self._guild_state_repo = guild_state_repo
        self._uow = uow

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
    ) -> dict[str, Any]:
        type_ = CONFIG_MODEL_MAP.get(config_type)

        if type_ is None:
            raise ValueError("Unknown config type")

        async with self._uow.start() as session:
            config = await get_or_create_specified_guild_config(
                session,
                config_type=type_,
                guild_id=guild_id,
            )

        return jsonable_encoder(config, exclude={"id", "guild_id"})

    async def get_guilds(self, guild_ids: list[str]) -> list[GuildCacheEntry]:
        return await self._guild_state_repo.get_guilds(guild_ids)

    def _is_base_type(self, value: Any, expected_type: type[Any]) -> bool:
        if issubclass(expected_type, int) and isinstance(value, int):
            return True

        if issubclass(expected_type, bool) and isinstance(value, bool):  # noqa: SIM103
            return True

        return False

    async def _is_discord_role_type(
        self, guild_id: int, value: Any, expected_type: type[Any]
    ) -> bool:
        if not isinstance(value, str):
            return False

        try:
            value = int(value)
        except ValueError:
            return False

        if issubclass(expected_type, DiscordRoleNoAdmID):
            role = await self._guild_state_repo.get_role(
                guild_id=guild_id, role_id=value
            )

            if role is None:
                return False

            return not role.administrator

        if (  # noqa: SIM103
            issubclass(expected_type, DiscordRoleID)
            and (
                await self._guild_state_repo.get_role(
                    guild_id=guild_id, role_id=value
                )
                is None
            )
        ):
            return False

        return True

    async def _is_discord_channel_type(
        self, guild_id: int, value: Any, expected_type: type[Any]
    ) -> bool:
        if not isinstance(value, str):
            return False

        try:
            value = int(value)
        except ValueError:
            return False

        if issubclass(expected_type, DiscordChannelID) and (  # noqa: SIM103
            await self._guild_state_repo.get_channel(
                guild_id=guild_id, channel_id=value
            )
            is None
        ):
            return False

        return True

    async def _validate_single_value(
        self, guild_id: int, value: Any, expected_type: type[Any]
    ) -> bool:
        if self._is_base_type(expected_type=expected_type, value=value):
            return True

        if await self._is_discord_role_type(
            guild_id=guild_id, value=value, expected_type=expected_type
        ):
            return True

        if await self._is_discord_channel_type(  # noqa: SIM103
            guild_id=guild_id, value=value, expected_type=expected_type
        ):
            return True

        return False

    def _validate_array_type(
        self, array_type: type[Any], value: list[Any]
    ) -> bool:
        if (
            issubclass(array_type, DiscordRoleID)
            or issubclass(array_type, DiscordRoleNoAdmID)
        ) and len(value) > 250:
            return False

        if issubclass(array_type, DiscordChannelID) and len(value) > 500:  # noqa: SIM103
            return False

        return True

    async def _validate_array(
        self, guild_id: int, array: list[Any], expected_type: type[list[Any]]
    ) -> bool:

        for value in array:
            result = await self._validate_single_value(
                guild_id=guild_id, value=value, expected_type=expected_type
            )

            if not result:
                return False

        return True

    async def _validate_type(
        self, guild_id: int, value: Any, expected_type: type[Any]
    ) -> bool:

        if issubclass(expected_type, list) and isinstance(value, list):
            args = typing.get_args(expected_type)

            if len(args) != 1:
                return False

            list_type = args[0]

            result = self._validate_array_type(
                array_type=list_type,
                value=value,  # pyright: ignore[reportUnknownArgumentType]
            )

            if not result:
                return False

            return await self._validate_array(
                guild_id=guild_id,
                array=value,  # pyright: ignore[reportUnknownArgumentType]
                expected_type=expected_type,  # pyright: ignore[reportUnknownArgumentType]
            )

        if issubclass(expected_type, list):
            return False

        return await self._validate_single_value(
            guild_id=guild_id,
            value=value,
            expected_type=expected_type,
        )

    async def update_config(
        self, guild_id: int, config_type: ConfigTypeEnum, data: dict[str, Any]
    ):
        type_ = CONFIG_MODEL_MAP.get(config_type)

        if type_ is None:
            raise ValueError("Unknown config type")

        columns = inspect(type_).columns

        valid_keys: dict[str, Any] = {}

        for column in columns:
            if column.key in ["id", "guild_id"]:
                continue

            if (value := data.get(column.key)) is None:
                continue

            if value is None and column.nullable:
                valid_keys[column.key] = None
                continue

            column_type = column.type.python_type

            if not await self._validate_type(
                guild_id=guild_id, value=value, expected_type=column_type
            ):
                continue

            valid_keys[column.key] = value

        if len(valid_keys) < 1:
            return

        async with self._uow.start() as session:
            config = await get_or_create_specified_guild_config(
                session,
                config_type=type_,
                guild_id=guild_id,
            )

            for k, v in valid_keys.items():
                setattr(config, k, v)
