"""Adapter registry utilities."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

AdapterFactory = Callable[[], object]
"""Type alias for adapter factory: no-arg callable returning an adapter instance."""


class AdapterRegistry:
    """Simple registry for adapter factories."""

    def __init__(self) -> None:
        self._registry: dict[str, dict[str, AdapterFactory]] = defaultdict(dict)

    def register(self, adapter_type: str, name: str, factory: AdapterFactory) -> None:
        """Register a factory for a given adapter type/name."""
        if name in self._registry[adapter_type]:
            raise ValueError(f"Adapter '{adapter_type}:{name}' already registered.")
        self._registry[adapter_type][name] = factory

    def get(self, adapter_type: str, name: str) -> object:
        """Create an adapter instance by type/name."""
        try:
            factory = self._registry[adapter_type][name]
        except KeyError as exc:
            raise KeyError(f"Adapter '{adapter_type}:{name}' not found.") from exc
        return factory()

    def list(self, adapter_type: str) -> list[str]:
        """List registered adapter names for a type."""
        return sorted(self._registry.get(adapter_type, {}).keys())
