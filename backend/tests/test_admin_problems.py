from tests.helpers import register, set_user_field

PUBLIC = {"in": "2 3\n", "out": "5", "explanation": "2 + 3 = 5."}
HIDDEN = {"in": "987654 1\n", "out": "1975308642"}


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def _payload(slug="double-it", tests=None, status="draft", **overrides):
    body = {
        "slug": slug,
        "title": "Double It",
        "description": "Read a number and print twice its value.",
        "difficulty": "Easy",
        "status": status,
        "sort_order": 1,
        "tags": ["Math"],
        "input_format": "One integer n.",
        "output_format": "Print 2 × n.",
        "constraints": "-10^6 <= n <= 10^6",
        "explanation": "Multiply by 2.",
        "time_limit_ms": 2000,
        "memory_limit_mb": 256,
        "starter_code": {"python": "# Write your solution here\n"},
        "tests": tests if tests is not None else [
            {"stdin": "4\n", "expected_output": "8", "is_hidden": False, "explanation": "4 doubled is 8."},
            {"stdin": "-7\n", "expected_output": "-14", "is_hidden": True},
        ],
    }
    body.update(overrides)
    return body


def _make_admin(client, session_factory, role="admin", email="staff@example.com", username="staff_one"):
    register(client, email=email, username=username)
    set_user_field(session_factory, email, role=role)


def test_student_cannot_view_or_change_problems(client):
    register(client)
    assert client.get("/api/v1/admin/problems").status_code == 403
    res = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    assert res.status_code == 403


def test_instructor_can_view_but_not_change(client, session_factory):
    _make_admin(client, session_factory, role="instructor")
    assert client.get("/api/v1/admin/problems").status_code == 200
    assert client.get("/api/v1/admin/overview").status_code == 200
    res = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    assert res.status_code == 403


def test_admin_creates_draft_hidden_from_students(client, session_factory, new_client):
    _make_admin(client, session_factory)
    res = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    assert res.status_code == 201
    created = res.json()["data"]
    assert created["status"] == "draft"
    assert len(created["tests"]) == 2
    slug = created["slug"]

    # The admin sees the hidden test; a student gets nothing for a draft.
    assert any(t["is_hidden"] for t in created["tests"])
    student = new_client()
    register(student, email="student@example.com", username="student_one")
    assert student.get(f"/api/v1/problems/{slug}").status_code == 404


def test_publish_requires_a_visible_example(client, session_factory):
    _make_admin(client, session_factory)
    hidden_only = _payload(
        slug="hidden-only",
        tests=[{"stdin": "1\n", "expected_output": "2", "is_hidden": True}],
    )
    created = client.post("/api/v1/admin/problems", json=hidden_only, headers=_csrf(client)).json()["data"]
    res = client.post(
        f"/api/v1/admin/problems/{created['id']}/status", json={"status": "published"}, headers=_csrf(client)
    )
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "PROBLEM_NOT_READY"


def test_publish_then_students_see_only_visible_examples(client, session_factory, new_client):
    _make_admin(client, session_factory)
    created = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client)).json()["data"]
    res = client.post(
        f"/api/v1/admin/problems/{created['id']}/status", json={"status": "published"}, headers=_csrf(client)
    )
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "published"

    student = new_client()
    register(student, email="student@example.com", username="student_one")
    detail = student.get("/api/v1/problems/double-it")
    assert detail.status_code == 200
    assert detail.json()["data"]["examples"] == [
        {"input": "4\n", "output": "8", "explanation": "4 doubled is 8."}
    ]
    assert "-7" not in detail.text and "-14" not in detail.text


def test_duplicate_slug_is_rejected(client, session_factory):
    _make_admin(client, session_factory)
    client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    res = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "SLUG_TAKEN"


def test_bad_slug_and_empty_tests_are_rejected(client, session_factory):
    _make_admin(client, session_factory)
    assert client.post(
        "/api/v1/admin/problems", json=_payload(slug="Not A Slug!"), headers=_csrf(client)
    ).status_code == 422
    assert client.post(
        "/api/v1/admin/problems", json=_payload(slug="empty-tests", tests=[]), headers=_csrf(client)
    ).status_code == 422


def test_python_only_starter_code(client, session_factory):
    _make_admin(client, session_factory)
    res = client.post(
        "/api/v1/admin/problems",
        json=_payload(slug="js-start", starter_code={"javascript": "//\n"}),
        headers=_csrf(client),
    )
    assert res.status_code == 422


def test_update_replaces_tests_and_is_logged(client, session_factory):
    _make_admin(client, session_factory)
    created = client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client)).json()["data"]
    updated = _payload(
        title="Double It Again",
        tests=[{"stdin": "5\n", "expected_output": "10", "is_hidden": False}],
    )
    res = client.put(f"/api/v1/admin/problems/{created['id']}", json=updated, headers=_csrf(client))
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["title"] == "Double It Again"
    assert len(data["tests"]) == 1

    log = client.get("/api/v1/admin/audit").json()["data"]
    actions = [row["action"] for row in log]
    assert "problem.create" in actions and "problem.update" in actions


def test_overview_reports_real_counts(client, session_factory):
    _make_admin(client, session_factory)
    client.post("/api/v1/admin/problems", json=_payload(), headers=_csrf(client))
    data = client.get("/api/v1/admin/overview").json()["data"]
    assert data["problems_draft"] == 1
    assert data["problems_published"] == 0
    assert data["students"] == 0  # the only account is staff, not a student
