from app.models import Submission
from tests.helpers import register
from tests.problem_helpers import FakeRunner, make_problem, make_user

PUBLIC = {"in": "2 3\n", "out": "5", "hidden": False}
HIDDEN = {"in": "987654 1\n", "out": "1975308642", "hidden": True}


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def _configure_runner(monkeypatch, *, configured=True):
    """Make the service believe a runner exists, and stop real background threads."""
    runner = FakeRunner([], configured=configured)
    monkeypatch.setattr("app.services.submission_service.get_judge_client", lambda: runner)
    monkeypatch.setattr("app.services.submission_service.enqueue_judging", lambda _id: None)
    return runner


def test_problem_list_requires_login(client):
    assert client.get("/api/v1/problems").status_code == 401


def test_problem_list_shows_only_published(client, session_factory):
    make_problem(session_factory, slug="visible-one", tests=[PUBLIC])
    make_problem(session_factory, slug="hidden-draft", status="draft", tests=[PUBLIC])
    register(client)
    res = client.get("/api/v1/problems")
    assert res.status_code == 200
    slugs = [p["slug"] for p in res.json()["data"]]
    assert slugs == ["visible-one"]
    assert res.json()["meta"]["total"] == 1


def test_problem_list_search_and_difficulty_filter(client, session_factory):
    make_problem(session_factory, slug="alpha-sum", tests=[PUBLIC])
    make_problem(session_factory, slug="beta-count", tests=[PUBLIC])
    register(client)
    assert [p["slug"] for p in client.get("/api/v1/problems?q=alpha").json()["data"]] == ["alpha-sum"]
    assert client.get("/api/v1/problems?difficulty=Hard").json()["data"] == []
    assert client.get("/api/v1/problems?difficulty=bogus").status_code == 422


def test_detail_exposes_only_public_examples_never_hidden_tests(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC, HIDDEN])
    register(client)
    res = client.get("/api/v1/problems/sum")
    assert res.status_code == 200
    data = res.json()["data"]
    # Visible examples carry input, output and an optional explanation. Nothing else.
    assert len(data["examples"]) == 1
    example = data["examples"][0]
    assert example["input"] == "2 3\n"
    assert example["output"] == "5"
    assert set(example) == {"input", "output", "explanation"}
    assert "987654" not in res.text and "1975308642" not in res.text


def test_detail_reports_execution_unavailable_when_runner_not_configured(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    assert client.get("/api/v1/problems/sum").json()["data"]["execution_available"] is False


def test_draft_problem_is_not_found(client, session_factory):
    make_problem(session_factory, slug="draft-one", status="draft", tests=[PUBLIC])
    register(client)
    res = client.get("/api/v1/problems/draft-one")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "PROBLEM_NOT_FOUND"


def test_submit_refused_with_clear_error_when_runner_not_configured(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
        headers=_csrf(client),
    )
    assert res.status_code == 503
    assert res.json()["error"]["code"] == "EXECUTION_NOT_CONFIGURED"
    # Nothing was stored, so the student can't be left with a stuck "queued" record.
    db = session_factory()
    try:
        assert db.query(Submission).count() == 0
    finally:
        db.close()


def test_submit_creates_queued_submission_when_runner_configured(client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
        headers=_csrf(client),
    )
    assert res.status_code == 202
    body = res.json()["data"]
    assert body["status"] == "QUEUED"
    assert body["problem_slug"] == "sum"
    assert body["source_code"] == "print(5)"


def test_submit_requires_csrf_header(client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "CSRF_FAILED"


def test_unsupported_language_rejected(client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)
    make_problem(session_factory, slug="sum", tests=[PUBLIC], starter={"python": "#\n"})
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "cpp", "source_code": "int main(){}"},
        headers=_csrf(client),
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "LANGUAGE_NOT_SUPPORTED"


def test_problem_with_no_tests_cannot_be_submitted(client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)
    make_problem(session_factory, slug="empty", tests=[])
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "empty", "language": "python", "source_code": "print(1)"},
        headers=_csrf(client),
    )
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "PROBLEM_NOT_READY"


def test_students_cannot_read_each_others_submissions(client, new_client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    created = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
        headers=_csrf(client),
    ).json()["data"]

    other = new_client()
    register(other, email="other@example.com", username="other_user")
    res = other.get(f"/api/v1/submissions/{created['id']}")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "SUBMISSION_NOT_FOUND"

    owner = client.get(f"/api/v1/submissions/{created['id']}")
    assert owner.status_code == 200


def test_queue_failure_is_reported_honestly(client, session_factory, monkeypatch):
    _configure_runner(monkeypatch)

    def broken_queue(_id):
        raise RuntimeError("redis down")

    monkeypatch.setattr("app.services.submission_service.enqueue_judging", broken_queue)
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    res = client.post(
        "/api/v1/submissions",
        json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
        headers=_csrf(client),
    )
    assert res.status_code == 503
    assert res.json()["error"]["code"] == "QUEUE_UNAVAILABLE"
