"""Setup module for creating and configuring the FastAPI bot instance."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import router as api_router
from src.core._global import config

from .lifespan import lifespan


def create_fastapi() -> FastAPI:
    """Create and return an instance of the FastAPI application."""

    app = FastAPI(title="Nightcore API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            config.api.DASHBOARD_FRONTEND_URI,
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    app.state.config = config

    app.include_router(api_router)

    return app


def create_api_server() -> uvicorn.Server:
    """Create the uvicorn server for the FastAPI application."""

    app = create_fastapi()

    return uvicorn.Server(
        uvicorn.Config(
            app=app,
            host=config.api.API_HOST,
            port=config.api.API_PORT,
        )
    )


async def run_fastapi(server: uvicorn.Server) -> None:
    """Run the FastAPI application in the current event loop."""

    await server.serve()


def stop_fastapi(server: uvicorn.Server) -> None:
    """Gracefully stop the FastAPI server."""

    server.should_exit = True
