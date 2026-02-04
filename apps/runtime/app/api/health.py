from fastapi import APIRouter

from app.schemas.common import StatusResponse
from app.utils.time import format_timestamp, utc_now

router = APIRouter()


@router.get("/health", response_model=StatusResponse, response_description="Service health and timestamp.")
def health():
    """Health check endpoint."""
    return StatusResponse(
        status="ok",
        timestamp=format_timestamp(utc_now()),
    )


