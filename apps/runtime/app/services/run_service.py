"""Run service for workflow run storage."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.core import Run


class RunService:
    """In-memory run store."""

    def __init__(self) -> None:
        self._store: dict[str, Run] = {}

    def create(self, run: Run) -> Run:
        """Store a run."""
        self._store[run.run_id] = run
        return run

    def get(self, run_id: str) -> Run | None:
        """Get a run by id."""
        return self._store.get(run_id)

    def list_runs(self) -> list[Run]:
        """List runs sorted by created_at descending."""
        return sorted(
            self._store.values(),
            key=lambda r: r.created_at,
            reverse=True,
        )


_run_service: RunService | None = None


def get_run_service() -> RunService:
    """FastAPI dependency for the run service."""
    global _run_service
    if _run_service is None:
        _run_service = RunService()
    return _run_service
