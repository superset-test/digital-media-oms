"""FastAPI application server."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.postgres import PostgresProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    postgres = PostgresProvider()
    await postgres.init()
    yield
    # Shutdown
    await postgres.shutdown()


class AppServer:
    """Application server factory."""

    @staticmethod
    def get_app() -> FastAPI:
        """Create and configure FastAPI application."""
        app = FastAPI(
            title="Backend API",
            description="FastAPI backend service",
            version="0.1.0",
            lifespan=lifespan,
        )

        # CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173", "http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Health check endpoint
        @app.get("/health", tags=["Health"])
        async def health_check():
            return {"status": "healthy"}

        # Register routers here
        # Example:
        # from app.controllers import users
        # app.include_router(users.router, prefix="/v1", tags=["Users"])

        return app
