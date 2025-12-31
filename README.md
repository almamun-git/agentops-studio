# AgentOps Studio (Stack-Agnostic Edition)

AgentOps Studio is a production-style platform to run multi-agent workflows with:
- **Tool calling** - Agents can invoke external tools (RAG, HTTP, DB, etc.)
- **Memory** - Short-term conversation state + long-term user profiles
- **Traces & audit logs** - Full visibility into agent decisions and tool calls
- **Evals** - Automated testing harness for agent reliability
- **Guardrails** - Safety policies and output validation

This repo is intentionally structured around **stable contracts + pluggable adapters** so the orchestrator/LLM/storage/observability can be swapped without rewriting the core product.

### Repo layout

- `apps/runtime`: FastAPI runtime API (agent workflow runner + adapters later)
- `apps/web`: Next.js UI (chat, run trace, memory, eval dashboard) — scaffolded later
- `docs/`: architecture + design notes
- `docker-compose.yml`: local infra (Postgres + Redis)

### Local dev (initial scaffold)

Bring up infrastructure:

```bash
make infra-up
# or: docker compose up -d
```

Run runtime API:

```bash
make dev-runtime
# or manually:
cd apps/runtime
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
uvicorn app.main:app --reload --port 8000
```

Verify:
- http://localhost:8000/health

### Next steps

- Define core data model: Run, Step, ToolCall, MemoryItem, EvalRun
- Add adapter interfaces: OrchestratorAdapter, LLMAdapter, VectorStoreAdapter, TelemetryAdapter
- Implement first concrete stack: FastAPI + (LangGraph) + Postgres + Redis + OpenTelemetry


