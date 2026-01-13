from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
async def get_memory(user_id: str):
    """Get user memory."""
    return {"user_id": user_id, "memory": {}}


@router.put("/{user_id}")
async def update_memory(user_id: str):
    """Update user memory."""
    return {"user_id": user_id, "status": "updated"}

