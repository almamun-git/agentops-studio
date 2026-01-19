import pytest

from app.adapters import AdapterRegistry


def test_registry_register_and_get():
    registry = AdapterRegistry()

    registry.register("llm", "echo", lambda: {"name": "echo"})

    assert registry.get("llm", "echo") == {"name": "echo"}


def test_registry_duplicate_registration_raises():
    registry = AdapterRegistry()

    registry.register("telemetry", "noop", lambda: None)

    with pytest.raises(ValueError):
        registry.register("telemetry", "noop", lambda: None)


def test_registry_missing_adapter_raises():
    registry = AdapterRegistry()

    with pytest.raises(KeyError):
        registry.get("vector", "missing")
