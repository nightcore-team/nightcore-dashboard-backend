from __future__ import annotations

from typing import Any

import sqlalchemy.types as types
from sqlalchemy import Dialect


class _BaseDiscordID(types.TypeDecorator[int]):
    impl = types.BigInteger

    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect):
        return int(value)

    def process_result_value(self, value: Any, dialect: Any) -> int | None:
        return value


class DiscordRoleID(_BaseDiscordID): ...


class DiscordChannelID(_BaseDiscordID): ...


class DiscordRoleNoAdmID(_BaseDiscordID): ...
