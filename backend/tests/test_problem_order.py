from app.models import Problem, ProblemTestCase
from tests.helpers import register

PUBLIC = {"in": "1\n", "out": "2", "hidden": False}


def _add(session_factory, slug, order):
    db = session_factory()
    try:
        problem = Problem(
            slug=slug,
            title=slug.title(),
            description="x",
            difficulty="Easy",
            status="published",
            sort_order=order,
            tags=[],
            time_limit_ms=2000,
            memory_limit_mb=256,
            starter_code={"python": "#\n"},
        )
        problem.test_cases = [ProblemTestCase(position=1, stdin="1\n", expected_output="2", is_hidden=False)]
        db.add(problem)
        db.commit()
    finally:
        db.close()


def test_list_follows_learning_path_order_and_reports_number(client, session_factory):
    # Inserted out of order on purpose.
    _add(session_factory, "third-step", 3)
    _add(session_factory, "first-step", 1)
    _add(session_factory, "second-step", 2)
    register(client)

    items = client.get("/api/v1/problems").json()["data"]
    assert [p["slug"] for p in items] == ["first-step", "second-step", "third-step"]
    assert [p["number"] for p in items] == [1, 2, 3]
