const defaultApiBase = "http://localhost:8000/api/v1";

export function getRuntimeBase(): string {
  const raw =
    typeof window === "undefined"
      ? process.env.NEXT_PUBLIC_RUNTIME_BASE
      : window.__NEXT_DATA__?.query?.runtimeBase ?? process.env.NEXT_PUBLIC_RUNTIME_BASE;
  const base = raw && typeof raw === "string" && raw.length > 0 ? raw : defaultApiBase;
  if (base.startsWith("http://") || base.startsWith("https://")) {
    return base;
  }
  if (base.startsWith("/")) {
    return `http://localhost:8000${base}`;
  }
  return base;
}
