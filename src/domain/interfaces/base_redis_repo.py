from typing import Protocol


class IBaseRedisRepository(Protocol):
    async def is_ready(self) -> bool:
        """Return whether the cached Discord state is ready."""

        ...
