from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "agentops-runtime",
    }


