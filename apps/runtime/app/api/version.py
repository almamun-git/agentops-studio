from fastapi import APIRouter

from app.core.metadata import API_VERSION, APP_VERSION

router = APIRouter()


@router.get("/version")
def get_version():
    """Get API version information."""
    return {
        "version": APP_VERSION,
        "api_version": API_VERSION,
    }

