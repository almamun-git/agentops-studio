"""In-memory vector store adapter."""

from __future__ import annotations

import json

from app.models.core import MemoryItem


class InMemoryVectorStore:
    """Simple in-memory vector store for local development."""

    def __init__(self) -> None:
        self._items: dict[str, dict[str, MemoryItem]] = {}

    async def upsert(self, items: list[MemoryItem]) -> None:
        for item in items:
            self._items.setdefault(item.user_id, {})[item.memory_id] = item

    async def query(self, user_id: str, query: str, *, limit: int = 10) -> list[MemoryItem]:
        needle = query.lower()
        candidates = self._items.get(user_id, {}).values()
        matches = [
            item
            for item in candidates
            if needle in item.key.lower()
            or needle in json.dumps(item.value, sort_keys=True).lower()
        ]
        return matches[:limit]

    async def delete(self, memory_id: str) -> None:
        for user_items in self._items.values():
            if memory_id in user_items:
                del user_items[memory_id]
                break
