"use client";

import { useEffect, useState } from "react";

type VersionPayload = {
  version: string;
  api_version: string;
};

type VersionState =
  | { state: "idle" | "loading" }
  | { state: "ready"; payload: VersionPayload }
  | { state: "error"; message: string };

const defaultRuntimeBase = "http://localhost:8000/api/v1";

export function VersionCard() {
  const [version, setVersion] = useState<VersionState>({ state: "idle" });
  const runtimeBase =
    process.env.NEXT_PUBLIC_RUNTIME_BASE ?? defaultRuntimeBase;

  useEffect(() => {
    let cancelled = false;

    const loadVersion = async () => {
      try {
        setVersion({ state: "loading" });
        const response = await fetch(`${runtimeBase}/version`);
        if (!response.ok) {
          throw new Error(`Version check failed (${response.status})`);
        }
        const payload = (await response.json()) as VersionPayload;
        if (!cancelled) {
          setVersion({ state: "ready", payload });
        }
      } catch (error) {
        if (!cancelled) {
          setVersion({
            state: "error",
            message: error instanceof Error ? error.message : "Unknown error",
          });
        }
      }
    };

    loadVersion();
    return () => {
      cancelled = true;
    };
  }, [runtimeBase]);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
      <h2 className="text-lg font-semibold">Runtime version</h2>
      <p className="mt-2 text-sm text-slate-300">
        Confirm the API version the UI is talking to.
      </p>
      <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">
        {version.state === "idle" || version.state === "loading" ? (
          <p className="text-xs text-slate-400">Fetching version...</p>
        ) : null}
        {version.state === "ready" ? (
          <div className="space-y-1 text-xs text-slate-300">
            <p>Runtime: {version.payload.version}</p>
            <p>API: {version.payload.api_version}</p>
          </div>
        ) : null}
        {version.state === "error" ? (
          <div>
            <p className="text-xs uppercase text-rose-300">Unavailable</p>
            <p className="mt-1 text-xs text-slate-400">{version.message}</p>
          </div>
        ) : null}
      </div>
    </div>
  );
}
