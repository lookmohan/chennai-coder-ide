from datetime import datetime, timezone

import pytest

from app.models.base import UTCDateTime
from tests.helpers import login, register


def test_api_datetimes_are_utc_with_z_suffix(client):
    res = register(client)
    created = res.json()["data"]["created_at"]
    assert created.endswith("Z") or created.endswith("+00:00")

    client.cookies.clear()
    last_login = login(client).json()["data"]["last_login_at"]
    assert last_login.endswith("Z") or last_login.endswith("+00:00")


def test_utc_type_round_trip_and_rejects_naive():
    t = UTCDateTime()
    aware = datetime(2026, 10, 7, 12, 0, tzinfo=timezone.utc)
    stored = t.process_bind_param(aware, None)
    assert stored.tzinfo is None and stored.hour == 12
    assert t.process_result_value(stored, None) == aware
    assert t.process_bind_param(None, None) is None
    with pytest.raises(ValueError):
        t.process_bind_param(datetime(2026, 10, 7, 12, 0), None)
