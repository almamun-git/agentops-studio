from datetime import datetime, timezone

from app.adapters.inmemory_telemetry import InMemoryTelemetry
from app.models.core import Run, Step, ToolCall


def test_inmemory_telemetry_records_events():
    telemetry = InMemoryTelemetry()
    run = Run(
        run_id="run-1",
        workflow_id="wf-1",
        created_at=datetime.now(timezone.utc),
        input={},
    )
    step = Step(step_id="step-1", run_id="run-1", name="step")
    tool_call = ToolCall(tool_call_id="tc-1", tool_name="tool", input={})

    telemetry.record_run(run)
    telemetry.record_step(step)
    telemetry.record_tool_call(tool_call)

    assert telemetry.runs == [run]
    assert telemetry.steps == [step]
    assert telemetry.tool_calls == [tool_call]
