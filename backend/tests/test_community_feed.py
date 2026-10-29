from tests.helpers import register
from tests.problem_helpers import make_problem

PUBLIC = {"in": "1\n", "out": "2", "hidden": False}


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def test_community_feed_requires_login(client):
    assert client.get("/api/v1/community/latest").status_code == 401


def test_feed_shows_published_questions_with_reply_counts_and_no_drafts(client, new_client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    make_problem(session_factory, slug="hidden-draft", status="draft", tests=[PUBLIC])
    register(client, email="ann@example.com", username="ann_one")

    question = client.post(
        "/api/v1/problems/sum/discussion", json={"body": "How do I read two numbers?"}, headers=_csrf(client)
    ).json()["data"]
    client.post(
        "/api/v1/problems/hidden-draft/discussion" , json={"body": "Should not appear"}, headers=_csrf(client)
    )

    other = new_client()
    register(other, email="bob@example.com", username="bob_two")
    other.post(
        "/api/v1/problems/sum/discussion",
        json={"body": "Use split().", "parent_id": question["id"]},
        headers=_csrf(other),
    )

    feed = other.get("/api/v1/community/latest").json()["data"]
    bodies = [row["post"]["body"] for row in feed]
    assert "How do I read two numbers?" in bodies
    assert "Should not appear" not in bodies
    row = next(r for r in feed if r["post"]["body"] == "How do I read two numbers?")
    assert row["problem_slug"] == "sum"
    assert row["reply_count"] == 1
    assert row["post"]["author_username"] == "ann_one"
