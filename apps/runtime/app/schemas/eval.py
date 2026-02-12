"""Evaluation-related schemas."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.core import EvalStatus


class EvalRunCreate(BaseModel):
    """Request schema for starting an evaluation run."""
    run_id: str | None = Field(default=None, description="Workflow run to evaluate.")
    suite: str | None = Field(default=None, description="Evaluation suite name.")


class EvalRunResponse(BaseModel):
    """Evaluation run response schema."""
    eval_id: str
    run_id: str | None = None
    status: EvalStatus
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    results: dict | None = None
    metrics: dict | None = None
    metadata: dict | None = None

