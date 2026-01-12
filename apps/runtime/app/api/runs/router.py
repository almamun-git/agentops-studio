from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create_run():
    """Create a new workflow run."""
    return {"message": "Not implemented yet"}


@router.get("/{run_id}")
async def get_run(run_id: str):
    """Get run details."""
    return {"run_id": run_id, "status": "pending"}

