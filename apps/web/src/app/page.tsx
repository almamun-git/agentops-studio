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
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-6">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
              AgentOps Studio
            </p>
            <h1 className="text-2xl font-semibold">Runtime Console</h1>
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-300">
            <a
              className="rounded-full border border-slate-700 px-3 py-1 hover:border-emerald-400 hover:text-emerald-300"
              href="/runs"
            >
              Runs
            </a>
            <span className="rounded-full border border-slate-700 px-3 py-1">
              Early Preview
            </span>
          </div>
        </div>
      </header>

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
              {endpoints.map((endpoint) => (
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
                  <a
                    className="text-xs font-mono text-slate-200 hover:text-emerald-300"
                    href={`${runtimeBase}${endpoint.path}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {endpoint.path}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <aside className="space-y-6">
          <HealthCard />
          <VersionCard />
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Quick start</h2>
            <ol className="mt-3 space-y-2 text-sm text-slate-300">
              <li>1. Start the runtime: `make dev-runtime`</li>
              <li>2. Open the runtime docs: {runtimeBase}</li>
              <li>3. Create a run and inspect it in this UI.</li>
            </ol>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
            <h2 className="text-lg font-semibold">Status</h2>
            <p className="mt-2 text-sm text-slate-300">
              This UI is a lightweight console. Next: add run creation and live
              status checks.
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
}
