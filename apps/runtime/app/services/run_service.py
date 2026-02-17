"""Run service for workflow run storage."""

from __future__ import annotations

from app.adapters.interfaces import RunStoreAdapter
from app.models.core import Run


class RunService:
    """Run service backed by a RunStore adapter."""

    def __init__(self, store: RunStoreAdapter) -> None:
        self._store = store

    def create(self, run: Run) -> Run:
        """Store a run."""
        return self._store.create(run)

    def get(self, run_id: str) -> Run | None:
        """Get a run by id."""
        return self._store.get(run_id)

    def list_runs(self) -> list[Run]:
        """List runs sorted by created_at descending."""
        return self._store.list_runs()


_run_service: RunService | None = None


def get_run_service() -> RunService:
    """FastAPI dependency for the run service."""
    global _run_service
    if _run_service is None:
        from app.adapters.factory import get_run_store
        _run_service = RunService(get_run_store())
    return _run_service
