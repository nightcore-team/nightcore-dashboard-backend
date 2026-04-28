from src.domain.interfaces.base_redis_repo import IBaseRedisRepository


class IUserGuildsRepository(IBaseRedisRepository):
    async def get_user_guilds(self, user_id: int) -> list[str]: ...
