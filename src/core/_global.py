"""The module provides a global config for composing all configs and convenient use throughout the project."""  # noqa: E501

from functools import cached_property

from src.api.config import Config as ApiConfig
from src.core.security.config import Config as JwtConfig
from src.infra.postgres.config import Config as PostgresConfig
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

    @cached_property
    def postgres(self) -> PostgresConfig:
        """Return the Postgres configuration settings."""
        return PostgresConfig()

    @cached_property
    def jwt(self) -> JwtConfig:
        """Return the Jwt configuration settings."""
        return JwtConfig()  # type: ignore


config = Config()
