from tests.helpers import register

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 200
JPEG = b"\xff\xd8\xff" + b"0" * 200


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def test_upload_png_sets_photo_and_serves_it_publicly(client, new_client):
    register(client)
    res = client.post(
        "/api/v1/users/me/avatar",
        files={"file": ("me.png", PNG, "image/png")},
        headers=_csrf(client),
    )
    assert res.status_code == 200
    avatar_url = res.json()["data"]["profile"]["avatar_url"]
    assert avatar_url.startswith("/api/v1/users/student_one/avatar?v=")

    # Anyone can view a profile photo, without logging in.
    public = new_client().get("/api/v1/users/student_one/avatar")
    assert public.status_code == 200
    assert public.headers["content-type"] == "image/png"
    assert public.content == PNG


def test_jpeg_accepted(client):
    register(client)
    res = client.post(
        "/api/v1/users/me/avatar", files={"file": ("me.jpg", JPEG, "image/jpeg")}, headers=_csrf(client)
    )
    assert res.status_code == 200


def test_text_file_renamed_as_png_is_refused(client):
    register(client)
    res = client.post(
        "/api/v1/users/me/avatar",
        files={"file": ("evil.png", b"<script>alert(1)</script>", "image/png")},
        headers=_csrf(client),
    )
    assert res.status_code == 415
    assert res.json()["error"]["code"] == "AVATAR_INVALID_TYPE"


def test_oversized_photo_is_refused(client):
    register(client)
    big = b"\x89PNG\r\n\x1a\n" + b"0" * (600 * 1024)
    res = client.post(
        "/api/v1/users/me/avatar", files={"file": ("big.png", big, "image/png")}, headers=_csrf(client)
    )
    assert res.status_code == 413
    assert res.json()["error"]["code"] == "AVATAR_TOO_LARGE"


def test_upload_requires_csrf(client):
    register(client)
    res = client.post("/api/v1/users/me/avatar", files={"file": ("me.png", PNG, "image/png")})
    assert res.status_code == 403


def test_remove_photo(client, new_client):
    register(client)
    client.post("/api/v1/users/me/avatar", files={"file": ("me.png", PNG, "image/png")}, headers=_csrf(client))
    res = client.delete("/api/v1/users/me/avatar", headers=_csrf(client))
    assert res.status_code == 200
    assert res.json()["data"]["profile"]["avatar_url"] is None
    assert new_client().get("/api/v1/users/student_one/avatar").status_code == 404
