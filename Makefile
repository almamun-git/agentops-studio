.PHONY: help infra-up infra-down dev-runtime clean

help:
	@echo "AgentOps Studio - Common Commands"
	@echo ""
	@echo "  make infra-up      - Start local infrastructure (Postgres + Redis)"
	@echo "  make infra-down    - Stop local infrastructure"
	@echo "  make dev-runtime   - Run runtime API in dev mode"
	@echo "  make clean         - Clean Python cache files"

infra-up:
	docker compose up -d

infra-down:
	docker compose down

dev-runtime:
	cd apps/runtime && \
	python -m venv .venv && \
	source .venv/bin/activate && \
	pip install -U pip && \
	pip install -e . && \
	uvicorn app.main:app --reload --port 8000

clean:
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

