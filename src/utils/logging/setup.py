"""Setup logging utilities for the application."""

import logging
import sys
from logging import Handler
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from src.utils.logging.config import DEFAULT_LOGGING_LEVEL_DICT, FORMATTER

_queue = Queue()  # pyright: ignore[reportUnknownVariableType]
_listener: QueueListener | None = None


def setup_logging() -> logging.Logger:
    """Set up and configure logging for the entire application."""
    handlers: list[Handler] = []

    root_logger = logging.getLogger()
    root_logger.setLevel(DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO))

    # --- Console handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO)
    )
    console_handler.setFormatter(FORMATTER)

    handlers.append(console_handler)

    # --- uvicorn ---
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.propagate = True

    # # --- redis ---
    # redis_logger = logging.getLogger("redis")
    # redis_logger.setLevel(logging.INFO)
    # redis_logger.propagate = True

    # --- Queue handler ---
    queue_handler = QueueHandler(queue=_queue)  # pyright: ignore[reportUnknownArgumentType]
    queue_handler.setLevel(
        DEFAULT_LOGGING_LEVEL_DICT.get("main", logging.INFO)
    )

    root_logger.addHandler(queue_handler)

    _listener = QueueListener(
        _queue,  # pyright: ignore[reportUnknownArgumentType]
        *handlers,
        respect_handler_level=True,
    )
    _listener.start()

    return root_logger


def stop_logging():
    """Stop the logging QueueListener and flush pending records."""

    _listener.stop() if _listener else None
