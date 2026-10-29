"""Client for the Piston code execution API (github.com/engineer-man/piston).

Piston's answers are translated into the same status ids Judge0 uses, so the
judging rules in judging.py work unchanged for either runner.

Known limitation: Piston does not report time or memory per run, so runtime and
memory figures are blank, and a run killed with SIGKILL is reported as a time
limit exceeded (a memory-limit kill looks the same).
"""
import httpx

from app.services.judge0_client import ExecutionUnavailable, RunResult

# Our language name -> (Piston language name, file name the code is saved as).
PISTON_LANGUAGES: dict[str, tuple[str, str]] = {
    "python": ("python", "main.py"),
    "javascript": ("javascript", "main.js"),
    "java": ("java", "Main.java"),
    "cpp": ("c++", "main.cpp"),
}

STATUS_ACCEPTED_RUN = 3
STATUS_TIME_LIMIT = 5
STATUS_COMPILATION_ERROR = 6
STATUS_RUNTIME_ERROR = 11


class PistonClient:
    def __init__(self, base_url: str, timeout_seconds: float) -> None:
        self.base_url = base_url.rstrip("/")
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
        if language not in PISTON_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        piston_language, filename = PISTON_LANGUAGES[language]

        payload = {
            "language": piston_language,
            "version": "*",  # use the installed version of this language
            "files": [{"name": filename, "content": source_code}],
            "stdin": stdin,
            "run_timeout": int(time_limit_s * 1000),
            "run_memory_limit": memory_limit_kb * 1024,  # Piston takes bytes
        }
        try:
            response = httpx.post(f"{self.base_url}/execute", json=payload, timeout=self.timeout_seconds)
        except httpx.HTTPError as exc:
            raise ExecutionUnavailable("Could not reach the code runner.") from exc

        if response.status_code == 429:
            raise ExecutionUnavailable("The free code runner is busy right now. Please try again in a moment.")
        if response.status_code >= 400:
            raise ExecutionUnavailable(f"Code runner responded with HTTP {response.status_code}.")

        return _to_run_result(response.json())


def _to_run_result(data: dict) -> RunResult:
    compile_step = data.get("compile")
    if compile_step and (compile_step.get("code") or 0) != 0:
        message = compile_step.get("stderr") or compile_step.get("output") or ""
        return RunResult(
            status_id=STATUS_COMPILATION_ERROR,
            status_description="Compilation error",
            stdout="",
            stderr=message,
            compile_output=message,
            time_ms=None,
            memory_kb=None,
        )

    run = data.get("run") or {}
    stdout = run.get("stdout") or ""
    stderr = run.get("stderr") or ""

    if run.get("signal") == "SIGKILL":
        return RunResult(STATUS_TIME_LIMIT, "Time limit exceeded", stdout, stderr, "", None, None)
    if (run.get("code") or 0) != 0:
        return RunResult(STATUS_RUNTIME_ERROR, "Runtime error", stdout, stderr, "", None, None)
    return RunResult(STATUS_ACCEPTED_RUN, "Accepted", stdout, stderr, "", None, None)
