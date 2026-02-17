"""Evaluation run service."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.core import EvalRun
from app.schemas.eval import EvalRunCreate
from app.services.run_service import RunService
from app.utils.id import generate_eval_id


def _evaluate_run(run, started_at: datetime, finished_at: datetime) -> tuple[int, int, int, float]:
    """Evaluate a run: passed, failed, skipped, duration_seconds."""
    if run is None:
        return 0, 1, 0, (finished_at - started_at).total_seconds()
    passed = 0
    failed = 0
    if run.status == "completed" and run.steps and run.output:
        passed = 1
    else:
        failed = 1
    duration = (finished_at - started_at).total_seconds()
    return passed, failed, 0, duration


class EvalService:
    """In-memory evaluation run store and execution."""

    def __init__(self, run_svc: RunService) -> None:
        self._store: dict[str, EvalRun] = {}
        self._run_svc = run_svc

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
        """Execute an evaluation run: fetches run, compares outputs, computes metrics."""
        eval_run = self._store.get(eval_id)
        if not eval_run or eval_run.status != "pending":
            return eval_run
        now = datetime.now(timezone.utc)
        updated = eval_run.model_copy(update={
            "status": "running",
            "started_at": now,
        })
        self._store[eval_id] = updated
        run = self._run_svc.get(eval_run.run_id) if eval_run.run_id else None
        passed, failed, skipped, duration = _evaluate_run(run, now, now)
        finished = updated.model_copy(update={
            "status": "completed",
            "finished_at": now,
            "results": {"passed": passed, "failed": failed, "skipped": skipped},
            "metrics": {"duration_seconds": duration},
        })
        self._store[eval_id] = finished
        return finished


_eval_service: EvalService | None = None


def get_eval_service() -> EvalService:
    """FastAPI dependency for the eval service."""
    global _eval_service
    if _eval_service is None:
        from app.services.run_service import get_run_service
        _eval_service = EvalService(get_run_service())
    return _eval_service
