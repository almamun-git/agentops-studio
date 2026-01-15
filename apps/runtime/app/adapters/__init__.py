"""Adapter interfaces for orchestrator, LLM, vector store, telemetry.

Each adapter implements a stable contract so implementations can be swapped
without changing the core runtime API.

Concrete implementations (e.g. LangGraph, AutoGen, Semantic Kernel) will live
in submodules such as `orchestrator.langgraph` or `orchestrator.autogen`.
"""

