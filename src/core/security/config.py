"""Defines the Config class for Jwt environment settings."""

from src.core.env import BaseEnvConfig


class Config(BaseEnvConfig):
    JWT_PUBLIC: str
    JWT_ALGORITHM: str
