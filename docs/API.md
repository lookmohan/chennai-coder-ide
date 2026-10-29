# API (v1)

Base path: `/api/v1`. Interactive docs at `/docs` in development (disabled in production).

**Success:** `{ "success": true, "data": ..., "meta": ... }`
**Error:** `{ "success": false, "error": { "code": "...", "message": "...", "details": [...] } }`

Auth: session cookie (send `X-CSRF-Token` on POST/PATCH/PUT/DELETE) or `Authorization: Bearer <token>`.

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | none | Liveness |
| GET | `/health/ready` | none | Readiness (checks DB); 503 `DATABASE_UNAVAILABLE` |
| POST | `/auth/register` | none | Create student account, sets cookies. 201 / 409 `EMAIL_TAKEN` `USERNAME_TAKEN` / 422 / 429 |
| POST | `/auth/login` | none | Sets cookies. 401 `INVALID_CREDENTIALS` / 403 `ACCOUNT_SUSPENDED` / 429 `RATE_LIMITED` |
| POST | `/auth/logout` | none | Clears cookies |
| GET | `/auth/me` | any user | Current user + profile |
| GET | `/users/me` | any user | Same as `/auth/me` |
| PATCH | `/users/me` | any user | Update profile. Send only fields to change; `null` clears optional fields; `display_name` can't be null/blank |
| GET | `/users/{username}` | none | Public profile (no email/role/status/id). 404 `USER_NOT_FOUND` |
| GET | `/admin/students?page&page_size&q` | instructor, admin | Paginated students (`page_size` max 100). `meta: {page, page_size, total}` |

## Error codes

`NOT_AUTHENTICATED` 401 · `TOKEN_EXPIRED` 401 · `INVALID_TOKEN` 401 · `INVALID_CREDENTIALS` 401 · `FORBIDDEN` 403 · `CSRF_FAILED` 403 · `ACCOUNT_SUSPENDED` 403 · `NOT_FOUND` / `USER_NOT_FOUND` 404 · `EMAIL_TAKEN` / `USERNAME_TAKEN` 409 · `VALIDATION_ERROR` 422 · `RATE_LIMITED` 429 (with `Retry-After`) · `INTERNAL_ERROR` 500 · `DATABASE_UNAVAILABLE` 503
