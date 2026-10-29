from tests.helpers import register


def _patch(client, body):
    return client.patch(
        "/api/v1/users/me", json=body, headers={"X-CSRF-Token": client.cookies.get("cc_csrf")}
    )


def test_display_name_cannot_be_nulled_or_blanked(client):
    register(client)
    assert _patch(client, {"display_name": None}).status_code == 422
    assert _patch(client, {"display_name": "   "}).status_code == 422
    assert client.get("/api/v1/auth/me").json()["data"]["profile"]["display_name"] == "Student One"


def test_omitted_display_name_is_left_unchanged(client):
    register(client)
    res = _patch(client, {"bio": "Hello"})
    assert res.status_code == 200
    profile = res.json()["data"]["profile"]
    assert profile["display_name"] == "Student One"
    assert profile["bio"] == "Hello"


def test_optional_fields_can_be_cleared_with_null(client):
    register(client)
    _patch(client, {"bio": "Hello", "website_url": "https://example.com"})
    res = _patch(client, {"bio": None, "website_url": None})
    assert res.status_code == 200
    profile = res.json()["data"]["profile"]
    assert profile["bio"] is None and profile["website_url"] is None
