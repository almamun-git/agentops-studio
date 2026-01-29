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

  useEffect(() => {
    let cancelled = false;

    const loadRun = async () => {
      try {
        setDetail({ state: "loading" });
        const response = await fetch(`${runtimeBase}/runs/${params.runId}`);
        if (!response.ok) {
          throw new Error(`Failed to load run (${response.status})`);
        }
        const payload = (await response.json()) as RunDetail;
        if (!cancelled) {
          setDetail({ state: "ready", payload });
        }
      } catch (err) {
        if (!cancelled) {
          setDetail({
            state: "error",
            message: err instanceof Error ? err.message : "Unknown error",
          });
        }
      }
    };

    loadRun();
    return () => {
      cancelled = true;
    };
  }, [runtimeBase, params.runId]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h1 className="text-2xl font-semibold">Run detail</h1>
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
      </div>
    </div>
  );
}
