"use client";

import { useEffect, useState } from "react";

import { getRuntimeBase } from "@/lib/runtime";

export default function RunsPage() {
  const runtimeBase = getRuntimeBase();
  const [workflowId, setWorkflowId] = useState("demo-workflow");
  const [inputJson, setInputJson] = useState('{"prompt":"hello"}');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [runs, setRuns] = useState<Array<{
    run_id: string;
    workflow_id: string;
    status: string;
    created_at: string;
  }> | null>(null);
  const [runsError, setRunsError] = useState<string | null>(null);
  const [runsLoading, setRunsLoading] = useState(false);

  const loadRuns = async () => {
    try {
      setRunsError(null);
      setRunsLoading(true);
      const response = await fetch(`${runtimeBase}/runs`);
      if (!response.ok) {
        throw new Error(`Failed to load runs (${response.status})`);
      }
      const payload = (await response.json()) as { runs?: typeof runs };
      setRuns(payload.runs ?? []);
    } catch (err) {
      setRunsError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setRunsLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, [runtimeBase]);

  const handleSubmit = async () => {
    setResult(null);
    setError(null);
    setIsSubmitting(true);

    try {
      const parsedInput = JSON.parse(inputJson);
      const response = await fetch(`${runtimeBase}/runs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workflow_id: workflowId,
          input: parsedInput,
        }),
      });

      const payload = await response.json();
      if (!response.ok) {
        const message =
          payload?.detail ?? `Failed to create run (${response.status})`;
        throw new Error(`${message} | URL: ${runtimeBase}/runs`);
      }

      setResult(JSON.stringify(payload, null, 2));
      loadRuns();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h1 className="text-2xl font-semibold">Runs</h1>
          <p className="mt-2 text-sm text-slate-300">
            Create a run and inspect the response from the runtime API.
          </p>
        </div>
        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-lg font-semibold">Create a run</h2>
          <p className="mt-2 text-sm text-slate-300">
            Send a run request to the runtime API.
          </p>
          <p className="mt-2 text-xs text-slate-400">
            Runtime base:{" "}
            <span className="font-mono text-slate-200">{runtimeBase}</span>
          </p>
          <div className="mt-4 grid gap-4">
            <label className="text-xs uppercase text-slate-400">
              Workflow ID
              <input
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                value={workflowId}
                onChange={(event) => setWorkflowId(event.target.value)}
              />
            </label>
            <label className="text-xs uppercase text-slate-400">
              Input JSON
              <textarea
                className="mt-2 min-h-[120px] w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                value={inputJson}
                onChange={(event) => setInputJson(event.target.value)}
              />
            </label>
            <button
              className="w-fit rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:border-emerald-400 hover:text-emerald-300"
              type="button"
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Creating..." : "Create run"}
            </button>
            {error ? (
              <div className="rounded-lg border border-rose-800 bg-rose-950/40 px-4 py-3 text-sm text-rose-200">
                {error}
              </div>
            ) : null}
            {result ? (
              <div className="rounded-lg border border-slate-800 bg-slate-950 px-4 py-3">
                <p className="text-xs uppercase text-slate-400">
                  Response payload
                </p>
                <pre className="mt-2 overflow-auto text-xs text-slate-200">
                  {result}
                </pre>
              </div>
            ) : null}
          </div>
        </div>
        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Recent runs</h2>
            <button
              className="text-xs text-slate-300 hover:text-emerald-300"
              type="button"
              onClick={loadRuns}
            >
              Refresh
            </button>
          </div>
          {runsError ? (
            <p className="mt-3 text-sm text-rose-200">{runsError}</p>
          ) : null}
          <div className="mt-4 space-y-3">
            {runsLoading ? (
              <p className="text-sm text-slate-400">Loading runs...</p>
            ) : null}
            {(runs ?? []).map((run) => (
              <div
                key={run.run_id}
                className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm"
              >
                <div>
                  <p className="font-medium text-slate-100">
                    {run.workflow_id}
                  </p>
                  <p className="text-xs text-slate-400">{run.run_id}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs uppercase text-slate-400">
                    {run.status}
                  </p>
                  <p className="text-xs text-slate-500">{run.created_at}</p>
                </div>
              </div>
            ))}
            {runs && runs.length === 0 ? (
              <p className="text-sm text-slate-400">No runs yet.</p>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
}
