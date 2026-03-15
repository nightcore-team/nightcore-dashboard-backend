"""Guild related endpoints."""

from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from ..depends import GuildStateRepositoryDependency
from ..schemas import ChannelInfoSchema, GuildInfoSchema, RoleInfoSchema

router = APIRouter(prefix="/guilds", tags=["Guild Endpoints"])


@router.get(
    "/", response_model=list[GuildInfoSchema], status_code=status.HTTP_200_OK
)
async def get_bot_guilds(
    guild_state_repository: GuildStateRepositoryDependency,
):
    """Get a list of guilds the bot is in."""

    return await guild_state_repository.get_guilds()


@router.get(
    "/{guild_id}",
    response_model=GuildInfoSchema,
    status_code=status.HTTP_200_OK,
)
async def get_guild_info(
    guild_id: int,
    guild_state_repository: GuildStateRepositoryDependency,
):
    """Get cached guild details, including roles and channels."""

    guild = await guild_state_repository.get_guild(str(guild_id))
    if guild is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guild not found.",
        )

    return guild


@router.get(
    "/{guild_id}/roles",
    response_model=list[RoleInfoSchema],
    status_code=status.HTTP_200_OK,
)
async def get_guild_roles(
    guild_id: int,
    guild_state_repository: GuildStateRepositoryDependency,
):
    """Get roles for a specific guild."""

    guild = await guild_state_repository.get_guild(str(guild_id))
    if guild is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guild not found.",
        )

    return await guild_state_repository.get_roles(str(guild_id))


@router.get(
    "/{guild_id}/channels",
    response_model=list[ChannelInfoSchema],
    status_code=status.HTTP_200_OK,
)
async def get_guild_channels(
    guild_id: int,
    guild_state_repository: GuildStateRepositoryDependency,
):
    """Get channels for a specific guild."""

    guild = await guild_state_repository.get_guild(str(guild_id))
    if guild is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guild not found.",
        )

    return await guild_state_repository.get_channels(str(guild_id))
