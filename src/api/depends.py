"""API dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from src.infra.redis.repository import GuildStateRepository


def get_guild_state_repository(request: Request) -> GuildStateRepository:
    """Get the Redis-backed guild state repository."""

    guild_state_repository = getattr(
        request.app.state,
        "guild_state_repository",
        None,
    )
    if guild_state_repository is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Guild state repository is unavailable.",
        )

    return guild_state_repository


async def get_ready_guild_state_repository(
    guild_state_repository: Annotated[
        GuildStateRepository,
        Depends(get_guild_state_repository),
    ],
) -> GuildStateRepository:
    """Get the Redis-backed guild state repository after readiness check."""

    if not await guild_state_repository.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot cache is not ready yet.",
        )

    return guild_state_repository


GuildStateRepositoryDependency = Annotated[
    GuildStateRepository,
    Depends(get_ready_guild_state_repository),
]
