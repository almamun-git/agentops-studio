from datetime import datetime

import pytest

from app.adapters.inmemory_orchestrator import InMemoryOrchestrator
from app.models.core import Run, Step


@pytest.mark.asyncio
async def test_inmemory_orchestrator_stores_runs_and_steps():
    orchestrator = InMemoryOrchestrator()
    run = Run(
        run_id="run-1",
        workflow_id="wf-1",
        created_at=datetime.now(datetime.UTC),
        input={},
    )

    await orchestrator.start_run(run)
    stored = await orchestrator.get_run("run-1")

    assert stored == run

    step = Step(step_id="step-1", run_id="run-1", name="step")
    orchestrator.add_step(step)

    steps = await orchestrator.list_steps("run-1")
    assert steps == [step]
