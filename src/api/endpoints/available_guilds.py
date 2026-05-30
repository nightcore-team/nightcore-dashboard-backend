"""Available-guilds related endpoints."""

from fastapi import status
from fastapi.routing import APIRouter

from ..dependencies import (
    AccessServiceDependency,
    GuildStateServiceDependency,
    UserIdDependency,
)
from ..schemas.guild import GuildInfoSchema

router = APIRouter(
    prefix="/available-guilds", tags=["available-guilds endpoint"]
)


@router.get(
    "",
    response_model=list[GuildInfoSchema],
    status_code=status.HTTP_200_OK,
)
async def get_available_guilds(
    user_id: UserIdDependency,
    access_service: AccessServiceDependency,
    guild_state_service: GuildStateServiceDependency,
):
    guild_ids = await access_service.get_user_guilds(user_id)

    return await guild_state_service.get_guilds(guild_ids)
