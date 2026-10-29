from tests.helpers import register, set_user_field
from tests.problem_helpers import make_problem

PUBLIC = {"in": "2 3\n", "out": "5", "hidden": False}


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def _student(client, session_factory, email="ann@example.com", username="ann_one"):
    register(client, email=email, username=username)
    return client


def test_discussion_requires_login(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    assert client.get("/api/v1/problems/sum/discussion").status_code == 401


def test_draft_problem_has_no_discussion(client, session_factory):
    make_problem(session_factory, slug="draft-one", status="draft", tests=[PUBLIC])
    register(client)
    assert client.get("/api/v1/problems/draft-one/discussion").status_code == 404


def test_post_and_reply_appear_for_everyone(client, new_client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client, email="ann@example.com", username="ann_one")
    post = client.post(
        "/api/v1/problems/sum/discussion", json={"body": "How do I split the line?"}, headers=_csrf(client)
    )
    assert post.status_code == 201
    post_id = post.json()["data"]["id"]

    other = new_client()
    register(other, email="bob@example.com", username="bob_two")
    reply = other.post(
        "/api/v1/problems/sum/discussion",
        json={"body": "Try split() with no arguments.", "parent_id": post_id},
        headers=_csrf(other),
    )
    assert reply.status_code == 201

    threads = other.get("/api/v1/problems/sum/discussion").json()["data"]
    assert len(threads) == 1
    assert threads[0]["post"]["body"] == "How do I split the line?"
    assert threads[0]["post"]["author_username"] == "ann_one"
    assert threads[0]["replies"][0]["body"] == "Try split() with no arguments."


def test_replies_to_replies_are_refused(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    top = client.post("/api/v1/problems/sum/discussion", json={"body": "Question"}, headers=_csrf(client)).json()["data"]
    reply = client.post(
        "/api/v1/problems/sum/discussion",
        json={"body": "Answer", "parent_id": top["id"]},
        headers=_csrf(client),
    ).json()["data"]
    res = client.post(
        "/api/v1/problems/sum/discussion",
        json={"body": "Reply to reply", "parent_id": reply["id"]},
        headers=_csrf(client),
    )
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "REPLY_TO_REPLY"


def test_empty_post_is_refused(client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client)
    res = client.post("/api/v1/problems/sum/discussion", json={"body": "   "}, headers=_csrf(client))
    assert res.status_code == 422


def test_only_author_or_staff_can_delete_and_text_is_removed(client, new_client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client, email="ann@example.com", username="ann_one")
    post = client.post("/api/v1/problems/sum/discussion", json={"body": "Secret text"}, headers=_csrf(client)).json()["data"]

    other = new_client()
    register(other, email="bob@example.com", username="bob_two")
    assert other.delete(f"/api/v1/discussion/{post['id']}", headers=_csrf(other)).status_code == 403

    deleted = client.delete(f"/api/v1/discussion/{post['id']}", headers=_csrf(client))
    assert deleted.status_code == 200
    threads = other.get("/api/v1/problems/sum/discussion").json()["data"]
    assert threads[0]["post"]["is_removed"] is True
    assert threads[0]["post"]["body"] is None
    assert "Secret text" not in other.get("/api/v1/problems/sum/discussion").text


def test_report_rules(client, new_client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client, email="ann@example.com", username="ann_one")
    post = client.post("/api/v1/problems/sum/discussion", json={"body": "Hello"}, headers=_csrf(client)).json()["data"]

    own = client.post(f"/api/v1/discussion/{post['id']}/report", json={"reason": "spam"}, headers=_csrf(client))
    assert own.status_code == 400

    other = new_client()
    register(other, email="bob@example.com", username="bob_two")
    first = other.post(f"/api/v1/discussion/{post['id']}/report", json={"reason": "spam"}, headers=_csrf(other))
    assert first.status_code == 201
    again = other.post(f"/api/v1/discussion/{post['id']}/report", json={"reason": "spam"}, headers=_csrf(other))
    assert again.status_code == 409


def test_student_cannot_see_reports_moderator_can_remove(client, new_client, session_factory):
    make_problem(session_factory, slug="sum", tests=[PUBLIC])
    register(client, email="ann@example.com", username="ann_one")
    post = client.post("/api/v1/problems/sum/discussion", json={"body": "Rude text"}, headers=_csrf(client)).json()["data"]

    reporter = new_client()
    register(reporter, email="bob@example.com", username="bob_two")
    reporter.post(f"/api/v1/discussion/{post['id']}/report", json={"reason": "abusive"}, headers=_csrf(reporter))

    assert reporter.get("/api/v1/community/reports").status_code == 403

    mod = new_client()
    register(mod, email="mod@example.com", username="mod_one")
    set_user_field(session_factory, "mod@example.com", role="moderator")
    reports = mod.get("/api/v1/community/reports").json()["data"]
    assert len(reports) == 1
    assert reports[0]["reason"] == "abusive"

    res = mod.post(
        f"/api/v1/community/reports/{reports[0]['id']}/resolve",
        json={"action": "remove"},
        headers=_csrf(mod),
    )
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "actioned"

    threads = reporter.get("/api/v1/problems/sum/discussion").json()["data"]
    assert threads[0]["post"]["is_removed"] is True
    assert mod.get("/api/v1/community/reports?status=open").json()["data"] == []
