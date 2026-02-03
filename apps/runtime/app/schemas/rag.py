"""RAG request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class RagDocumentIn(BaseModel):
    """Document payload for ingestion."""

    text: str = Field(..., min_length=1, description="Document text content.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")


class RagDocument(BaseModel):
    """Stored document details."""

    doc_id: str
    text: str
    metadata: dict | None = None
    created_at: datetime


class RagMatch(BaseModel):
    """Matched document for a query."""

    doc_id: str
    text: str
    score: float
    metadata: dict | None = None
    created_at: datetime


class RagIngestRequest(BaseModel):
    """Ingest documents into the RAG store."""

    user_id: str = Field(..., description="User or tenant identifier.")
    documents: list[RagDocumentIn] = Field(..., description="Documents to ingest.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "user-1",
                    "documents": [
                        {"text": "Mars mission summary", "metadata": {"source": "notes"}},
                    ],
                }
            ]
        }
    }


class RagIngestResponse(BaseModel):
    """RAG ingest response."""

    user_id: str
    documents: list[RagDocument]


class RagQueryRequest(BaseModel):
    """Query documents from the RAG store."""

    user_id: str = Field(..., description="User or tenant identifier.")
    query: str = Field(..., min_length=1, description="Search query text.")
    top_k: int = Field(default=5, ge=1, le=50, description="Max matches to return.")
    min_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score required to return a match.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"user_id": "user-1", "query": "mars mission", "top_k": 3}]
        }
    }


class RagQueryResponse(BaseModel):
    """RAG query response."""

    user_id: str
    query: str
    matches: list[RagMatch]


class RagDeleteResponse(BaseModel):
    """RAG delete response."""

    doc_id: str
    deleted: bool = True
