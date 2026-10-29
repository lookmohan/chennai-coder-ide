"""Clients for external code runners.

Chennai Coder practice is Python-only. Practice runs in the browser (Pyodide), so these clients
are only used when server-side submissions are switched on, and only for Python.
"""
from dataclasses import dataclass
from typing import Protocol

import httpx

from app.core.config import get_settings

# Judge0 language ids (Judge0 CE). Python is the only supported language.
LANGUAGE_IDS: dict[str, int] = {
    "python": 71,
}
SUPPORTED_LANGUAGES = frozenset(LANGUAGE_IDS)


class ExecutionUnavailable(Exception):
    """The runner could not be reached or returned an unusable response."""


@dataclass(frozen=True)
class RunResult:
    """Runner-independent result. Status ids follow Judge0's numbering."""

    status_id: int
    status_description: str
    stdout: str
    stderr: str
    compile_output: str
    time_ms: int | None
    memory_kb: int | None


class CodeRunner(Protocol):
    configured: bool

    def run(
        self,
        *,
        source_code: str,
        language: str,
        stdin: str,
        time_limit_s: float,
        memory_limit_kb: int,
    ) -> RunResult: ...


def _to_ms(value) -> int | None:
    try:
        return round(float(value) * 1000)
    except (TypeError, ValueError):
        return None


def _to_int(value) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class Judge0Client:
    def __init__(self, base_url: str, api_key: str, timeout_seconds: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    @property
    def configured(self) -> bool:
        return bool(self.base_url)

    def run(
        self,
        *,
        source_code: str,
        language: str,
        stdin: str,
        time_limit_s: float,
        memory_limit_kb: int,
    ) -> RunResult:
        if language not in LANGUAGE_IDS:
            raise ValueError(f"Unsupported language: {language}")

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Auth-Token"] = self.api_key

        payload = {
            "source_code": source_code,
            "language_id": LANGUAGE_IDS[language],
            "stdin": stdin,
            "cpu_time_limit": time_limit_s,
            "memory_limit": memory_limit_kb,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/submissions",
                params={"base64_encoded": "false", "wait": "true"},
                json=payload,
                headers=headers,
                timeout=self.timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ExecutionUnavailable("Could not reach the code runner.") from exc

        if response.status_code >= 400:
            raise ExecutionUnavailable(f"Code runner responded with HTTP {response.status_code}.")

        data = response.json()
        status = data.get("status") or {}
        return RunResult(
            status_id=_to_int(status.get("id")) or 13,
            status_description=str(status.get("description") or ""),
            stdout=data.get("stdout") or "",
            stderr=data.get("stderr") or "",
            compile_output=data.get("compile_output") or "",
            time_ms=_to_ms(data.get("time")),
            memory_kb=_to_int(data.get("memory")),
        )


def get_judge_client() -> CodeRunner:
    """Return the runner chosen by the RUNNER setting. Empty means no runner (submissions paused)."""
    settings = get_settings()
    if settings.runner == "piston":
        from app.services.piston_client import PistonClient

        return PistonClient(settings.piston_url, settings.judge0_timeout_seconds)
    if settings.runner == "judge0":
        return Judge0Client(settings.judge0_url, settings.judge0_api_key, settings.judge0_timeout_seconds)
    return Judge0Client("", "", settings.judge0_timeout_seconds)
