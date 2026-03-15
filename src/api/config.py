"""Defines the Config class for database environment settings."""

from src.core.env import BaseEnvConfig


class Config(BaseEnvConfig):
    API_HOST: str
    API_PORT: int
