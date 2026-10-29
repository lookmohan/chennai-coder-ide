import httpx
import pytest

from app.services import piston_client
from app.services.judge0_client import ExecutionUnavailable
from app.services.piston_client import PistonClient


class FakeResponse:
    def __init__(self, status_code=200, body=None):
        self.status_code = status_code
        self._body = body or {}

    def json(self):
        return self._body


def _client():
    return PistonClient("https://piston.example/api/v2", timeout_seconds=5)


def _run(monkeypatch, response=None, error=None):
    captured = {}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        if error is not None:
            raise error
        return response

    monkeypatch.setattr(piston_client.httpx, "post", fake_post)
    result = _client().run(
        source_code="print(1)", language="python", stdin="", time_limit_s=2.0, memory_limit_kb=256 * 1024
    )
    return result, captured


def test_success_maps_to_accepted_run_with_stdout(monkeypatch):
    body = {"run": {"stdout": "5\n", "stderr": "", "code": 0, "signal": None}}
    result, _ = _run(monkeypatch, FakeResponse(200, body))
    assert result.status_id == 3
    assert result.stdout == "5\n"


def test_request_uses_correct_language_file_name_and_limits(monkeypatch):
    _, captured = _run(monkeypatch, FakeResponse(200, {"run": {"code": 0}}))
    assert captured["url"] == "https://piston.example/api/v2/execute"
    assert captured["json"]["language"] == "python"
    assert captured["json"]["version"] == "*"
    assert captured["json"]["files"] == [{"name": "main.py", "content": "print(1)"}]
    assert captured["json"]["run_timeout"] == 2000
    assert captured["json"]["run_memory_limit"] == 256 * 1024 * 1024


def test_nonzero_exit_is_runtime_error(monkeypatch):
    body = {"run": {"stdout": "", "stderr": "Traceback", "code": 1, "signal": None}}
    result, _ = _run(monkeypatch, FakeResponse(200, body))
    assert result.status_id == 11
    assert result.stderr == "Traceback"


def test_compile_failure_is_compilation_error(monkeypatch):
    body = {"compile": {"code": 1, "stderr": "main.cpp: error", "output": "main.cpp: error"}, "run": {}}
    result, _ = _run(monkeypatch, FakeResponse(200, body))
    assert result.status_id == 6
    assert "error" in result.compile_output


def test_sigkill_is_treated_as_time_limit(monkeypatch):
    body = {"run": {"stdout": "", "stderr": "", "code": None, "signal": "SIGKILL"}}
    result, _ = _run(monkeypatch, FakeResponse(200, body))
    assert result.status_id == 5


def test_rate_limit_becomes_unavailable_not_a_wrong_answer(monkeypatch):
    with pytest.raises(ExecutionUnavailable):
        _run(monkeypatch, FakeResponse(429, {}))


def test_network_failure_becomes_unavailable(monkeypatch):
    with pytest.raises(ExecutionUnavailable):
        _run(monkeypatch, error=httpx.ConnectError("boom"))


def test_unconfigured_when_url_empty():
    assert PistonClient("", 5).configured is False
