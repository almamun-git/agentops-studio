"""Run-related schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class RunCreate(BaseModel):
    """Schema for creating a run."""
    workflow_id: str
    input: dict


class RunResponse(BaseModel):
    """Schema for run response."""
    run_id: str
    workflow_id: str
    status: Literal["pending", "running", "completed", "failed"]
    created_at: datetime

