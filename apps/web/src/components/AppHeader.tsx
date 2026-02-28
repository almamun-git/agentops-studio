"use client";

export function AppHeader() {
  return (
    <header className="border-b border-slate-800">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-6">
        <a href="/" className="block">
          <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
            AgentOps Studio
          </p>
          <h1 className="text-2xl font-semibold">Runtime Console</h1>
        </a>
        <nav className="flex items-center gap-3 text-xs text-slate-300">
          <a
            className="rounded-full border border-slate-700 px-3 py-1 hover:border-emerald-400 hover:text-emerald-300"
            href="/"
          >
            Home
          </a>
          <a
            className="rounded-full border border-slate-700 px-3 py-1 hover:border-emerald-400 hover:text-emerald-300"
            href="/runs"
          >
            Runs
          </a>
          <a
            className="rounded-full border border-slate-700 px-3 py-1 hover:border-emerald-400 hover:text-emerald-300"
            href="/memory"
          >
            Memory
          </a>
          <a
            className="rounded-full border border-slate-700 px-3 py-1 hover:border-emerald-400 hover:text-emerald-300"
            href="/eval"
          >
            Eval
          </a>
          <span className="rounded-full border border-slate-700 px-3 py-1">
            Early Preview
          </span>
        </nav>
      </div>
    </header>
  );
}
