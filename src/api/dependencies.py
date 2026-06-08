"""API dependencies."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from src.core.security.jwt import JWTTokenService
from src.infra.postgres.uow import UnitOfWork
from src.infra.redis.repository import (
    GuildStateRepository,
    UserGuildsRepository,
)
from src.services.access import AccessService
from src.services.guild_state import GuildStateService


def get_jwt_token_service(request: Request) -> JWTTokenService:
    return JWTTokenService(request.app.state.config.jwt)


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


def get_user_guilds_repository(request: Request) -> UserGuildsRepository:
    """Get the Redis-backed user guilds repository."""

    user_guilds_repository = getattr(
        request.app.state,
        "user_guilds_repository",
        None,
    )
    if user_guilds_repository is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User guilds repository is unavailable.",
        )

    return user_guilds_repository


async def get_ready_user_guilds_repository(
    user_guilds_repository: Annotated[
        UserGuildsRepository,
        Depends(get_user_guilds_repository),
    ],
) -> UserGuildsRepository:
    """Get the Redis-backed user guilds repository after readiness check."""

    if not await user_guilds_repository.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Bot cache is not ready yet.",
        )

    return user_guilds_repository


async def get_uow(request: Request) -> UnitOfWork:
    uow = getattr(
        request.app.state,
        "uow",
        None,
    )

    if uow is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="UnitOfWork is unavailable.",
        )

    return uow


def get_user_id(
    request: Request,
    jwt_token_service: Annotated[
        JWTTokenService,
        Depends(get_jwt_token_service),
    ],
) -> int:
    token = request.headers.get("Authorization")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token not found.",
        )

    payload = jwt_token_service.decode(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token.",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bad token payload.",
        )

    try:
        return int(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Bad token payload.",
        ) from e


def get_access_service(
    user_guilds_repository: Annotated[
        UserGuildsRepository,
        Depends(get_ready_user_guilds_repository),
    ],
    guild_state_repository: Annotated[
        GuildStateRepository,
        Depends(get_ready_guild_state_repository),
    ],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> AccessService:
    return AccessService(
        user_guilds_repo=user_guilds_repository,  # type: ignore
        guild_state_repo=guild_state_repository,  # type: ignore
        uow=uow,
    )


def get_guild_state_service(
    guild_state_repository: Annotated[
        GuildStateRepository,
        Depends(get_ready_guild_state_repository),
    ],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> GuildStateService:
    return GuildStateService(uow=uow, guild_state_repo=guild_state_repository)  # type: ignore


UserIdDependency = Annotated[int, Depends(get_user_id)]

GuildStateServiceDependency = Annotated[
    GuildStateService, Depends(get_guild_state_service)
]
AccessServiceDependency = Annotated[AccessService, Depends(get_access_service)]
