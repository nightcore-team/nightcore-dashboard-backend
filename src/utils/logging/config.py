"""Configuration constants for logging setup."""

from logging import INFO, Formatter
from typing import Final

DEFAULT_LOGGING_LEVEL_DICT: Final[dict[str, int]] = {
    "main": INFO,
    "sqlalchemy": INFO,
    "sqlalchemy.engine": INFO,
    "sqlalchemy.pool": INFO,
    "asyncio": INFO,
    "redis": INFO,
    "uvicorn": INFO,
}

FORMATTER = Formatter(
    "%(asctime)s ~ %(name)-8s ~ %(levelname)-2s ~ %(message)s"
)
