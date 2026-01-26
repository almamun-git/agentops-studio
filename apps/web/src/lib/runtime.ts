const defaultApiBase = "http://localhost:8000/api/v1";

export function getRuntimeBase(): string {
  const base = process.env.NEXT_PUBLIC_RUNTIME_BASE ?? defaultApiBase;
  if (base.startsWith("http://") || base.startsWith("https://")) {
    return base;
  }
  if (base.startsWith("/")) {
    return `http://localhost:8000${base}`;
  }
  return base;
}
