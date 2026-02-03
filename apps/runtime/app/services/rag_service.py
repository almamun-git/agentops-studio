"""RAG service for ingesting and querying documents."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from app.adapters.factory import get_vector_store
from app.adapters.interfaces import VectorStoreAdapter
from app.models.core import MemoryItem
from app.schemas.rag import RagDocument, RagDocumentIn, RagMatch
from app.utils.id import generate_memory_id

_CANDIDATE_MULTIPLIER = 3


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _metadata_text(metadata: dict | None) -> str:
    if not metadata:
        return ""
    try:
        return json.dumps(metadata, sort_keys=True, default=str)
    except TypeError:
        return " ".join(str(value) for value in metadata.values())


def _score(query: str, text: str) -> float:
    query_tokens = set(_tokenize(query))
    if not query_tokens:
        return 0.0
    text_tokens = set(_tokenize(text))
    if not text_tokens:
        return 0.0
    hits = len(query_tokens.intersection(text_tokens))
    return hits / len(query_tokens)


class RagService:
    """Coordinates RAG ingest and retrieval operations."""

    def __init__(self, vector_store: VectorStoreAdapter) -> None:
        """Initialize RAG service with a vector store backend."""
        self._vector_store = vector_store

    async def ingest(self, user_id: str, documents: list[RagDocumentIn]) -> list[RagDocument]:
        """Ingest documents for a user into the vector store."""
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
            stored.append(
                RagDocument(
                    doc_id=doc_id,
                    text=doc.text,
                    metadata=doc.metadata,
                    created_at=now,
                )
            )

        if items:
            await self._vector_store.upsert(items)

        return stored

    async def query(self, user_id: str, query: str, top_k: int, *, min_score: float = 0.0) -> list[RagMatch]:
        """Query documents for a user, returning top matches by relevance."""
        if top_k <= 0:
            return []
        candidates = await self._vector_store.query(
            user_id,
            query,
            limit=top_k * _CANDIDATE_MULTIPLIER,
        )
        scored: list[tuple[float, MemoryItem]] = []

        for item in candidates:
            text = str(item.value.get("text", ""))
            metadata = item.value.get("metadata")
            content = f"{text} {_metadata_text(metadata)}".strip()
            score = _score(query, content)
            if score <= 0.0 or score < min_score:
                continue
            scored.append((score, item))

        scored.sort(key=lambda pair: (pair[0], pair[1].created_at), reverse=True)

        matches: list[RagMatch] = []
        for score, item in scored[:top_k]:
            matches.append(
                RagMatch(
                    doc_id=item.memory_id,
                    text=str(item.value.get("text", "")),
                    metadata=item.value.get("metadata"),
                    score=score,
                    created_at=item.created_at,
                )
            )

        return matches

    async def delete(self, doc_id: str) -> None:
        """Delete a document from the vector store by id."""
        await self._vector_store.delete(doc_id)


def get_rag_service() -> RagService:
    """FastAPI dependency for the RAG service."""
    return RagService(get_vector_store())
