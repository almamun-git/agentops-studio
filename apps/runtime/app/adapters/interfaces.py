"""Adapter interface definitions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from app.models.core import MemoryItem, Run, Step, ToolCall


@runtime_checkable
class RunStoreAdapter(Protocol):
    """Interface for run storage backends."""

    def create(self, run: Run) -> Run:
        """Store a run."""

    def get(self, run_id: str) -> Run | None:
        """Get a run by id."""

    def list_runs(self) -> list[Run]:
        """List runs (e.g. sorted by created_at desc)."""


class AdapterError(RuntimeError):
    """Raised when adapter operations fail."""


@runtime_checkable
class OrchestratorAdapter(Protocol):
    """Interface for workflow orchestration backends."""

    async def start_run(self, run: Run) -> Run:
        """Start execution for a run."""

    async def get_run(self, run_id: str) -> Run | None:
        """Fetch a run by ID."""

    async def list_steps(self, run_id: str) -> list[Step]:
        """List steps for a given run."""


@runtime_checkable
class LLMAdapter(Protocol):
    """Interface for LLM providers."""

    async def generate(self, prompt: str, *, metadata: dict | None = None) -> str:
        """Generate a completion from a prompt."""

    async def chat(
        self,
        messages: list[dict],
        *,
        metadata: dict | None = None,
    ) -> dict:
        """Generate a response for a chat conversation."""


@runtime_checkable
class VectorStoreAdapter(Protocol):
    """Interface for vector store backends."""

    async def upsert(self, items: list[MemoryItem]) -> None:
        """Upsert memory items."""

    async def list(self, user_id: str) -> list[MemoryItem]:
        """List all memory items for a user."""

    async def query(self, user_id: str, query: str, *, limit: int = 10) -> list[MemoryItem]:
        """Query memory items for a user."""

    async def delete(self, memory_id: str) -> None:
        """Delete a memory item."""


@runtime_checkable
class TelemetryAdapter(Protocol):
    """Interface for telemetry backends."""

    def record_run(self, run: Run) -> None:
        """Record run-level telemetry."""

    def record_step(self, step: Step) -> None:
        """Record step-level telemetry."""

    def record_tool_call(self, tool_call: ToolCall) -> None:
        """Record tool-call telemetry."""
