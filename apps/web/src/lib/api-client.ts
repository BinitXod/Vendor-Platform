// Client-side fetch wrapper. All calls go through the BFF proxy at
// /api/backend/*, so the browser never talks to FastAPI directly and
// BACKEND_URL stays server-side.

const BFF_PREFIX = "/api/backend";

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string,
    public body: unknown
  ) {
    super(detail || `HTTP ${status}`);
  }
}

async function request<T>(
  path: string,
  init: RequestInit & { json?: unknown } = {}
): Promise<T> {
  const { json, headers, ...rest } = init;

  const finalHeaders = new Headers(headers);
  let body: BodyInit | undefined = init.body ?? undefined;

  if (json !== undefined) {
    finalHeaders.set("Content-Type", "application/json");
    body = JSON.stringify(json);
  }

  const res = await fetch(`${BFF_PREFIX}${path}`, {
    ...rest,
    headers: finalHeaders,
    body,
  });

  if (res.status === 204) {
    return undefined as T;
  }

  const contentType = res.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await res.json().catch(() => null) : await res.text();

  if (!res.ok) {
    const detail =
      (payload && typeof payload === "object" && "detail" in payload
        ? String((payload as { detail: unknown }).detail)
        : null) ?? `Request failed (${res.status})`;
    throw new ApiError(res.status, detail, payload);
  }

  return payload as T;
}

export const api = {
  get: <T>(path: string) => request<T>(path, { method: "GET" }),
  post: <T>(path: string, json?: unknown) =>
    request<T>(path, { method: "POST", json }),
  patch: <T>(path: string, json?: unknown) =>
    request<T>(path, { method: "PATCH", json }),
  del: <T>(path: string) => request<T>(path, { method: "DELETE" }),
  postForm: <T>(path: string, form: FormData) =>
    request<T>(path, { method: "POST", body: form }),
};
