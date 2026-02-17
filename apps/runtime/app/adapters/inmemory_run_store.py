"""In-memory run store adapter."""

from __future__ import annotations

from app.models.core import Run


class InMemoryRunStore:
    """Stores runs in memory."""

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
