import os

# Must be set before the app (and Settings) are imported.
os.environ["ENV"] = "test"
os.environ["JWT_SECRET"] = "test-secret-" + "x" * 40
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["COOKIE_SECURE"] = "false"
os.environ["RATE_LOGIN_PER_MINUTE"] = "1000"
os.environ["RATE_LOGIN_PER_EMAIL_PER_15MIN"] = "1000"
os.environ["RATE_REGISTER_PER_HOUR"] = "1000"
os.environ["SUBMISSION_RATE_PER_MINUTE"] = "1000"
# Server-side submissions are off by default. The submission tests turn them on explicitly.
os.environ["SUBMISSIONS_ENABLED"] = "true"
# Override anything from a developer's .env so tests always start with the runner off.
os.environ["RUNNER"] = ""
os.environ["JUDGE0_URL"] = ""
os.environ["QUEUE_MODE"] = "thread"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.core.database import get_db  # noqa: E402
from app.core.rate_limit import reset_rate_limits  # noqa: E402
from app.main import create_app  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_limits():
    reset_rate_limits()
    yield
    reset_rate_limits()


@pytest.fixture()
def session_factory():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture()
def app(session_factory):
    application = create_app()

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    application.dependency_overrides[get_db] = override_get_db
    return application


@pytest.fixture()
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def new_client(app):
    """Factory for independent clients (separate cookie jars)."""
    clients = []

    def factory() -> TestClient:
        c = TestClient(app)
        clients.append(c)
        return c

    yield factory
    for c in clients:
        c.close()
