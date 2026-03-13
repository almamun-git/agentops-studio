AgentOps Studio web UI (Next.js + Tailwind).

## Getting Started

Install dependencies and run the dev server:

```bash
npm install
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) to view the UI.

Configure the runtime API base (optional):

```bash
export NEXT_PUBLIC_RUNTIME_BASE="http://localhost:8000/api/v1"
```

Or add `apps/web/.env.local` with:

```
NEXT_PUBLIC_RUNTIME_BASE=http://localhost:8000/api/v1
```

The home page uses `src/app/page.tsx`.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Notes

- This UI is a lightweight console for the runtime API.
- Extend it with pages for runs, memory, and evals as the backend matures.
- You can override the runtime base per-session by passing a `runtimeBase` query parameter in the URL (for example, `/?runtimeBase=http://localhost:8001/api/v1`).
- Each page shows the active runtime base in the header so you can confirm which environment you are connected to.
