from typing import Any, Protocol


class IJWTTokenService(Protocol):
    def decode(self, token: str) -> dict[str, Any] | None:
        """Verify a JWT token and return its payload if valid, otherwise None."""  # noqa: E501
