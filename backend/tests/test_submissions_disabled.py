from app.core.config import Settings, get_settings
from app.services.judge0_client import SUPPORTED_LANGUAGES


def test_submissions_are_off_by_default():
    assert Settings.model_fields["submissions_enabled"].default is False


def test_only_python_is_supported_by_the_runner():
    assert SUPPORTED_LANGUAGES == frozenset({"python"})


def test_submission_endpoints_return_clear_404_when_disabled(client, monkeypatch):
    monkeypatch.setenv("SUBMISSIONS_ENABLED", "false")
    get_settings.cache_clear()
    try:
        create = client.post(
            "/api/v1/submissions",
            json={"problem_slug": "sum", "language": "python", "source_code": "print(5)"},
        )
        assert create.status_code == 404
        assert create.json()["error"]["code"] == "SUBMISSIONS_DISABLED"

        read = client.get("/api/v1/submissions/00000000-0000-0000-0000-000000000000")
        assert read.status_code == 404
        assert read.json()["error"]["code"] == "SUBMISSIONS_DISABLED"
    finally:
        monkeypatch.undo()
        get_settings.cache_clear()


def test_problem_detail_still_works_with_submissions_off(client, session_factory, monkeypatch):
    from tests.helpers import register
    from tests.problem_helpers import make_problem

    make_problem(session_factory, slug="sum", tests=[{"in": "1\n", "out": "2", "hidden": False}])
    register(client)
    monkeypatch.setenv("SUBMISSIONS_ENABLED", "false")
    get_settings.cache_clear()
    try:
        res = client.get("/api/v1/problems/sum")
        assert res.status_code == 200
    finally:
        monkeypatch.undo()
        get_settings.cache_clear()
