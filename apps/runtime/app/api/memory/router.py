from fastapi import APIRouter, Depends

from app.schemas.memory import MemoryResponse
from app.services.memory_service import MemoryService, get_memory_service

router = APIRouter()


@router.get("/{user_id}", response_model=MemoryResponse, response_description="User memory items.")
async def get_memory(
    user_id: str,
    memory_svc: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    """Get all memory items for a user."""
    items = await memory_svc.get_all(user_id)
    return MemoryResponse(user_id=user_id, items=items)


@router.put("/{user_id}", response_description="Updated memory status.")
async def update_memory(user_id: str):
    """Update user memory."""
    return {"user_id": user_id, "status": "updated"}

