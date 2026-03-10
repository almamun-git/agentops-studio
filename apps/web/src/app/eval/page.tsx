"use client";

import { useState } from "react";

import { formatTimestamp } from "@/lib/format";
import { getRuntimeBase } from "@/lib/runtime";

type EvalRun = {
  eval_id: string;
  run_id: string | null;
  status: string;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  results: Record<string, unknown> | null;
  metrics: Record<string, unknown> | null;
  metadata: Record<string, unknown> | null;
};

export default function EvalPage() {
  const runtimeBase = getRuntimeBase();
  const [runId, setRunId] = useState("");
  const [suite, setSuite] = useState("");
  const [createResult, setCreateResult] = useState<EvalRun | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [fetchId, setFetchId] = useState("");
  const [fetchResult, setFetchResult] = useState<EvalRun | null>(null);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(false);

  const handleCreate = async () => {
    setCreateError(null);
    setCreateResult(null);
    setCreating(true);
    try {
      const body: { run_id?: string; suite?: string } = {};
      if (runId.trim()) body.run_id = runId.trim();
      if (suite.trim()) body.suite = suite.trim();
      const response = await fetch(`${runtimeBase}/eval/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const payload = (await response.json()) as EvalRun;
      if (!response.ok) {
        throw new Error((payload as { detail?: string })?.detail ?? `Failed (${response.status})`);
      }
      setCreateResult(payload);
      setFetchId(payload.eval_id);
      setFetchResult(payload);
      setFetchError(null);
    } catch (err) {
      setCreateError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setCreating(false);
    }
  };

  const handleFetch = async () => {
    if (!fetchId.trim()) return;
    setFetchError(null);
    setFetchResult(null);
    setFetching(true);
    try {
      const response = await fetch(
        `${runtimeBase}/eval/${encodeURIComponent(fetchId.trim())}`
      );
      const payload = (await response.json()) as EvalRun | { detail?: string };
      if (!response.ok) {
        throw new Error(
          (payload as { detail?: string })?.detail ?? `Failed (${response.status})`
        );
      }
      setFetchResult(payload as EvalRun);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setFetching(false);
    }
  };

  const displayRun = createResult ?? fetchResult;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <nav className="mb-4 flex items-center justify-between text-sm">
          <a
            href="/"
            className="inline-block text-slate-400 hover:text-emerald-300"
          >
            ← Back to home
          </a>
          <span className="font-mono text-xs text-slate-500">
            Base: {runtimeBase}
          </span>
        </nav>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h1 className="text-2xl font-semibold">Eval</h1>
          <p className="mt-2 text-sm text-slate-300">
            Create evaluation runs and inspect results.
          </p>
          <p className="mt-2 text-xs text-slate-400">
            Runtime base:{" "}
            <span className="font-mono text-slate-200">{runtimeBase}</span>
          </p>
        </div>

        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-lg font-semibold">Create evaluation</h2>
          <p className="mt-2 text-sm text-slate-400">
            Optionally link a workflow run and/or suite name.
          </p>
          <div className="mt-4 grid gap-4">
            <label className="text-xs uppercase text-slate-400" htmlFor="eval-run-id">
              Run ID (optional)
              <input
                id="eval-run-id"
                className="mt-2 w-full max-w-md rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                value={runId}
                onChange={(e) => setRunId(e.target.value)}
                placeholder="Workflow run to evaluate"
              />
            </label>
            <label className="text-xs uppercase text-slate-400" htmlFor="eval-suite">
              Suite (optional)
              <input
                id="eval-suite"
                className="mt-2 w-full max-w-md rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                value={suite}
                onChange={(e) => setSuite(e.target.value)}
                placeholder="Evaluation suite name"
              />
            </label>
            <button
              type="button"
              onClick={handleCreate}
              disabled={creating}
              className="w-fit rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:border-emerald-400 hover:text-emerald-300 disabled:opacity-50"
            >
              {creating ? "Running..." : "Run eval"}
            </button>
            {createError ? (
              <p className="text-sm text-rose-200">{createError}</p>
            ) : null}
          </div>
        </div>

        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-lg font-semibold">Get evaluation by ID</h2>
          <div className="mt-4 flex flex-wrap items-end gap-3">
            <label className="text-xs uppercase text-slate-400" htmlFor="eval-id">
              Eval ID
              <input
                id="eval-id"
                className="mt-2 block w-64 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm text-slate-100"
                value={fetchId}
                onChange={(e) => setFetchId(e.target.value)}
              />
            </label>
            <button
              type="button"
              onClick={handleFetch}
              disabled={fetching || !fetchId.trim()}
              className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:border-emerald-400 hover:text-emerald-300 disabled:opacity-50"
            >
              {fetching ? "Loading..." : "Fetch"}
            </button>
          </div>
          {fetchError ? (
            <p className="mt-3 text-sm text-rose-200">{fetchError}</p>
          ) : null}
        </div>

        {displayRun ? (
          <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Evaluation result</h2>
            <div className="mt-4 space-y-2 text-sm text-slate-300">
              <p>
                Eval ID:{" "}
                <span className="font-mono text-slate-200">
                  {displayRun.eval_id}
                </span>
              </p>
              <p>
                Status:{" "}
                <span className="uppercase text-slate-400">
                  {displayRun.status}
                </span>
              </p>
              {displayRun.run_id ? (
                <p>
                  Run ID:{" "}
                  <span className="font-mono text-slate-200">
                    {displayRun.run_id}
                  </span>
                </p>
              ) : null}
              <p className="text-xs text-slate-500">
                Created {formatTimestamp(displayRun.created_at)}
              </p>
            </div>
            {(displayRun.results || displayRun.metrics) && (
              <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">
                <pre className="overflow-auto text-xs text-slate-300">
                  {JSON.stringify(
                    {
                      results: displayRun.results,
                      metrics: displayRun.metrics,
                    },
                    null,
                    2
                  )}
                </pre>
              </div>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}
