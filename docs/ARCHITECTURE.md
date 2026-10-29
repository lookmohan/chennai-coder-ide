# Architecture

Describes what is built now, plus the decisions that constrain later phases.

## Shape

```
Browser ──► Next.js (App Router)  ──/api/v1/* proxy──►  FastAPI  ──► MySQL 8
                                                          │
                                                          ├──► Redis (rate limits, Celery broker)
                                                          └──► Celery worker (execution jobs, from Phase 2)
```

- **Same-origin proxy.** The browser never calls FastAPI directly. `next.config.mjs` rewrites `/api/v1/*` to `BACKEND_URL`, so cookies are first-party and CORS is not needed in practice (CORS is still configured on the backend as defense in depth).
- **Layering (backend):** `api/` (HTTP, validation, auth deps) → `services/` (business rules) → `repositories/` (queries) → `models/` (SQLAlchemy). Routes stay thin.
- **Server state (frontend):** TanStack Query only. No duplicate copies in a client store. `features/<area>/` holds hooks, schemas and types per area.
- **Response format:** success `{success: true, data, meta?}`; error `{success: false, error: {code, message, details?}}`. Stack traces never reach clients.

## Auth

Custom JWT (HS256, 60 min default) in an `httpOnly` cookie, plus a readable CSRF cookie. Cookie-authenticated mutations must echo it in `X-CSRF-Token`. Bearer tokens are accepted for API clients and skip CSRF. The token carries only the user id: **role and status are loaded from the database on each request**, so promotions, demotions and suspensions apply immediately. There is no refresh-token flow yet; sessions end when the token expires.

## Authorization

`require_roles(...)` dependency in `api/deps.py`. The frontend hides nothing for security; `/admin/*` returns 403 for students regardless of the UI. Resource-ownership checks (e.g. "own submissions only") are added with the resources they protect.

## Code execution (Phase 2 design, not built)

API creates a submission → enqueues a Celery task → worker calls a **Judge0-compatible service on a separate host/network** → results saved. Student code is never `exec`/`eval`'d in the API or worker process. Hidden test cases never leave the backend.

## Decisions to revisit

- Fixed-window rate limiting is simple but allows short bursts at window edges.
- Registration reveals whether an email/username exists (`409`). Acceptable for a learning platform; tighten if enumeration becomes a concern.
- Access tokens aren't revocable before expiry (suspension is still immediate because status is checked per request).
- MySQL has no `RETURNING`; server-generated values (timestamps) are read back with `db.refresh()` after writes.
