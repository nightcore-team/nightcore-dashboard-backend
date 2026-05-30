"""API schemas."""

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

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
