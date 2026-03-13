"use client";

import { useState } from "react";

import { formatTimestamp } from "@/lib/format";
import { getRuntimeBase } from "@/lib/runtime";

type MemoryItem = {
  memory_id: string;
  user_id: string;
  key: string;
  value: Record<string, unknown>;
  metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string | null;
};

export default function MemoryPage() {
  const runtimeBase = getRuntimeBase();
  const [userId, setUserId] = useState("demo-user");
  const [items, setItems] = useState<MemoryItem[] | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [upsertKey, setUpsertKey] = useState("");
  const [upsertValue, setUpsertValue] = useState('{}');
  const [upserting, setUpserting] = useState(false);
  const [upsertError, setUpsertError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const loadMemory = async () => {
    setLoadError(null);
    setLoading(true);
    try {
      const response = await fetch(`${runtimeBase}/memory/${encodeURIComponent(userId)}`);
      if (!response.ok) {
        throw new Error(`Failed to load memory (${response.status})`);
      }
      const payload = (await response.json()) as { user_id: string; items: MemoryItem[] };
      setItems(payload.items ?? []);
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : "Unknown error");
      setItems(null);
    } finally {
      setLoading(false);
    }
  };

  const handleUpsert = async () => {
    if (!upsertKey.trim()) return;
    setUpsertError(null);
    setUpserting(true);
    try {
      let value: Record<string, unknown>;
      try {
        value = JSON.parse(upsertValue) as Record<string, unknown>;
      } catch {
        throw new Error("Value must be valid JSON");
      }
      const response = await fetch(`${runtimeBase}/memory/${encodeURIComponent(userId)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: [{ key: upsertKey.trim(), value }] }),
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data?.detail ?? `Upsert failed (${response.status})`);
      }
      setUpsertKey("");
      setUpsertValue("{}");
      await loadMemory();
    } catch (err) {
      setUpsertError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setUpserting(false);
    }
  };

  const handleDelete = async (memoryId: string) => {
    setDeletingId(memoryId);
    try {
      const response = await fetch(
        `${runtimeBase}/memory/${encodeURIComponent(userId)}/${encodeURIComponent(memoryId)}`,
        { method: "DELETE" }
      );
      if (!response.ok) throw new Error(`Delete failed (${response.status})`);
      await loadMemory();
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <nav className="mb-4 flex flex-wrap items-center justify-between gap-2 text-sm">
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
          <h1 className="text-2xl font-semibold">Memory</h1>
          <p className="mt-2 text-sm text-slate-300">
            View and edit user memory by user ID.
          </p>
        </div>

        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-lg font-semibold">Load memory</h2>
          <p className="mt-2 text-xs text-slate-400">
            Runtime base: <span className="font-mono text-slate-200">{runtimeBase}</span>
          </p>
          <div className="mt-4 flex flex-wrap items-end gap-3">
            <label className="text-xs uppercase text-slate-400" htmlFor="user-id">
              User ID
              <input
                id="user-id"
                className="mt-2 block w-56 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
              />
            </label>
            <button
              type="button"
              onClick={loadMemory}
              disabled={loading}
              className="rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:border-emerald-400 hover:text-emerald-300 disabled:opacity-50"
            >
              {loading ? "Loading..." : "Load"}
            </button>
          </div>
          {loadError ? (
            <p className="mt-3 text-sm text-rose-200">{loadError}</p>
          ) : null}
        </div>

        {items !== null ? (
          <>
            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <h2 className="text-lg font-semibold">Add or update</h2>
              <div className="mt-4 grid gap-4">
                <label className="text-xs uppercase text-slate-400" htmlFor="memory-key">
                  Key
                  <input
                    id="memory-key"
                    className="mt-2 w-full max-w-md rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100"
                    value={upsertKey}
                    onChange={(e) => setUpsertKey(e.target.value)}
                  />
                </label>
                <label className="text-xs uppercase text-slate-400" htmlFor="memory-value">
                  Value (JSON)
                  <textarea
                    id="memory-value"
                    className="mt-2 min-h-[80px] w-full max-w-md rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm text-slate-100"
                    value={upsertValue}
                    onChange={(e) => setUpsertValue(e.target.value)}
                  />
                </label>
                <button
                  type="button"
                  onClick={handleUpsert}
                  disabled={upserting || !upsertKey.trim()}
                  className="w-fit rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:border-emerald-400 hover:text-emerald-300 disabled:opacity-50"
                >
                  {upserting ? "Saving..." : "Save"}
                </button>
                {upsertError ? (
                  <p className="text-sm text-rose-200">{upsertError}</p>
                ) : null}
              </div>
            </div>

            <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Items</h2>
                <button
                  type="button"
                  onClick={loadMemory}
                  className="text-xs text-slate-300 hover:text-emerald-300"
                >
                  Refresh
                </button>
              </div>
              <div className="mt-4 space-y-3">
                {items.length === 0 ? (
                  <p className="text-sm text-slate-400">No memory items.</p>
                ) : (
                  items.map((item) => (
                    <div
                      key={item.memory_id}
                      className="rounded-xl border border-slate-800 bg-slate-950 px-4 py-3"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="min-w-0 flex-1">
                          <p className="font-medium text-slate-100">{item.key}</p>
                          <p className="mt-1 font-mono text-xs text-slate-400">
                            {item.memory_id}
                          </p>
                          <pre className="mt-2 overflow-auto text-xs text-slate-300">
                            {JSON.stringify(item.value, null, 2)}
                          </pre>
                          <p className="mt-2 text-xs text-slate-500">
                            Created {formatTimestamp(item.created_at)}
                            {item.updated_at
                              ? ` · Updated ${formatTimestamp(item.updated_at)}`
                              : ""}
                          </p>
                        </div>
                        <button
                          type="button"
                          onClick={() => handleDelete(item.memory_id)}
                          disabled={deletingId === item.memory_id}
                          className="shrink-0 text-xs text-rose-400 hover:text-rose-300 disabled:opacity-50"
                        >
                          {deletingId === item.memory_id ? "Deleting..." : "Delete"}
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </>
        ) : null}
      </div>
    </div>
  );
}
