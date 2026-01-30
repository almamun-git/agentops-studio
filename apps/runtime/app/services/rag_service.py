"""RAG service for ingesting and querying documents."""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone

from app.adapters.factory import get_vector_store
from app.adapters.interfaces import VectorStoreAdapter
from app.models.core import MemoryItem
from app.schemas.rag import RagDocument, RagDocumentIn, RagMatch
from app.utils.id import generate_memory_id


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _score(query: str, text: str) -> float:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0
    text_counts = Counter(_tokenize(text))
    hits = sum(text_counts.get(token, 0) for token in query_tokens)
    return hits / max(len(query_tokens), 1)


class RagService:
    """Coordinates RAG ingest and retrieval operations."""

    def __init__(self, vector_store: VectorStoreAdapter) -> None:
        self._vector_store = vector_store

    async def ingest(self, user_id: str, documents: list[RagDocumentIn]) -> list[RagDocument]:
        now = datetime.now(timezone.utc)
        items: list[MemoryItem] = []
        stored: list[RagDocument] = []

        for doc in documents:
            doc_id = generate_memory_id()
            payload = {"text": doc.text, "metadata": doc.metadata or {}}
            item = MemoryItem(
                memory_id=doc_id,
                user_id=user_id,
                key=f"doc:{doc_id}",
                value=payload,
                metadata={"kind": "rag_document"},
                created_at=now,
            )
            items.append(item)
            stored.append(RagDocument(doc_id=doc_id, text=doc.text, metadata=doc.metadata))

        if items:
            await self._vector_store.upsert(items)

        return stored

    async def query(self, user_id: str, query: str, top_k: int) -> list[RagMatch]:
        candidates = await self._vector_store.query(user_id, query, limit=top_k * 3)
        scored: list[tuple[float, MemoryItem]] = []

        for item in candidates:
            text = str(item.value.get("text", ""))
            scored.append((_score(query, text), item))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        matches: list[RagMatch] = []
        for score, item in scored[:top_k]:
            matches.append(
                RagMatch(
                    doc_id=item.memory_id,
                    text=str(item.value.get("text", "")),
                    metadata=item.value.get("metadata"),
                    score=score,
                )
            )

        return matches


def get_rag_service() -> RagService:
    """FastAPI dependency for the RAG service."""
    return RagService(get_vector_store())
