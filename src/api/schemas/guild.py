"""API schemas."""

from typing import Any

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

from src.infra.postgres.models._enums import ConfigTypeEnum

from ..types import DiscordId


class Base(BaseModel):
    """Base schema."""

    model_config = SettingsConfigDict(extra="ignore")


class GuildInfoSchema(Base):
    """Schema for a guild."""

    id: DiscordId
    name: str


class RoleInfoSchema(Base):
    """Schema for a guild role."""

    id: DiscordId
    name: str
    color: str
    position: int
    administrator: bool


class ChannelInfoSchema(Base):
    """Schema for a guild channel."""

    id: DiscordId
    name: str
    type: str


class ConfigUpdateBody(Base):
    config_type: ConfigTypeEnum
    data: dict[str, Any]
