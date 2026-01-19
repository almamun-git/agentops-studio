"""In-memory telemetry adapter."""

from __future__ import annotations

from app.models.core import Run, Step, ToolCall


class InMemoryTelemetry:
    """Stores telemetry in local memory for inspection/tests."""

    def __init__(self) -> None:
        self.runs: list[Run] = []
        self.steps: list[Step] = []
        self.tool_calls: list[ToolCall] = []

    def record_run(self, run: Run) -> None:
        self.runs.append(run)

    def record_step(self, step: Step) -> None:
        self.steps.append(step)

    def record_tool_call(self, tool_call: ToolCall) -> None:
        self.tool_calls.append(tool_call)
