"use client";

import { useEffect, useState } from "react";

import { formatTimestamp } from "@/lib/format";
import { getRuntimeBase } from "@/lib/runtime";

type RunDetail = {
  run_id: string;
  workflow_id: string;
  status: string;
  created_at: string;
  steps: Array<{
    step_id: string;
    name: string;
    status: string;
    started_at: string | null;
    finished_at: string | null;
    output: Record<string, unknown> | null;
  }>;
};

type RunDetailState =
  | { state: "idle" | "loading" }
  | { state: "ready"; payload: RunDetail }
  | { state: "error"; message: string };

export default function RunDetailPage({
  params,
}: {
  params: { runId: string };
}) {
  const runtimeBase = getRuntimeBase();
  const [detail, setDetail] = useState<RunDetailState>({ state: "idle" });

  const loadRun = async () => {
    try {
      setDetail({ state: "loading" });
      const response = await fetch(`${runtimeBase}/runs/${params.runId}`);
      if (!response.ok) {
        throw new Error(`Failed to load run (${response.status})`);
      }
      const payload = (await response.json()) as RunDetail;
      setDetail({ state: "ready", payload });
    } catch (err) {
      setDetail({
        state: "error",
        message: err instanceof Error ? err.message : "Unknown error",
      });
    }
  };

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      if (!cancelled) {
        await loadRun();
      }
    };

    load();
    return () => {
      cancelled = true;
    };
  }, [runtimeBase, params.runId]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <nav className="mb-4 flex items-center justify-between text-sm">
          <a
            href="/runs"
            className="inline-block text-slate-400 hover:text-emerald-300"
          >
            ← Back to runs
          </a>
          <span className="font-mono text-xs text-slate-500">
            Base: {runtimeBase}
          </span>
        </nav>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-semibold">Run detail</h1>
            <button
              className="text-xs text-slate-300 hover:text-emerald-300"
              type="button"
              onClick={loadRun}
            >
              Refresh
            </button>
          </div>
          <p className="mt-2 text-sm text-slate-300">
            Select a run to view its steps, status, and outputs.
          </p>
          {detail.state === "loading" ? (
            <p className="mt-4 text-sm text-slate-400">Loading run...</p>
          ) : null}
          {detail.state === "error" ? (
            <p className="mt-4 text-sm text-rose-200">{detail.message}</p>
          ) : null}
          {detail.state === "ready" ? (
            <div className="mt-4 grid gap-2 text-sm text-slate-300">
              <p>
                Workflow:{" "}
                <span className="font-medium text-slate-100">
                  {detail.payload.workflow_id}
                </span>
              </p>
              <p>
                Status:{" "}
                <span className="uppercase text-slate-400">
                  {detail.payload.status}
                </span>
              </p>
              <p className="text-xs text-slate-400">
                Run ID: {detail.payload.run_id}
              </p>
              <p className="text-xs text-slate-400">
                Created at {formatTimestamp(detail.payload.created_at)}
              </p>
            </div>
          ) : null}
        </div>
        {detail.state === "ready" ? (
          <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Steps</h2>
            <div className="mt-4 space-y-3">
              {detail.payload.steps.map((step) => (
                <div
                  key={step.step_id}
                  className="rounded-xl border border-slate-800 bg-slate-950 px-4 py-3"
                >
                  <div className="flex items-center justify-between text-sm">
                    <p className="font-medium text-slate-100">{step.name}</p>
                    <p className="text-xs uppercase text-slate-400">
                      {step.status}
                    </p>
                  </div>
                  <p className="mt-2 text-xs text-slate-400">
                    {step.step_id}
                  </p>
                  {(step.started_at || step.finished_at) ? (
                    <p className="mt-1 text-xs text-slate-500">
                      {step.started_at
                        ? `Started ${formatTimestamp(step.started_at)}`
                        : ""}
                      {step.started_at && step.finished_at ? " · " : ""}
                      {step.finished_at
                        ? `Finished ${formatTimestamp(step.finished_at)}`
                        : ""}
                    </p>
                  ) : null}
                  {step.output && Object.keys(step.output).length > 0 ? (
                    <div className="mt-3 rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2">
                      <p className="text-xs uppercase text-slate-500">
                        Output
                      </p>
                      <pre className="mt-1 overflow-auto text-xs text-slate-300">
                        {JSON.stringify(step.output, null, 2)}
                      </pre>
                    </div>
                  ) : null}
                </div>
              ))}
              {detail.payload.steps.length === 0 ? (
                <p className="text-sm text-slate-400">No steps available.</p>
              ) : null}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
