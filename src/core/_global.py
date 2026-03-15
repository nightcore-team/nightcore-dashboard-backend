"""The module provides a global config for composing all configs and convenient use throughout the project."""  # noqa: E501

from functools import cached_property

from src.api.config import Config as ApiConfig
from src.infra.redis.config import Config as RedisConfig


class Config:
    @cached_property
    def api(self) -> ApiConfig:
        """Return the API configuration settings."""
        return ApiConfig()  # type: ignore

    @cached_property
    def redis(self) -> RedisConfig:
        """Return the Redis configuration settings."""
        return RedisConfig()  # type: ignore


config = Config()
