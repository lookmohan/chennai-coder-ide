import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Problem, ProblemTestCase, Submission, SubmissionStatus as S
from app.services.judge0_client import ExecutionUnavailable, Judge0Client, RunResult, get_judge_client

logger = logging.getLogger("app.judging")

MAX_MESSAGE_CHARS = 500
# Judge0 status ids for runtime failures (signals and other non-zero exits).
RUNTIME_ERROR_IDS = {7, 8, 9, 10, 11, 12, 14}
LABELS = {
    S.wrong_answer: "Wrong answer",
    S.time_limit_exceeded: "Time limit exceeded",
    S.runtime_error: "Runtime error",
    S.memory_limit_exceeded: "Memory limit exceeded",
}


def normalize_output(text: str) -> str:
    """Ignore line-ending differences, trailing spaces and surrounding blank lines."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").strip().split("\n")
    return "\n".join(line.rstrip() for line in lines)


def classify(result: RunResult, expected: str) -> S:
    if result.status_id == 3:  # ran to completion; compare the output ourselves
        same = normalize_output(result.stdout) == normalize_output(expected)
        return S.accepted if same else S.wrong_answer
    if result.status_id == 5:
        return S.time_limit_exceeded
    if result.status_id == 6:
        return S.compilation_error
    if result.status_id in RUNTIME_ERROR_IDS:
        if "memory" in result.status_description.lower():
            return S.memory_limit_exceeded
        return S.runtime_error
    return S.system_error


def _clip(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def failure_message(verdict: S, position: int, total: int, test: ProblemTestCase, result: RunResult) -> str:
    if verdict == S.compilation_error:
        return _clip(f"Compilation error: {result.compile_output or result.stderr}", MAX_MESSAGE_CHARS)

    label = LABELS.get(verdict, "Failed")
    if test.is_hidden:
        # Hidden tests: say which one failed, never its input, expected output or stderr.
        return f"{label} on hidden test {position} of {total}."

    parts = [f"{label} on example test {position} of {total}."]
    if verdict == S.wrong_answer:
        parts.append(
            f"Input: {_clip(test.stdin, 150)!r}. Expected: {_clip(test.expected_output, 150)!r}. "
            f"Your output: {_clip(result.stdout, 150)!r}."
        )
    elif verdict in (S.runtime_error, S.memory_limit_exceeded):
        parts.append(f"Error: {_clip(result.stderr or result.status_description, 200)}")
    return _clip(" ".join(parts), MAX_MESSAGE_CHARS)


def _max(a: int | None, b: int | None) -> int | None:
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def _finish(
    db: Session,
    sub: Submission,
    status: S,
    message: str,
    *,
    failed_position: int | None = None,
    runtime_ms: int | None = None,
    memory_kb: int | None = None,
) -> Submission:
    sub.status = status.value
    sub.message = message[:MAX_MESSAGE_CHARS]
    sub.failed_test_position = failed_position
    sub.runtime_ms = runtime_ms
    sub.memory_kb = memory_kb
    sub.judged_at = datetime.now(timezone.utc)
    db.commit()
    return sub


def judge_submission(db: Session, submission_id: uuid.UUID, client: Judge0Client | None = None) -> Submission | None:
    """Run every test for a queued submission and record the verdict.

    Idempotent: a submission that is no longer QUEUED is returned unchanged.
    """
    sub = db.get(Submission, submission_id)
    if sub is None or sub.status != S.queued.value:
        return sub

    problem = db.get(Problem, sub.problem_id)
    tests = sorted(problem.test_cases, key=lambda t: t.position)
    sub.status = S.running.value
    sub.total_count = len(tests)
    db.commit()

    try:
        runner = client or get_judge_client()
        if not runner.configured:
            return _finish(db, sub, S.system_error, "Code execution is not configured on this server.")
        if not tests:
            return _finish(db, sub, S.system_error, "This problem has no test cases yet.")

        runtime_ms: int | None = None
        memory_kb: int | None = None
        total = len(tests)
        for position, test in enumerate(tests, start=1):
            result = runner.run(
                source_code=sub.source_code,
                language=sub.language,
                stdin=test.stdin,
                time_limit_s=problem.time_limit_ms / 1000,
                memory_limit_kb=problem.memory_limit_mb * 1024,
            )
            runtime_ms = _max(runtime_ms, result.time_ms)
            memory_kb = _max(memory_kb, result.memory_kb)

            verdict = classify(result, test.expected_output)
            if verdict != S.accepted:
                return _finish(
                    db,
                    sub,
                    verdict,
                    failure_message(verdict, position, total, test, result),
                    failed_position=position,
                    runtime_ms=runtime_ms,
                    memory_kb=memory_kb,
                )
            sub.passed_count += 1

        return _finish(db, sub, S.accepted, "All tests passed.", runtime_ms=runtime_ms, memory_kb=memory_kb)

    except ExecutionUnavailable:
        logger.warning("judge_runner_unavailable", extra={"submission_id": str(submission_id)})
        db.rollback()
        return _finish(db, sub, S.system_error, "The code runner is unavailable right now. Please try again shortly.")
    except Exception:
        logger.exception("judging_failed", extra={"submission_id": str(submission_id)})
        db.rollback()
        return _finish(db, sub, S.system_error, "Unexpected error while judging. Please try again.")
