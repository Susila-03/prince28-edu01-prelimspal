"""App factory: build a fully wired FastAPI app from settings."""

import json
import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from prelimspal.api.errors import register_error_handlers
from prelimspal.api.middleware import RequestContextMiddleware
from prelimspal.api.routes import documents, health
from prelimspal.config import Settings, get_settings
from prelimspal.logging_setup import setup_logging
from prelimspal.store import RecordStore

logger = logging.getLogger("prelimspal")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    setup_logging(settings.log_level)

    store = RecordStore(settings.data_file)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            count = store.load()
            logger.info("records loaded", extra={"records": count})
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            logger.error("could not load records: %s", exc)

        yield

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    app.state.settings = settings
    app.state.store = store

    # Register request ID middleware
    app.add_middleware(RequestContextMiddleware)

    # Register error handlers
    register_error_handlers(app)

    # Documents API routes
    v1 = APIRouter(prefix="/v1")
    v1.include_router(documents.router)

    # Include application routers
    app.include_router(health.router)
    app.include_router(v1)

    return app
