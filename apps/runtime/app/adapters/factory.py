"""Adapter factories and shared instances."""

from __future__ import annotations

from app.adapters import (
    AdapterRegistry,
    EchoLLMAdapter,
    InMemoryOrchestrator,
    InMemoryTelemetry,
    InMemoryVectorStore,
)
from app.adapters.interfaces import VectorStoreAdapter
from app.core.config import settings

_registry = AdapterRegistry()
_registry.register("orchestrator", "inmemory", InMemoryOrchestrator)
_registry.register("llm", "echo", EchoLLMAdapter)
_registry.register("vector_store", "inmemory", InMemoryVectorStore)
_registry.register("telemetry", "inmemory", InMemoryTelemetry)

_cache: dict[str, object] = {}


def _get_cached(adapter_type: str, name: str) -> object:
    cache_key = f"{adapter_type}:{name}"
    if cache_key not in _cache:
        _cache[cache_key] = _registry.get(adapter_type, name)
    return _cache[cache_key]


def get_vector_store() -> VectorStoreAdapter:
    """Return the configured vector store adapter."""
    return _get_cached("vector_store", settings.vector_store_adapter)
