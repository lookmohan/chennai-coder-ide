import uuid

from app.models import Problem, ProblemTestCase, Profile, Submission, User
from app.models import SubmissionStatus as S
from app.services.judge0_client import RunResult


def make_user(session_factory, email="judge@example.com", username="judgeuser") -> str:
    db = session_factory()
    try:
        user = User(email=email, password_hash=None, role="student", status="active")
        user.profile = Profile(display_name="Judge User", username=username)
        db.add(user)
        db.commit()
        return str(user.id)
    finally:
        db.close()


def make_problem(session_factory, *, slug="sum", status="published", tests=None, starter=None) -> str:
    db = session_factory()
    try:
        problem = Problem(
            slug=slug,
            title=slug.replace("-", " ").title(),
            description="Test problem.",
            difficulty="Easy",
            status=status,
            tags=["Math"],
            time_limit_ms=2000,
            memory_limit_mb=256,
            starter_code=starter if starter is not None else {"python": "# code\n"},
        )
        problem.test_cases = [
            ProblemTestCase(
                position=i,
                stdin=t["in"],
                expected_output=t["out"],
                is_hidden=t.get("hidden", True),
            )
            for i, t in enumerate(tests or [], start=1)
        ]
        db.add(problem)
        db.commit()
        return str(problem.id)
    finally:
        db.close()


def make_submission(session_factory, user_id: str, problem_id: str, source="print(1)", language="python") -> str:
    # Column types expect uuid.UUID objects, not strings: convert before inserting.
    db = session_factory()
    try:
        sub = Submission(
            user_id=uuid.UUID(str(user_id)),
            problem_id=uuid.UUID(str(problem_id)),
            language=language,
            source_code=source,
            status=S.queued.value,
            total_count=0,
        )
        db.add(sub)
        db.commit()
        return str(sub.id)
    finally:
        db.close()


def run_result(status_id=3, stdout="", stderr="", compile_output="", description="", time_ms=10, memory_kb=2048):
    return RunResult(
        status_id=status_id,
        status_description=description,
        stdout=stdout,
        stderr=stderr,
        compile_output=compile_output,
        time_ms=time_ms,
        memory_kb=memory_kb,
    )


class FakeRunner:
    """Stands in for Judge0. Each call pops the next item: a RunResult, or an exception to raise."""

    def __init__(self, results, configured=True):
        self.results = list(results)
        self.configured = configured
        self.calls = []

    def run(self, **kwargs):
        self.calls.append(kwargs)
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item
