# Database

**MySQL 8.0.16 or newer** (8.4 in Docker Compose). SQLAlchemy 2.0 models in `backend/app/models/`, migrations in `backend/alembic/versions/`, driver `PyMySQL` (pure Python, no compiler needed on Windows) plus `cryptography` (required by MySQL 8's default login method).

> MariaDB and XAMPP are **not** tested. MySQL 8 is the target. CHECK constraints need MySQL 8.0.16+.

Connection URL: `mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE?charset=utf8mb4`

## Design notes

- **Charset:** `utf8mb4` / `utf8mb4_unicode_ci` everywhere (full Unicode, case-insensitive comparisons).
- **UUID keys:** stored as `CHAR(32)`.
- **Datetimes:** MySQL has no timezone-aware column. All times are stored as **naive UTC** and the session is forced to UTC (`SET time_zone = '+00:00'`). The `UTCDateTime` type in `models/base.py` converts on the way in and returns timezone-aware values on the way out, so the API emits `...Z` timestamps. Never write naive datetimes (the type raises an error).
- **Names:** constraint/index names follow a fixed naming convention (`models/base.py`). After the first successful `alembic upgrade head`, run `alembic check` to confirm the migration matches the models.

## Tables (migration `0001`)

**users**: `id` (pk), `email` (unique), `password_hash` (nullable, for future OAuth-only accounts), `external_auth_provider` + `external_auth_id` (unique together), `role` (`student|instructor|admin|moderator`, check constraint, indexed), `status` (`active|suspended|deactivated`, check constraint), `last_login_at`, `created_at`, `updated_at`.

**profiles** (1:1 with users, cascade delete): `user_id` (pk, fk), `display_name`, `username` (unique), `avatar_url`, `bio`, `github_url`, `linkedin_url`, `website_url`, `location`, timestamps.

**audit_logs** (append-only): `id`, `actor_id` (fk, `SET NULL` on user delete), `action`, `entity_type`, `entity_id`, `metadata` (JSON, never secrets), `ip`, `created_at`.

## Conventions for upcoming tables

UUID primary keys, `UTCDateTime` for every timestamp, explicit indexes for every filter/sort used by list endpoints, check constraints for enum-like columns. Hidden test cases get their own table and are never selected by any schema returned to the frontend.

## Tests

Backend tests build tables from the models on in-memory SQLite, so they cover application logic but **not** the Alembic migration or MySQL behavior. Verify the migration on real MySQL (`alembic upgrade head`, then `alembic check`).

## Handy commands (Docker)

```
docker compose exec mysql mysql -uchennai -p chennai_coder -e "SHOW TABLES;"
docker compose exec mysql mysql -uchennai -p chennai_coder -e "SELECT email, role, status FROM users;"
```
