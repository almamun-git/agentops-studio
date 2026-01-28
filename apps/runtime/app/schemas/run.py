"""Run-related schemas."""

from datetime import datetime

from pydantic import BaseModel

from app.models.core import RunStatus, Step, ToolCall


class RunCreate(BaseModel):
    """Schema for creating a run."""
    workflow_id: str
    input: dict


class RunResponse(BaseModel):
    """Schema for run response."""
    run_id: str
    workflow_id: str
    status: RunStatus
    created_at: datetime


class ToolCallResponse(ToolCall):
    """Schema for tool call response."""


class StepResponse(Step):
    """Schema for step response."""


class RunDetailResponse(RunResponse):
    """Schema for run response with steps."""

    steps: list[StepResponse]


class RunListResponse(BaseModel):
    """Schema for listing runs."""

    runs: list[RunResponse]

