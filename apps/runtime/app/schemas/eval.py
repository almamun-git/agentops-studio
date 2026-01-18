"""Evaluation-related schemas."""

from datetime import datetime

from pydantic import BaseModel

from app.models.core import EvalStatus


class EvalRunResponse(BaseModel):
    """Evaluation run response schema."""
    eval_id: str
    status: EvalStatus
    created_at: datetime
    results: dict | None = None
    metrics: dict | None = None

