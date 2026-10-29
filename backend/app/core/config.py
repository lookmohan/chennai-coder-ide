from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"  # development | test | production
    database_url: str = "mysql+pymysql://chennai:chennai@localhost:3306/chennai_coder?charset=utf8mb4"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = ""
    jwt_expires_minutes: int = 60

    # Public address of the website. Sign-in with Google/GitHub returns to <PUBLIC_APP_URL>/api/v1/...
    public_app_url: str = "http://localhost:3000"

    cors_origins: str = "http://localhost:3000"
    cookie_secure: bool = False
    cookie_domain: str | None = None

    # Sign-in with Google / GitHub. Leave empty to hide the buttons.
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""

    rate_login_per_minute: int = 10
    rate_login_per_email_per_15min: int = 10
    rate_register_per_hour: int = 10
    submission_rate_per_minute: int = 10

    # Server-side submissions are switched off. Practice runs in the browser (Pyodide).
    # The judging code is kept so official grading can be switched on later.
    submissions_enabled: bool = False

    ai_mentor_daily_limit: int = 10

    # How judging jobs run (only matters when submissions_enabled is true):
    #   thread - in-process background thread. For local development on Windows (no Redis needed).
    #   celery - Redis-backed worker. Needed in production only if submissions are on.
    queue_mode: str = "thread"

    # Which code runner grades submissions (only used when submissions_enabled is true):
    #   ""       - none. Submissions are refused with a clear message (the default).
    #   "piston" - Piston API (free public instance by default, see piston_url).
    #   "judge0" - a Judge0-compatible server at judge0_url.
    runner: str = ""
    piston_url: str = "https://emkc.org/api/v2/piston"
    judge0_url: str = ""
    judge0_api_key: str = ""
    judge0_timeout_seconds: float = 15.0

    @model_validator(mode="after")
    def _validate(self) -> "Settings":
        if len(self.jwt_secret) < 32:
            raise ValueError(
                "JWT_SECRET must be set and at least 32 characters. "
                'Generate one: python -c "import secrets; print(secrets.token_urlsafe(48))"'
            )
        if self.env == "production" and not self.cookie_secure:
            raise ValueError("COOKIE_SECURE must be true when ENV=production")
        if self.queue_mode not in ("thread", "celery"):
            raise ValueError("QUEUE_MODE must be 'thread' or 'celery'")
        # A Redis worker is only required when submissions are actually switched on.
        if self.env == "production" and self.submissions_enabled and self.queue_mode != "celery":
            raise ValueError("QUEUE_MODE must be 'celery' when ENV=production and submissions are enabled")
        if self.runner not in ("", "piston", "judge0"):
            raise ValueError("RUNNER must be empty, 'piston' or 'judge0'")
        if self.cookie_domain == "":
            self.cookie_domain = None
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
