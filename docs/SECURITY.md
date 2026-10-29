# Security

Status of controls in the current build. "Planned" items do not exist yet.

| Control | Status | Notes |
|---|---|---|
| Password hashing | Done | Argon2id (argon2-cffi defaults), rehash on login if parameters change |
| Password policy | Done | 10-128 chars, at least one letter and one number |
| Session cookie | Done | `httpOnly`, `SameSite=Lax`, `Secure` via `COOKIE_SECURE` (**required** when `ENV=production`; backend refuses to start otherwise) |
| CSRF | Done | Double-submit token for cookie-authenticated mutations |
| Authorization | Done (roles) | Role read from DB per request; 401 vs 403 distinguished. Ownership checks come with each resource |
| Login timing | Done | Dummy hash verification for unknown emails; identical error for wrong password and unknown email |
| Rate limiting | Done | Login (per IP and per email), registration. Redis-backed; in-memory fallback is per-process |
| Input validation | Done | Pydantic on every body; URLs restricted to http(s) (blocks `javascript:`) |
| SQL injection | Done | ORM / bound parameters only |
| XSS | Partly | React escapes output; user text is never rendered as HTML. Re-check when community/markdown rendering is added |
| Security headers | Done | nosniff, frame deny, referrer policy on API and web; CSP **planned** |
| Secrets | Done | Only via env; `.gitignore` excludes `.env*` (examples excluded from the ignore) |
| Logging | Done | JSON; request path/status/duration only; failed logins log a hash of the email, never passwords/tokens |
| Audit log | Partly | Register/login/admin-promote recorded. Moderation and admin actions added with those features |
| Docs/OpenAPI | Done | `/docs` disabled when `ENV=production` |
| File uploads | Planned | Type/MIME/size validation, object storage |
| Code sandbox isolation | Planned | Judge0-compatible runner on a separate host/network, never in the API trust boundary |
| AI guardrails | Planned | Server-side solution-request detection plus per-student limits |
| OAuth (Google/GitHub) | Planned | Optional |
| Password reset / email verification | Planned | Needs SMTP |

## Behind a proxy

Rate limiting uses `request.client.host`. Run uvicorn with `--proxy-headers` and a **restricted** `--forwarded-allow-ips` (the compose file uses `*` for local development only; do not do that on a public host).

## Reporting

Email the maintainers privately; do not open a public issue for vulnerabilities.
