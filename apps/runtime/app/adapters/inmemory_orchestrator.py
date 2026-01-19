"""In-memory orchestrator adapter."""

from __future__ import annotations

from collections import defaultdict

from app.models.core import Run, Step


class InMemoryOrchestrator:
    """Stores runs and steps in local memory."""

    def __init__(self) -> None:
        self._runs: dict[str, Run] = {}
        self._steps: dict[str, list[Step]] = defaultdict(list)

    async def start_run(self, run: Run) -> Run:
        self._runs[run.run_id] = run
        return run

    async def get_run(self, run_id: str) -> Run | None:
        return self._runs.get(run_id)

    async def list_steps(self, run_id: str) -> list[Step]:
        return list(self._steps.get(run_id, []))

    def add_step(self, step: Step) -> None:
        """Add a step for a run (helper for local usage)."""
        self._steps[step.run_id].append(step)
