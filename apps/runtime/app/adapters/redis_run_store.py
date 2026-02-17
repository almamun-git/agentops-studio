"""Redis-backed run store adapter. Requires: pip install -e '.[redis]'"""

from __future__ import annotations

import json

from app.core.config import settings
from app.models.core import Run

RUN_KEY_PREFIX = "run:"
RUN_IDS_KEY = "run_ids"


class RedisRunStore:
    """Stores runs in Redis as JSON."""

    def __init__(self, redis_url: str | None = None) -> None:
        from redis import Redis

        self._redis = Redis.from_url(redis_url or settings.redis_url, decode_responses=True)

    def create(self, run: Run) -> Run:
        """Store a run."""
        key = f"{RUN_KEY_PREFIX}{run.run_id}"
        data = run.model_dump(mode="json")
        self._redis.set(key, json.dumps(data))
        self._redis.sadd(RUN_IDS_KEY, run.run_id)
        return run

    def get(self, run_id: str) -> Run | None:
        """Get a run by id."""
        key = f"{RUN_KEY_PREFIX}{run_id}"
        raw = self._redis.get(key)
        if not raw:
            return None
        return Run.model_validate(json.loads(raw))

    def list_runs(self) -> list[Run]:
        """List runs sorted by created_at descending."""
        ids = self._redis.smembers(RUN_IDS_KEY)
        runs: list[Run] = []
        for rid in ids:
            run = self.get(rid)
            if run:
                runs.append(run)
        return sorted(runs, key=lambda r: r.created_at, reverse=True)
