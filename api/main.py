"""TAQVO FastAPI application entry point."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_api_settings
from api.database import close_database


settings = get_api_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("taqvo.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""

    logger.info("TAQVO API starting...")
    yield
    await close_database()
    logger.info("TAQVO API stopped.")


app = FastAPI(
    title="TAQVO API",
    description="Backend API for TAQVO BOT and TAQVO PRO MAX.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://abdulhakiym.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Return API service information."""

    return {
        "service": "TAQVO API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Return a basic application health status."""

    return {
        "status": "healthy",
        "service": "taqvo-api",
    }
