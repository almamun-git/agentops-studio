from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "AgentOps Runtime",
        "version": "0.1.0",
        "docs": "/docs",
    }

