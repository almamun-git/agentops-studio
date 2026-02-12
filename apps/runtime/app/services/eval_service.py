"""Evaluation run service."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.core import EvalRun
from app.schemas.eval import EvalRunCreate
from app.utils.id import generate_eval_id


class EvalService:
    """In-memory evaluation run store and execution."""

    def __init__(self) -> None:
        self._store: dict[str, EvalRun] = {}

    def create(self, payload: EvalRunCreate) -> EvalRun:
        """Create a new evaluation run (pending)."""
        now = datetime.now(timezone.utc)
        eval_id = generate_eval_id()
        eval_run = EvalRun(
            eval_id=eval_id,
            run_id=payload.run_id,
            status="pending",
            created_at=now,
            metadata={"suite": payload.suite} if payload.suite else None,
        )
        self._store[eval_id] = eval_run
        return eval_run

    def get(self, eval_id: str) -> EvalRun | None:
        """Get an evaluation run by id."""
        return self._store.get(eval_id)

    def run(self, eval_id: str) -> EvalRun | None:
        """Execute an evaluation run (placeholder: marks completed with stub results)."""
        eval_run = self._store.get(eval_id)
        if not eval_run or eval_run.status != "pending":
            return eval_run
        now = datetime.now(timezone.utc)
        updated = eval_run.model_copy(update={
            "status": "running",
            "started_at": now,
        })
        self._store[eval_id] = updated
        # Placeholder execution: set results and metrics
        finished = updated.model_copy(update={
            "status": "completed",
            "finished_at": now,
            "results": {"passed": 0, "failed": 0, "skipped": 0},
            "metrics": {"duration_seconds": 0.0},
        })
        self._store[eval_id] = finished
        return finished


_eval_service: EvalService | None = None


def get_eval_service() -> EvalService:
    """FastAPI dependency for the eval service."""
    global _eval_service
    if _eval_service is None:
        _eval_service = EvalService()
    return _eval_service
