from datetime import datetime, timedelta, timezone

ONLINE_WINDOW = timedelta(minutes=2)
OFFLINE_AFTER = timedelta(hours=48)


def presence(last_seen: datetime | None, now: datetime | None = None) -> dict:
    """Online / last-seen wording, worked out on the server so every browser shows the same thing.

    - within 2 minutes: Online
    - within an hour: a few minutes ago
    - within a day: a few hours ago
    - within two days: yesterday
    - older, or never: Offline
    """
    now = now or datetime.now(timezone.utc)
    if last_seen is None or now - last_seen >= OFFLINE_AFTER:
        return {"online": False, "label": "Offline", "last_seen_at": last_seen.isoformat() if last_seen else None}

    age = now - last_seen
    if age <= ONLINE_WINDOW:
        label, online = "Online", True
    elif age < timedelta(hours=1):
        label, online = "Last seen a few minutes ago", False
    elif age < timedelta(hours=24):
        label, online = "Last seen a few hours ago", False
    else:
        label, online = "Last seen yesterday", False
    return {"online": online, "label": label, "last_seen_at": last_seen.isoformat()}
