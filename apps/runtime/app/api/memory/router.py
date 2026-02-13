from fastapi import APIRouter, Depends

from app.schemas.memory import (
    MemoryDeleteResponse,
    MemoryResponse,
    MemoryUpsertRequest,
    MemoryUpsertResponse,
)
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


@router.put("/{user_id}", response_model=MemoryUpsertResponse, response_description="Upserted memory items.")
async def upsert_memory(
    user_id: str,
    payload: MemoryUpsertRequest,
    memory_svc: MemoryService = Depends(get_memory_service),
) -> MemoryUpsertResponse:
    """Upsert memory items for a user."""
    items = await memory_svc.upsert(user_id, payload.items)
    return MemoryUpsertResponse(user_id=user_id, items=items)


@router.delete("/{user_id}/{memory_id}", response_model=MemoryDeleteResponse)
async def delete_memory(
    user_id: str,
    memory_id: str,
    memory_svc: MemoryService = Depends(get_memory_service),
) -> MemoryDeleteResponse:
    """Delete a memory item by id."""
    await memory_svc.delete(memory_id)
    return MemoryDeleteResponse(memory_id=memory_id)

