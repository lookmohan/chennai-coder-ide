from tests.helpers import register, set_user_field


def test_unauthenticated_cannot_list_students(client):
    res = client.get("/api/v1/admin/students")
    assert res.status_code == 401


def test_student_gets_403_on_admin_students(client):
    register(client)
    res = client.get("/api/v1/admin/students")
    assert res.status_code == 403
    assert res.json() == {
        "success": False,
        "error": {
            "code": "FORBIDDEN",
            "message": "You do not have permission to perform this action.",
        },
    }


def test_moderator_gets_403_on_admin_students(client, session_factory):
    register(client)
    set_user_field(session_factory, "student@example.com", role="moderator")
    assert client.get("/api/v1/admin/students").status_code == 403


def test_instructor_can_list_students_only(new_client, session_factory):
    student = new_client()
    register(student)

    instructor = new_client()
    register(instructor, email="teach@example.com", username="teacher_one")
    set_user_field(session_factory, "teach@example.com", role="instructor")

    res = instructor.get("/api/v1/admin/students")
    assert res.status_code == 200
    body = res.json()
    assert body["meta"]["total"] == 1  # the instructor is not listed as a student
    assert body["data"][0]["username"] == "student_one"
    assert "password_hash" not in res.text


def test_role_change_applies_immediately_not_from_token(client, session_factory):
    register(client)
    assert client.get("/api/v1/admin/students").status_code == 403
    set_user_field(session_factory, "student@example.com", role="admin")
    # Same token, but role is read from the DB on each request.
    assert client.get("/api/v1/admin/students").status_code == 200


def test_pagination_bounds_validated(new_client, session_factory):
    admin = new_client()
    register(admin, email="a@example.com", username="admin_one")
    set_user_field(session_factory, "a@example.com", role="admin")
    assert admin.get("/api/v1/admin/students?page_size=1000").status_code == 422
    assert admin.get("/api/v1/admin/students?page=0").status_code == 422


def test_cookie_auth_requires_csrf_for_mutations(client):
    register(client)
    res = client.patch("/api/v1/users/me", json={"bio": "hello"})
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "CSRF_FAILED"


def test_cookie_auth_with_csrf_can_update_profile(client):
    register(client)
    res = client.patch(
        "/api/v1/users/me",
        json={"bio": "I love Python", "github_url": "https://github.com/example"},
        headers={"X-CSRF-Token": client.cookies.get("cc_csrf")},
    )
    assert res.status_code == 200
    assert res.json()["data"]["profile"]["bio"] == "I love Python"


def test_bearer_auth_does_not_need_csrf(client, new_client):
    register(client)
    token = client.cookies.get("cc_access")
    api = new_client()
    res = api.patch(
        "/api/v1/users/me",
        json={"location": "Chennai"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["data"]["profile"]["location"] == "Chennai"


def test_profile_rejects_javascript_urls(client):
    register(client)
    res = client.patch(
        "/api/v1/users/me",
        json={"website_url": "javascript:alert(1)"},
        headers={"X-CSRF-Token": client.cookies.get("cc_csrf")},
    )
    assert res.status_code == 422


def test_public_profile_hides_private_fields(client):
    register(client)
    res = client.get("/api/v1/users/student_one")
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["username"] == "student_one"
    for private in ("email", "role", "status", "password_hash", "id"):
        assert private not in data


def test_public_profile_404(client):
    res = client.get("/api/v1/users/does_not_exist")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "USER_NOT_FOUND"


def test_health_endpoints(client):
    assert client.get("/api/v1/health").status_code == 200
    assert client.get("/api/v1/health/ready").status_code == 200
