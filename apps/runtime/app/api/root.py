from fastapi import APIRouter

from app.core.constants import API_V1_PREFIX, DOCS_PATH
from app.core.metadata import APP_NAME, APP_VERSION
from app.schemas.common import RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse, response_description="Service name, version, and API base paths.")
def root() -> RootResponse:
    """Root endpoint with API information."""
    return RootResponse(
        name=APP_NAME,
        version=APP_VERSION,
        docs=DOCS_PATH,
        api_base=API_V1_PREFIX,
        version_endpoint=f"{API_V1_PREFIX}/version",
    )

