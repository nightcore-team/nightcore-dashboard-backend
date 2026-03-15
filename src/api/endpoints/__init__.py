from fastapi import APIRouter

from .guild import router as guild_router

router = APIRouter(prefix="/api")
router.include_router(guild_router)
