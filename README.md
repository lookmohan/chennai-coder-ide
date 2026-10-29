# Chennai Coder

**Learn. Code. Build.** A coding education and practice platform: problems, a browser editor, sandboxed code execution, courses, contests, community, an AI mentor, and instructor monitoring.

> **Build status: Phase 1 (Foundation) written; not yet verified by running it.**
> Accounts, profiles, roles and the responsive app shell exist. The coding engine and everything after are **not built**. See [Roadmap](#roadmap).

## What exists today

| Area | Status |
|---|---|
| Monorepo, Docker Compose (mysql, redis, backend, worker) | Written |
| FastAPI under `/api/v1`, consistent error envelope | Written |
| MySQL 8 models + Alembic migration `0001` (users, profiles, audit_logs) | Written |
| Auth: register / login / logout / me (argon2, JWT httpOnly cookie, CSRF double-submit) | Written |
| Roles enforced server-side from the DB on every request | Written |
| Rate limiting, audit log, JSON logging, `python -m app.create_admin` | Written |
| `GET /admin/students` (account data only) | Written |
| Next.js frontend: landing, login, register, dashboard, profile | Written |
| Design tokens (light/dark/system), responsive sidebar + bottom nav, a11y basics | Written |
| Backend tests (pytest) and frontend tests (vitest) | Written, **never run** |
| Problems, editor, execution, submissions, progress, courses, contests, community, AI mentor, notifications, admin UI | **Not started** |

"Written" means the code exists, not that it has been run. First step on a new machine: run both test suites and fix what fails.

Navigation items for unbuilt features are shown disabled with a "Soon" badge. The dashboard shows "Not enough data yet" instead of numbers, because there is no data source yet.

## Run it locally

Requirements: Python 3.12+, Node 20+, and **MySQL 8** (easiest via Docker, or the MySQL Installer for Windows). Redis is optional for now (rate limiting falls back to in-memory).

### 1. Database (Docker, recommended)

```bash
copy .env.example .env     # then set MYSQL_ROOT_PASSWORD, MYSQL_PASSWORD, JWT_SECRET
docker compose up -d mysql redis
docker compose ps          # wait until mysql is "healthy"
```

Prefer no Docker? Install MySQL 8 from dev.mysql.com, then create the database and user:

```sql
CREATE DATABASE chennai_coder CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chennai'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON chennai_coder.* TO 'chennai'@'localhost';
FLUSH PRIVILEGES;
```

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
copy .env.example .env          # set DATABASE_URL and JWT_SECRET
python -c "import secrets; print(secrets.token_urlsafe(48))"   # paste as JWT_SECRET
alembic upgrade head
alembic check
uvicorn app.main:app --reload   # http://localhost:8000/docs
```

`DATABASE_URL` looks like `mysql+pymysql://chennai:yourpassword@localhost:3306/chennai_coder?charset=utf8mb4`. Use letters and numbers only in the password.

### 3. Frontend

```bash
cd frontend
copy .env.example .env.local
npm install
npm run dev                     # http://localhost:3000
```

The browser only talks to Next.js. `/api/v1/*` is proxied to `BACKEND_URL` (default `http://localhost:8000`), so auth cookies are first-party. There is no `NEXT_PUBLIC_API_URL`.

### 4. First admin

```bash
cd backend
python -m app.create_admin --email you@example.com --username mohanraj --display-name "Mohanraj"
```

Prompts for a password (or set `ADMIN_PASSWORD`). There is deliberately no HTTP endpoint for this.

### 5. Tests

```bash
cd backend && pytest                  # in-memory SQLite, no MySQL/Redis needed
cd frontend && npm test && npm run typecheck && npm run lint
```

## Docs

[ARCHITECTURE](docs/ARCHITECTURE.md) · [SECURITY](docs/SECURITY.md) · [API](docs/API.md) · [DATABASE](docs/DATABASE.md) · [BRAND](docs/BRAND.md). `DEPLOYMENT.md` will be written once there is a deployable product.

## Roadmap

1. **Foundation**: written; verify by running tests
2. Coding engine (problems, Monaco, Judge0-compatible execution, submissions)
3. Student progress (events, dashboard, streak, XP)
4. Instructor (admin dashboard, student monitoring, timeline)
5. Community
6. AI Mentor
7. Courses
8. Contests
9. Notifications, achievements, analytics, accessibility, performance, deployment

## Manual setup needed in later phases (not done)

Judge0-compatible execution service on a separate host, AI provider key, S3-compatible bucket, SMTP, OAuth credentials (optional), production domain/HTTPS, backups, monitoring.

## Troubleshooting

- **`JWT_SECRET must be set and at least 32 characters`**: backend refuses to start without it; generate one as above.
- **`Access denied for user`**: `DATABASE_URL` user/password doesn't match the MySQL user. With Docker, they must equal `MYSQL_USER` / `MYSQL_PASSWORD` in the root `.env`.
- **`Can't connect to MySQL server`**: MySQL isn't running yet (`docker compose ps`) or the port is wrong.
- **`cryptography package is required`**: run `pip install -r requirements-dev.txt` again.
- **Frontend shows "service temporarily unavailable"**: backend isn't running or `BACKEND_URL` is wrong.
- **Redirected to /login in a loop**: clear cookies for `localhost`; a stale `cc_access` cookie is the usual cause.
- **Password with `@`, `#`, `/` breaks the URL**: use letters and numbers only, or URL-encode it.
