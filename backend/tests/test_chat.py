from datetime import datetime, timedelta, timezone

from app.services.presence import presence
from tests.helpers import register, set_user_field


def _csrf(client):
    return {"X-CSRF-Token": client.cookies.get("cc_csrf")}


def test_chat_requires_login(client):
    assert client.get("/api/v1/chat/room").status_code == 401


def test_direct_messages_are_not_available(client):
    register(client, email="ann@example.com", username="ann_one")
    assert client.get("/api/v1/chat/conversations").status_code == 404
    assert client.get("/api/v1/chat/with/ann_one").status_code == 404
    assert client.post("/api/v1/chat/with/ann_one", json={"body": "hi"}, headers=_csrf(client)).status_code == 404


def test_room_post_is_visible_to_everyone_and_marked_mine_only_for_author(client, new_client):
    register(client, email="ann@example.com", username="ann_one")
    sent = client.post("/api/v1/chat/room", json={"body": "Hello everyone"}, headers=_csrf(client))
    assert sent.status_code == 201
    assert sent.json()["data"]["mine"] is True

    bob = new_client()
    register(bob, email="bob@example.com", username="bob_two")
    messages = bob.get("/api/v1/chat/room").json()["data"]
    assert len(messages) == 1
    assert messages[0]["body"] == "Hello everyone"
    assert messages[0]["author_username"] == "ann_one"
    assert messages[0]["mine"] is False
    assert messages[0]["can_delete"] is False


def test_empty_and_long_messages_are_refused(client):
    register(client, email="ann@example.com", username="ann_one")
    assert client.post("/api/v1/chat/room", json={"body": "   "}, headers=_csrf(client)).status_code == 422
    assert client.post("/api/v1/chat/room", json={"body": "x" * 501}, headers=_csrf(client)).status_code == 422


def test_authors_can_delete_their_message_others_cannot(client, new_client):
    register(client, email="ann@example.com", username="ann_one")
    message = client.post("/api/v1/chat/room", json={"body": "oops"}, headers=_csrf(client)).json()["data"]

    bob = new_client()
    register(bob, email="bob@example.com", username="bob_two")
    assert bob.delete(f"/api/v1/chat/room/{message['id']}", headers=_csrf(bob)).status_code == 403

    assert client.delete(f"/api/v1/chat/room/{message['id']}", headers=_csrf(client)).status_code == 200
    assert client.get("/api/v1/chat/room").json()["data"] == []


def test_moderator_can_remove_any_message(client, new_client, session_factory):
    register(client, email="ann@example.com", username="ann_one")
    message = client.post("/api/v1/chat/room", json={"body": "rude"}, headers=_csrf(client)).json()["data"]

    mod = new_client()
    register(mod, email="mod@example.com", username="mod_one")
    set_user_field(session_factory, "mod@example.com", role="moderator")
    assert mod.delete(f"/api/v1/chat/room/{message['id']}", headers=_csrf(mod)).status_code == 200


def test_people_list_hides_yourself_and_shows_presence(client, new_client):
    register(client, email="ann@example.com", username="ann_one")
    bob = new_client()
    register(bob, email="bob@example.com", username="bob_two")
    assert bob.get("/api/v1/auth/me").status_code == 200

    people = client.get("/api/v1/chat/people").json()["data"]
    usernames = [p["username"] for p in people]
    assert "bob_two" in usernames
    assert "ann_one" not in usernames
    bob_row = next(p for p in people if p["username"] == "bob_two")
    assert bob_row["presence"]["label"] == "Online"


def test_presence_wording_follows_the_time_passed():
    now = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)
    assert presence(now - timedelta(seconds=30), now)["label"] == "Online"
    assert presence(now - timedelta(minutes=10), now)["label"] == "Last seen a few minutes ago"
    assert presence(now - timedelta(hours=5), now)["label"] == "Last seen a few hours ago"
    assert presence(now - timedelta(hours=30), now)["label"] == "Last seen yesterday"
    assert presence(now - timedelta(days=3), now)["label"] == "Offline"
    assert presence(None, now)["label"] == "Offline"
