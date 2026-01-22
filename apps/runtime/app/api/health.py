from fastapi import APIRouter

from app.schemas.common import StatusResponse
from app.utils.time import utc_now

router = APIRouter()


@router.get("/health", response_model=StatusResponse)
def health():
    """Health check endpoint."""
    return StatusResponse(
        status="ok",
        timestamp=utc_now(),
    )


