from app.content.topics import TOPICS
from app.models import Problem, ProblemTestCase
from tests.helpers import register


def _add_problem(session_factory, slug, topic, difficulty, status="published"):
    db = session_factory()
    try:
        problem = Problem(
            slug=slug,
            title=slug.replace("-", " ").title(),
            description="A question.",
            difficulty=difficulty,
            status=status,
            topic_slug=topic,
            tags=[],
            time_limit_ms=2000,
            memory_limit_mb=256,
            starter_code={"python": "# Write your solution here\n"},
        )
        problem.test_cases = [
            ProblemTestCase(position=1, stdin="1\n", expected_output="2", is_hidden=False, explanation="1 + 1 = 2.")
        ]
        db.add(problem)
        db.commit()
    finally:
        db.close()


def test_topics_require_login(client):
    assert client.get("/api/v1/topics").status_code == 401


def test_all_concepts_are_listed_in_learning_order_with_targets(client, session_factory):
    register(client)
    data = client.get("/api/v1/topics").json()["data"]
    assert [t["slug"] for t in data] == [t["slug"] for t in TOPICS]
    assert data[0]["targets"] == {"Easy": 20, "Medium": 15, "Hard": 10}
    assert data[0]["number"] == 1


def test_counts_include_only_published_questions(client, session_factory):
    register(client)
    _add_problem(session_factory, "list-easy-one", "lists", "Easy")
    _add_problem(session_factory, "list-easy-two", "lists", "Easy")
    _add_problem(session_factory, "list-hard-draft", "lists", "Hard", status="draft")

    lists = next(t for t in client.get("/api/v1/topics").json()["data"] if t["slug"] == "lists")
    assert lists["counts"] == {"Easy": 2, "Medium": 0, "Hard": 0}


def test_topic_detail_groups_published_questions_by_level(client, session_factory):
    register(client)
    _add_problem(session_factory, "loop-easy", "loops", "Easy")
    _add_problem(session_factory, "loop-medium", "loops", "Medium")
    _add_problem(session_factory, "loop-draft", "loops", "Hard", status="draft")

    detail = client.get("/api/v1/topics/loops").json()["data"]
    assert detail["name"] == "Loops"
    assert [p["slug"] for p in detail["problems"]["Easy"]] == ["loop-easy"]
    assert [p["slug"] for p in detail["problems"]["Medium"]] == ["loop-medium"]
    assert detail["problems"]["Hard"] == []


def test_unknown_topic_is_not_found(client, session_factory):
    register(client)
    res = client.get("/api/v1/topics/not-a-topic")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "TOPIC_NOT_FOUND"
