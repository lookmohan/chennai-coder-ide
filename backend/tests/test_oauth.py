from app.models import User
from app.security.oauth import OAuthProfile
from tests.helpers import register


def _enable(monkeypatch, profile: OAuthProfile | None = None, error: Exception | None = None):
    monkeypatch.setattr("app.api.v1.oauth.provider_configured", lambda provider: True)

    def fake_fetch(provider, code):
        if error is not None:
            raise error
        return profile

    monkeypatch.setattr("app.api.v1.oauth.fetch_profile", fake_fetch)


def _google(email="person@example.com", verified=True, external_id="g-123"):
    return OAuthProfile(
        provider="google",
        external_id=external_id,
        email=email,
        email_verified=verified,
        display_name="Person One",
        username_hint="person.one",
        avatar_url=None,
    )


def test_providers_report_on_off_without_secrets(client):
    res = client.get("/api/v1/auth/oauth/providers")
    assert res.json()["data"] == {"google": False, "github": False}
    assert "secret" not in res.text.lower()


def test_start_refused_when_provider_not_configured(client):
    res = client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    assert res.status_code == 503
    assert res.json()["error"]["code"] == "OAUTH_NOT_CONFIGURED"


def test_start_redirects_to_provider_with_state_cookie(client, monkeypatch):
    _enable(monkeypatch)
    res = client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    assert res.status_code == 302
    assert res.headers["location"].startswith("https://accounts.google.com/")
    assert client.cookies.get("cc_oauth_state")


def test_callback_rejects_missing_or_wrong_state(client, monkeypatch):
    _enable(monkeypatch, profile=_google())
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    res = client.get(
        "/api/v1/auth/oauth/google/callback?code=abc&state=not-the-right-state", follow_redirects=False
    )
    assert res.status_code == 302
    assert "error=oauth_state" in res.headers["location"]
    assert client.cookies.get("cc_access") is None


def test_new_person_gets_an_account_without_a_password(client, session_factory, monkeypatch):
    _enable(monkeypatch, profile=_google())
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    state = client.cookies.get("cc_oauth_state")
    res = client.get(
        f"/api/v1/auth/oauth/google/callback?code=abc&state={state}", follow_redirects=False
    )
    assert res.status_code == 302
    assert res.headers["location"].endswith("/dashboard")
    assert client.cookies.get("cc_access")

    db = session_factory()
    try:
        user = db.query(User).filter(User.email == "person@example.com").one()
        assert user.password_hash is None
        assert user.external_auth_provider == "google"
        assert user.profile.username == "person_one"[:30] or user.profile.username.startswith("person")
    finally:
        db.close()


def test_verified_email_links_to_existing_account(client, session_factory, monkeypatch):
    register(client, email="person@example.com", username="existing_one")
    client.cookies.clear()
    _enable(monkeypatch, profile=_google(email="person@example.com", verified=True))
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    state = client.cookies.get("cc_oauth_state")
    client.get(f"/api/v1/auth/oauth/google/callback?code=abc&state={state}", follow_redirects=False)

    db = session_factory()
    try:
        users = db.query(User).filter(User.email == "person@example.com").all()
        assert len(users) == 1
        assert users[0].external_auth_provider == "google"
        assert users[0].profile.username == "existing_one"
    finally:
        db.close()


def test_unverified_email_never_links_to_existing_account(client, monkeypatch):
    register(client, email="person@example.com", username="existing_two")
    client.cookies.clear()
    _enable(monkeypatch, profile=_google(email="person@example.com", verified=False))
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    state = client.cookies.get("cc_oauth_state")
    res = client.get(
        f"/api/v1/auth/oauth/google/callback?code=abc&state={state}", follow_redirects=False
    )
    assert "error=email_in_use" in res.headers["location"]
    assert client.cookies.get("cc_access") is None


def test_suspended_account_cannot_sign_in_with_provider(client, session_factory, monkeypatch):
    register(client, email="person@example.com", username="suspended_one")
    db = session_factory()
    try:
        user = db.query(User).filter(User.email == "person@example.com").one()
        user.status = "suspended"
        user.external_auth_provider = "google"
        user.external_auth_id = "g-999"
        db.commit()
    finally:
        db.close()
    client.cookies.clear()

    _enable(monkeypatch, profile=_google(external_id="g-999"))
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    state = client.cookies.get("cc_oauth_state")
    res = client.get(
        f"/api/v1/auth/oauth/google/callback?code=abc&state={state}", follow_redirects=False
    )
    assert "error=account_suspended" in res.headers["location"]


def test_provider_failure_is_reported_without_details(client, monkeypatch):
    from app.core.errors import AppError

    _enable(monkeypatch, error=AppError("OAUTH_FAILED", "Sign-in didn't work.", 502))
    client.get("/api/v1/auth/oauth/google/start", follow_redirects=False)
    state = client.cookies.get("cc_oauth_state")
    res = client.get(
        f"/api/v1/auth/oauth/google/callback?code=abc&state={state}", follow_redirects=False
    )
    assert "error=oauth_failed" in res.headers["location"]
