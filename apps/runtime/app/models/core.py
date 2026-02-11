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

    run_id: str = Field(..., description="Unique run identifier.")
    workflow_id: str = Field(..., description="Workflow identifier.")
    status: RunStatus = Field(default="pending", description="Run status.")
    created_at: datetime = Field(..., description="When the run was created.")
    started_at: datetime | None = Field(default=None, description="When the run started.")
    finished_at: datetime | None = Field(default=None, description="When the run finished.")
    input: dict = Field(..., description="Run input payload.")
    output: dict | None = Field(default=None, description="Run output payload.")
    steps: list[Step] = Field(default_factory=list, description="Steps in this run.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")


class MemoryItem(BaseModel):
    """Stored memory item."""

    memory_id: str = Field(..., description="Unique memory item identifier.")
    user_id: str = Field(..., description="User or tenant identifier.")
    key: str = Field(..., description="Memory key.")
    value: dict = Field(..., description="Stored value.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")
    created_at: datetime = Field(..., description="When the item was created.")
    updated_at: datetime | None = Field(default=None, description="When the item was last updated.")


class EvalRun(BaseModel):
    """Evaluation run for a workflow or agent."""

    eval_id: str = Field(..., description="Unique evaluation run identifier.")
    run_id: str | None = Field(default=None, description="Associated workflow run id.")
    status: EvalStatus = Field(default="pending", description="Evaluation status.")
    created_at: datetime = Field(..., description="When the eval was created.")
    started_at: datetime | None = Field(default=None, description="When the eval started.")
    finished_at: datetime | None = Field(default=None, description="When the eval finished.")
    results: dict | None = Field(default=None, description="Evaluation results.")
    metrics: dict | None = Field(default=None, description="Evaluation metrics.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")
