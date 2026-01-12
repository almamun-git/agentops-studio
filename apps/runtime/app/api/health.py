from datetime import datetime

from fastapi import APIRouter

from app.schemas.common import StatusResponse

router = APIRouter()


@router.get("/health", response_model=StatusResponse)
def health():
    """Health check endpoint."""
    return StatusResponse(
        status="ok",
        timestamp=datetime.utcnow(),
    )


