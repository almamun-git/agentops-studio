"""Evaluation-related schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class EvalRunResponse(BaseModel):
    """Evaluation run response schema."""
    eval_id: str
    status: Literal["pending", "running", "completed", "failed"]
    created_at: datetime
    results: dict | None = None

