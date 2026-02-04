from fastapi import APIRouter

from app.core.metadata import API_VERSION, APP_VERSION
from app.schemas.common import VersionResponse

router = APIRouter()


@router.get("/version", response_model=VersionResponse, response_description="API and app version.")
def get_version() -> VersionResponse:
    """Get API version information."""
    return VersionResponse(
        version=APP_VERSION,
        api_version=API_VERSION,
    )

