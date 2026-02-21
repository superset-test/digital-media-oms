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

        # Register routers
        from app.controllers import tenants, users

        app.include_router(tenants.router, prefix="/v1", tags=["Tenants"])
        app.include_router(users.router, prefix="/v1", tags=["Users"])

        # TODO: Register remaining routers:
        # from app.controllers import agencies, advertisers, contacts
        # from app.controllers import placements, ad_units, rate_cards
        # from app.controllers import orders, line_items
        # app.include_router(agencies.router, prefix="/v1", tags=["Agencies"])
        # app.include_router(advertisers.router, prefix="/v1", tags=["Advertisers"])
        # app.include_router(contacts.router, prefix="/v1", tags=["Contacts"])
        # app.include_router(placements.router, prefix="/v1", tags=["Placements"])
        # app.include_router(ad_units.router, prefix="/v1", tags=["Ad Units"])
        # app.include_router(rate_cards.router, prefix="/v1", tags=["Rate Cards"])
        # app.include_router(orders.router, prefix="/v1", tags=["Orders"])
        # app.include_router(line_items.router, prefix="/v1", tags=["Line Items"])

        return app
