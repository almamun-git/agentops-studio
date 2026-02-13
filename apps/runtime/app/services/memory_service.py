"""Memory service for listing and upserting user memory."""

from __future__ import annotations

from datetime import datetime, timezone

from app.adapters.factory import get_vector_store
from app.adapters.interfaces import VectorStoreAdapter
from app.models.core import MemoryItem
from app.schemas.memory import MemoryItemIn
from app.utils.id import generate_memory_id

MEMORY_KIND = "memory"


class MemoryService:
    """Coordinates memory operations via vector store."""

    def __init__(self, vector_store: VectorStoreAdapter) -> None:
        """Initialize memory service with a vector store backend."""
        self._vector_store = vector_store

    async def get_all(self, user_id: str) -> list[MemoryItem]:
        """List all memory items for a user (excludes RAG documents)."""
        items = await self._vector_store.list(user_id)
        return [i for i in items if i.metadata.get("kind") == MEMORY_KIND]

    async def upsert(self, user_id: str, items: list[MemoryItemIn]) -> list[MemoryItem]:
        """Upsert memory items for a user."""
        now = datetime.now(timezone.utc)
        memory_items: list[MemoryItem] = []
        for item_in in items:
            memory_id = generate_memory_id()
            item = MemoryItem(
                memory_id=memory_id,
                user_id=user_id,
                key=item_in.key,
                value=item_in.value,
                metadata={"kind": MEMORY_KIND} | (item_in.metadata or {}),
                created_at=now,
            )
            memory_items.append(item)
        if memory_items:
            await self._vector_store.upsert(memory_items)
        return memory_items

    async def delete(self, memory_id: str) -> None:
        """Delete a memory item by id."""
        await self._vector_store.delete(memory_id)


def get_memory_service() -> MemoryService:
    """FastAPI dependency for the memory service."""
    return MemoryService(get_vector_store())
