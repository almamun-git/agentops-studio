## AgentOps Studio (Stack-Agnostic Edition)

AgentOps Studio is a production-style platform to run multi-agent workflows with:
- tool calling
- memory
- traces/audit logs
- evals
- guardrails

This repo is intentionally structured around **stable contracts + pluggable adapters** so the orchestrator/LLM/storage/observability can be swapped without rewriting the core product.

### Repo layout

- `apps/runtime`: FastAPI runtime API (agent workflow runner + adapters later)
- `apps/web`: Next.js UI (chat, run trace, memory, eval dashboard) — scaffolded later
- `docs/`: architecture + design notes
- `docker-compose.yml`: local infra (Postgres + Redis)

### Local dev (initial scaffold)

Bring up infra:

```bash
docker compose up -d
```

Run runtime API:

```bash
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


