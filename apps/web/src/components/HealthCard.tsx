"use client";

import { useEffect, useState } from "react";

type HealthPayload = {
  status: "ok" | "error";
  timestamp: string;
};

type HealthState =
  | { state: "idle" | "loading" }
  | { state: "ready"; payload: HealthPayload }
  | { state: "error"; message: string };

const defaultRuntimeBase = "http://localhost:8000/api/v1";

export function HealthCard() {
  const [health, setHealth] = useState<HealthState>({ state: "idle" });
  const runtimeBase =
    process.env.NEXT_PUBLIC_RUNTIME_BASE ?? defaultRuntimeBase;

  useEffect(() => {
    let cancelled = false;

    const loadHealth = async () => {
      try {
        setHealth({ state: "loading" });
        const response = await fetch(`${runtimeBase}/health`);
        if (!response.ok) {
          throw new Error(`Health check failed (${response.status})`);
        }
        const payload = (await response.json()) as HealthPayload;
        if (!cancelled) {
          setHealth({ state: "ready", payload });
        }
      } catch (error) {
        if (!cancelled) {
          setHealth({
            state: "error",
            message: error instanceof Error ? error.message : "Unknown error",
          });
        }
      }
    };

    loadHealth();
    return () => {
      cancelled = true;
    };
  }, [runtimeBase]);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
      <h2 className="text-lg font-semibold">Runtime health</h2>
      <p className="mt-2 text-sm text-slate-300">
        Ping the runtime API to verify connectivity.
      </p>
      <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">
        {health.state === "idle" || health.state === "loading" ? (
          <p className="text-xs text-slate-400">Checking runtime...</p>
        ) : null}
        {health.state === "ready" ? (
          <div>
            <p className="text-xs uppercase text-emerald-300">Healthy</p>
            <p className="mt-1 text-xs text-slate-400">
              {health.payload.timestamp}
            </p>
          </div>
        ) : null}
        {health.state === "error" ? (
          <div>
            <p className="text-xs uppercase text-rose-300">Unavailable</p>
            <p className="mt-1 text-xs text-slate-400">{health.message}</p>
          </div>
        ) : null}
      </div>
    </div>
  );
}
