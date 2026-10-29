import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError, api } from "@/lib/api";

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

describe("api client", () => {
  const fetchMock = vi.fn();

  beforeEach(() => {
    vi.stubGlobal("fetch", fetchMock);
    document.cookie = "cc_csrf=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
  });

  afterEach(() => {
    fetchMock.mockReset();
    vi.unstubAllGlobals();
  });

  it("returns data and meta from a success envelope", async () => {
    fetchMock.mockResolvedValue(json({ success: true, data: { ok: 1 }, meta: { total: 3 } }));
    const res = await api<{ ok: number }>("/thing");
    expect(res.data).toEqual({ ok: 1 });
    expect(res.meta).toEqual({ total: 3 });
    expect(fetchMock.mock.calls[0][0]).toBe("/api/v1/thing");
  });

  it("throws ApiError with the backend code, message and field details", async () => {
    fetchMock.mockResolvedValue(
      json(
        {
          success: false,
          error: { code: "VALIDATION_ERROR", message: "Some fields are invalid", details: [{ field: "email", message: "bad" }] },
        },
        422,
      ),
    );
    const err = await api("/auth/register", { method: "POST", body: {} }).catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.code).toBe("VALIDATION_ERROR");
    expect(err.status).toBe(422);
    expect(err.details).toEqual([{ field: "email", message: "bad" }]);
  });

  it("maps a network failure to NETWORK_ERROR", async () => {
    fetchMock.mockRejectedValue(new TypeError("Failed to fetch"));
    const err = await api("/x").catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.code).toBe("NETWORK_ERROR");
    expect(err.status).toBe(0);
  });

  it("maps a non-JSON 5xx (e.g. backend down behind the proxy) to SERVICE_UNAVAILABLE", async () => {
    fetchMock.mockResolvedValue(new Response("Internal Server Error", { status: 500 }));
    const err = await api("/x").catch((e) => e);
    expect(err.code).toBe("SERVICE_UNAVAILABLE");
  });

  it("sends the CSRF header on mutations but not on GET", async () => {
    document.cookie = "cc_csrf=token123; path=/";
    // A Response body can only be read once, so return a fresh one per call.
    fetchMock.mockImplementation(() => Promise.resolve(json({ success: true, data: {} })));

    await api("/users/me", { method: "PATCH", body: { bio: "x" } });
    expect(fetchMock.mock.calls[0][1].headers["X-CSRF-Token"]).toBe("token123");

    await api("/auth/me");
    expect(fetchMock.mock.calls[1][1].headers["X-CSRF-Token"]).toBeUndefined();
  });
});
