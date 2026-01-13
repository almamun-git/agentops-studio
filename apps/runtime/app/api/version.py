from fastapi import APIRouter

router = APIRouter()


@router.get("/version")
def get_version():
    """Get API version information."""
    return {
        "version": "0.1.0",
        "api_version": "v1",
    }

