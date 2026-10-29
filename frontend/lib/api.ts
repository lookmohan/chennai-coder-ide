export type FieldError = { field: string; message: string };

export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public details?: FieldError[],
  ) {
    super(message);
    this.name = "ApiError";
  }
}

const BASE = "/api/v1";

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

type Options = { method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE"; body?: unknown; signal?: AbortSignal };

export type ApiResult<T> = { data: T; meta?: Record<string, unknown> };

export async function api<T>(path: string, opts: Options = {}): Promise<ApiResult<T>> {
  const method = opts.method ?? "GET";
  const headers: Record<string, string> = { Accept: "application/json" };
  if (opts.body !== undefined) headers["Content-Type"] = "application/json";
  if (method !== "GET") {
    // Double-submit CSRF: echo the readable cookie in a header.
    const csrf = getCookie("cc_csrf");
    if (csrf) headers["X-CSRF-Token"] = csrf;
  }

  let res: Response;
  try {
    res = await fetch(BASE + path, {
      method,
      headers,
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
      credentials: "same-origin",
      signal: opts.signal,
    });
  } catch (err) {
    if (err instanceof DOMException && err.name === "AbortError") throw err;
    throw new ApiError("NETWORK_ERROR", "Can't reach the server. Check your connection and try again.", 0);
  }

  let json: any = null;
  try {
    json = await res.json();
  } catch {
    /* non-JSON body (e.g. proxy error page) */
  }

  if (!res.ok || !json || json.success === false) {
    const e = json?.error;
    if (!e && res.status >= 500) {
      throw new ApiError("SERVICE_UNAVAILABLE", "The service is temporarily unavailable. Please try again shortly.", res.status);
    }
    throw new ApiError(
      e?.code ?? "UNKNOWN_ERROR",
      e?.message ?? "Something went wrong. Please try again.",
      res.status,
      e?.details,
    );
  }
  return { data: json.data as T, meta: json.meta ?? undefined };
}
