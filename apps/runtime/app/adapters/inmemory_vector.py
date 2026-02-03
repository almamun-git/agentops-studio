"""In-memory vector store adapter."""

from __future__ import annotations

import json
import re

from app.models.core import MemoryItem


class InMemoryVectorStore:
    """Simple in-memory vector store for local development."""

    def __init__(self) -> None:
        self._items: dict[str, dict[str, MemoryItem]] = {}

    async def upsert(self, items: list[MemoryItem]) -> None:
        for item in items:
            self._items.setdefault(item.user_id, {})[item.memory_id] = item

    async def query(self, user_id: str, query: str, *, limit: int = 10) -> list[MemoryItem]:
        tokens = re.findall(r"[a-z0-9]+", query.lower())
        candidates = self._items.get(user_id, {}).values()
        if not tokens:
            return []
        matches = []
        for item in candidates:
            haystack = f"{item.key} {json.dumps(item.value, sort_keys=True)}".lower()
            if any(token in haystack for token in tokens):
                matches.append(item)
        return matches[:limit]

    async def delete(self, memory_id: str) -> None:
        for user_items in self._items.values():
            if memory_id in user_items:
                del user_items[memory_id]
                break
