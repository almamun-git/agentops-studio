"""RAG request/response schemas."""

from pydantic import BaseModel, Field


class RagDocumentIn(BaseModel):
    """Document payload for ingestion."""

    text: str = Field(..., min_length=1)
    metadata: dict | None = None


class RagDocument(BaseModel):
    """Stored document details."""

    doc_id: str
    text: str
    metadata: dict | None = None


class RagMatch(BaseModel):
    """Matched document for a query."""

    doc_id: str
    text: str
    score: float
    metadata: dict | None = None


class RagIngestRequest(BaseModel):
    """Ingest documents into the RAG store."""

    user_id: str
    documents: list[RagDocumentIn]


class RagIngestResponse(BaseModel):
    """RAG ingest response."""

    user_id: str
    documents: list[RagDocument]


class RagQueryRequest(BaseModel):
    """Query documents from the RAG store."""

    user_id: str
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class RagQueryResponse(BaseModel):
    """RAG query response."""

    user_id: str
    query: str
    matches: list[RagMatch]
