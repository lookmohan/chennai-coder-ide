from tests.helpers import PASSWORD, login, register, set_user_field


def test_register_creates_student_and_sets_cookies(client):
    res = register(client)
    assert res.status_code == 201
    body = res.json()
    assert body["success"] is True
    assert body["data"]["role"] == "student"
    assert body["data"]["profile"]["username"] == "student_one"
    assert "password" not in res.text and "password_hash" not in res.text
    assert client.cookies.get("cc_access") and client.cookies.get("cc_csrf")


def test_register_cannot_choose_role(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "sneaky@example.com",
            "password": PASSWORD,
            "username": "sneaky",
            "display_name": "Sneaky",
            "role": "admin",
        },
    )
    assert res.status_code == 201
    assert res.json()["data"]["role"] == "student"


def test_duplicate_email_conflicts(client):
    register(client)
    res = register(client, username="other_name")
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "EMAIL_TAKEN"


def test_duplicate_username_conflicts(client):
    register(client)
    res = register(client, email="two@example.com")
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "USERNAME_TAKEN"


def test_weak_password_rejected_without_echoing_it(client):
    res = register(client, password="short1")
    assert res.status_code == 422
    body = res.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "short1" not in res.text


def test_bad_username_rejected(client):
    res = register(client, username="Bad Name!")
    assert res.status_code == 422


def test_login_success_updates_last_login(client):
    register(client)
    client.cookies.clear()
    res = login(client)
    assert res.status_code == 200
    assert res.json()["data"]["last_login_at"] is not None


def test_login_wrong_password_and_unknown_email_look_identical(client):
    register(client)
    wrong = login(client, password="wrong-password-1")
    unknown = login(client, email="nobody@example.com")
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_me_requires_authentication(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_me_with_cookie(client):
    register(client)
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 200
    assert res.json()["data"]["email"] == "student@example.com"


def test_logout_clears_session(client):
    register(client)
    client.post("/api/v1/auth/logout")
    assert client.get("/api/v1/auth/me").status_code == 401


def test_tampered_token_rejected(client):
    register(client)
    client.cookies.set("cc_access", client.cookies.get("cc_access") + "x")
    assert client.get("/api/v1/auth/me").status_code == 401


def test_suspended_user_cannot_login(client, session_factory):
    register(client)
    set_user_field(session_factory, "student@example.com", status="suspended")
    client.cookies.clear()
    res = login(client)
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "ACCOUNT_SUSPENDED"


def test_suspension_blocks_existing_session(client, session_factory):
    register(client)
    set_user_field(session_factory, "student@example.com", status="suspended")
    assert client.get("/api/v1/auth/me").status_code == 403


def test_login_rate_limited_per_email(client, monkeypatch):
    from app.core import config

    monkeypatch.setenv("RATE_LOGIN_PER_EMAIL_PER_15MIN", "3")
    config.get_settings.cache_clear()
    try:
        register(client)
        statuses = [login(client, password="wrong-password-1").status_code for _ in range(5)]
        assert statuses[:3] == [401, 401, 401]
        assert statuses[3] == 429
    finally:
        monkeypatch.delenv("RATE_LOGIN_PER_EMAIL_PER_15MIN", raising=False)
        config.get_settings.cache_clear()
