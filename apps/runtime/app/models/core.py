"""Core domain data models."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

RunStatus = Literal["pending", "running", "completed", "failed"]
StepStatus = Literal["pending", "running", "completed", "failed"]
ToolCallStatus = Literal["pending", "running", "completed", "failed"]
EvalStatus = Literal["pending", "running", "completed", "failed"]


class ToolCall(BaseModel):
    """Tool call performed during a step."""

    tool_call_id: str = Field(..., description="Unique tool call identifier.")
    tool_name: str = Field(..., description="Name of the invoked tool.")
    input: dict = Field(..., description="Tool input payload.")
    output: dict | None = Field(default=None, description="Tool output payload.")
    status: ToolCallStatus = Field(default="pending", description="Tool call status.")
    started_at: datetime | None = Field(default=None, description="When the tool call started.")
    finished_at: datetime | None = Field(default=None, description="When the tool call finished.")
    error: str | None = Field(default=None, description="Error message if failed.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")


class Step(BaseModel):
    """Single step inside a run."""

    step_id: str = Field(..., description="Unique step identifier.")
    run_id: str = Field(..., description="Parent run identifier.")
    name: str = Field(..., description="Step name.")
    status: StepStatus = Field(default="pending", description="Step status.")
    input: dict | None = Field(default=None, description="Step input.")
    output: dict | None = Field(default=None, description="Step output.")
    tool_calls: list[ToolCall] = Field(default_factory=list, description="Tool calls made in this step.")
    started_at: datetime | None = Field(default=None, description="When the step started.")
    finished_at: datetime | None = Field(default=None, description="When the step finished.")
    error: str | None = Field(default=None, description="Error message if failed.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")


class Run(BaseModel):
    """Top-level workflow run."""

    run_id: str
    workflow_id: str
    status: RunStatus = "pending"
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    input: dict
    output: dict | None = None
    steps: list[Step] = Field(default_factory=list)
    metadata: dict | None = None


class MemoryItem(BaseModel):
    """Stored memory item."""

    memory_id: str
    user_id: str
    key: str
    value: dict
    metadata: dict | None = None
    created_at: datetime
    updated_at: datetime | None = None


class EvalRun(BaseModel):
    """Evaluation run for a workflow or agent."""

    eval_id: str
    run_id: str | None = None
    status: EvalStatus = "pending"
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    results: dict | None = None
    metrics: dict | None = None
    metadata: dict | None = None
