"""Main entry point for the Nightcore Dashboard Backend."""

import asyncio
import contextlib
import signal

from src.setup import create_api_server
from src.utils.logging.setup import setup_logging, stop_logging


async def main() -> None:
    """Main function to start the Nightcore Dashboard Backend."""
    # Set up logging
    logger = setup_logging()

    # Create API Server
    server = create_api_server()
    server_task = asyncio.create_task(server.serve())

    loop = asyncio.get_running_loop()

    def shutdown() -> None:
        logger.info("Shutdown signal received. Stopping API server...")
        server.should_exit = True

    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)

    logger.info("Starting Nightcore Dashboard Backend API...")
    try:
        await server_task
    except asyncio.CancelledError:
        logger.info("Server task cancelled.")
    except Exception as e:
        logger.error("Error occurred: %s", e)
    finally:
        # Cleanup resources
        logger.info("Cleaning up resources...")
        logger.info("Nightcore Dashboard Backend has been stopped.")
        stop_logging()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
