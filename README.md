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

### RAG quickstart

Ingest documents:

```bash
curl -X POST http://localhost:8000/api/v1/rag/ingest \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","documents":[{"text":"Mars mission summary","metadata":{"source":"notes"}}]}'
```

Query documents:

```bash
curl -X POST http://localhost:8000/api/v1/rag/query \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user-1","query":"mars mission","top_k":3,"min_score":0.5}'
```

Delete a document:

```bash
curl -X DELETE http://localhost:8000/api/v1/rag/{doc_id}
```

### Adapter configuration

The runtime defaults to local in-memory adapters. Override via env vars:
`RUN_STORE_ADAPTER`, `ORCHESTRATOR_ADAPTER`, `LLM_ADAPTER`, `VECTOR_STORE_ADAPTER`, `TELEMETRY_ADAPTER`.

Run store options: `inmemory` (default), `redis`, `postgres`.
- Redis: `RUN_STORE_ADAPTER=redis`, requires `pip install -e '.[redis]'` and Redis running.
- Postgres: `RUN_STORE_ADAPTER=postgres`, requires `pip install -e '.[postgres]'` and Postgres running.

### API Documentation

See [docs/api.md](docs/api.md) for API endpoint documentation.
See [docs/data-model.md](docs/data-model.md) for core domain model definitions.
See [docs/adapters.md](docs/adapters.md) for adapter interfaces.
See [docs/push.md](docs/push.md) for pushing to GitHub.

### Project Status

🚧 **Early Development** - Core structure and API foundation in place.

### CI / CD

- GitHub Actions workflows:
  - `ci.yml` – runs tests for the runtime service
  - `lint.yml` – runs ruff on `app` and `tests`

### Next steps

- Implement first concrete stack: FastAPI + (LangGraph) + Postgres + Redis + OpenTelemetry
- Add Web UI: runs list/detail, RAG ingest/query, eval dashboard
- Add guardrails: safety policies and output validation


