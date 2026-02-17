"""Postgres-backed run store adapter. Requires: pip install -e '.[postgres]'"""

from __future__ import annotations

import json

from app.core.config import settings
from app.models.core import Run

TABLE = "runs"


class PostgresRunStore:
    """Stores runs in Postgres as JSONB."""

    def __init__(self, database_url: str | None = None) -> None:
        import psycopg
        self._database_url = database_url or settings.database_url
        self._conn: psycopg.Connection | None = None

    def _get_conn(self) -> "psycopg.Connection":
        import psycopg
        if self._conn is None or self._conn.closed:
            self._conn = psycopg.connect(self._database_url)
            with self._conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {TABLE} (
                        run_id TEXT PRIMARY KEY,
                        data JSONB NOT NULL
                    )
                """)
                self._conn.commit()
        return self._conn

    def create(self, run: Run) -> Run:
        """Store a run."""
        conn = self._get_conn()
        data = run.model_dump(mode="json")
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {TABLE} (run_id, data) VALUES (%s, %s) ON CONFLICT (run_id) DO UPDATE SET data = EXCLUDED.data",
                (run.run_id, json.dumps(data)),
            )
            conn.commit()
        return run

    def get(self, run_id: str) -> Run | None:
        """Get a run by id."""
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(f"SELECT data FROM {TABLE} WHERE run_id = %s", (run_id,))
            row = cur.fetchone()
        if not row:
            return None
        return Run.model_validate(json.loads(row[0]))

    def list_runs(self) -> list[Run]:
        """List runs sorted by created_at descending."""
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(f"SELECT data FROM {TABLE}")
            rows = cur.fetchall()
        runs = [Run.model_validate(json.loads(r[0])) for r in rows]
        return sorted(runs, key=lambda r: r.created_at, reverse=True)
