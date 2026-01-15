from fastapi import APIRouter

from app.core.metadata import APP_NAME, APP_VERSION

router = APIRouter()


@router.get("/")
def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "docs": "/docs",
    }

