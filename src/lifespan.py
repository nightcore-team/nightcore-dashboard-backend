"""Lifespan functions for managing the application lifecycle."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from src.infra.redis.client import create_redis_client
from src.infra.redis.repository import GuildStateRepository

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator[None]:
    """Async context manager for managing the lifespan of the FastAPI application."""  # noqa: E501

    redis_client = create_redis_client()
    guild_state_repository = GuildStateRepository(redis_client)

    logger.info("Connecting to Redis...")
    await guild_state_repository.connect()
    logger.info("Connected to Redis.")

    app.state.guild_state_repository = guild_state_repository

    yield

    await guild_state_repository.close()
    logger.info("Redis connection closed.")
