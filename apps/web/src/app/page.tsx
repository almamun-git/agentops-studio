import { HealthCard } from "@/components/HealthCard";
import { VersionCard } from "@/components/VersionCard";

export default function Home() {
  const runtimeBase =
    process.env.NEXT_PUBLIC_RUNTIME_BASE ?? "http://localhost:8000/api/v1";
  const endpoints = [
    { name: "Health", path: "/health", description: "Service heartbeat" },
    { name: "Version", path: "/version", description: "Runtime version info" },
    { name: "Runs", path: "/runs", description: "Create and inspect runs" },
    { name: "Memory", path: "/memory", description: "User memory store" },
    { name: "Eval", path: "/eval", description: "Evaluation runs" },
  ];

  return (
    <main className="mx-auto grid max-w-5xl gap-6 px-6 py-10 lg:grid-cols-[1.2fr_0.8fr]">
        <section className="space-y-6">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Runtime API</h2>
            <p className="mt-2 text-sm text-slate-300">
              Use the runtime API to start runs, inspect steps, and access
              memory.
            </p>
            <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 px-4 py-3">
              <p className="text-xs text-slate-400">Base URL</p>
              <p className="mt-1 break-all font-mono text-sm text-emerald-300">
                {runtimeBase}
              </p>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Core endpoints</h2>
            <ul className="mt-4 space-y-3">
              {endpoints.map((endpoint) => {
                const internalPath =
                  endpoint.path === "/runs"
                    ? "/runs"
                    : endpoint.path === "/memory"
                      ? "/memory"
                      : endpoint.path === "/eval"
                        ? "/eval"
                        : null;
                return (
                  <li
                    key={endpoint.path}
                    className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 px-4 py-3"
                  >
                    <div>
                      <p className="text-sm font-medium">{endpoint.name}</p>
                      <p className="text-xs text-slate-400">
                        {endpoint.description}
                      </p>
                    </div>
                    {internalPath ? (
                      <a
                        className="text-xs font-mono text-slate-200 hover:text-emerald-300"
                        href={internalPath}
                      >
                        {endpoint.path}
                      </a>
                    ) : (
                      <a
                        className="text-xs font-mono text-slate-200 hover:text-emerald-300"
                        href={`${runtimeBase}${endpoint.path}`}
                        target="_blank"
                        rel="noreferrer"
                      >
                        {endpoint.path}
                      </a>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </section>

        <aside className="space-y-6">
          <HealthCard />
          <VersionCard />
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Quick start</h2>
            <ol className="mt-3 space-y-2 text-sm text-slate-300">
              <li>1. Start the runtime: <code>make dev-runtime</code></li>
              <li>2. Open the runtime docs: {runtimeBase}</li>
              <li>3. Use the pages below to create runs, inspect steps, manage memory, and launch evals.</li>
            </ol>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Status</h2>
            <p className="mt-2 text-sm text-slate-300">
              Console includes run creation, run traces, memory store, and eval
              dashboards. Health and version are checked live above.
            </p>
          </div>
        </aside>
    </main>
  );
}
