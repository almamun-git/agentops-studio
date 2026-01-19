from app.adapters import LLMAdapter, OrchestratorAdapter, TelemetryAdapter, VectorStoreAdapter
from app.models.core import MemoryItem, Run, Step, ToolCall


class DummyOrchestrator:
    async def start_run(self, run: Run) -> Run:
        return run

    async def get_run(self, run_id: str) -> Run | None:
        return None

    async def list_steps(self, run_id: str) -> list[Step]:
        return []


class DummyLLM:
    async def generate(self, prompt: str, *, metadata: dict | None = None) -> str:
        return "ok"

    async def chat(self, messages: list[dict], *, metadata: dict | None = None) -> dict:
        return {"role": "assistant", "content": "ok"}


class DummyVectorStore:
    async def upsert(self, items: list[MemoryItem]) -> None:
        return None

    async def query(self, user_id: str, query: str, *, limit: int = 10) -> list[MemoryItem]:
        return []

    async def delete(self, memory_id: str) -> None:
        return None


class DummyTelemetry:
    def record_run(self, run: Run) -> None:
        return None

    def record_step(self, step: Step) -> None:
        return None

    def record_tool_call(self, tool_call: ToolCall) -> None:
        return None


def test_adapter_protocols_are_runtime_checkable():
    assert isinstance(DummyOrchestrator(), OrchestratorAdapter)
    assert isinstance(DummyLLM(), LLMAdapter)
    assert isinstance(DummyVectorStore(), VectorStoreAdapter)
    assert isinstance(DummyTelemetry(), TelemetryAdapter)
