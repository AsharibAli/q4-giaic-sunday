"""GIAIC DBMS - FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .models.upload import HealthResponse
from .routers.upload import router as upload_router
from .services.storage import get_storage_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting GIAIC DBMS API")
    settings = get_settings()
    logger.info(f"CORS origins: {settings.cors_origins_list}")
    yield
    logger.info("Shutting down GIAIC DBMS API")


app = FastAPI(
    title="GIAIC DBMS File Upload API",
    description="API for uploading images and videos to Cloudflare R2 storage",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """
    Check service health including R2 connectivity.

    Returns health status and timestamp.
    """
    storage = get_storage_service()
    r2_connected = storage.health_check()

    return HealthResponse(
        status="healthy" if r2_connected else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        services={"r2": "connected" if r2_connected else "disconnected"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
