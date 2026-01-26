"use client";

import { useState } from "react";

const defaultRuntimeBase = "http://localhost:8000/api/v1";

export default function RunsPage() {
  const runtimeBase =
    process.env.NEXT_PUBLIC_RUNTIME_BASE ?? defaultRuntimeBase;
  const [workflowId, setWorkflowId] = useState("demo-workflow");
  const [inputJson, setInputJson] = useState('{"prompt":"hello"}');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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
        throw new Error(payload?.detail ?? "Failed to create run");
      }

      setResult(JSON.stringify(payload, null, 2));
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
            This page will list workflow runs and their status. Next: add a
            simple create-run form and table view.
          </p>
        </div>
        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-lg font-semibold">Create a run</h2>
          <p className="mt-2 text-sm text-slate-300">
            Send a run request to the runtime API.
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
      </div>
    </div>
  );
}
