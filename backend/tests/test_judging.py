import uuid

from app.models import Submission, SubmissionStatus as S
from app.services.judge0_client import ExecutionUnavailable
from app.services.judging import judge_submission, normalize_output
from tests.problem_helpers import FakeRunner, make_problem, make_submission, make_user, run_result

PUBLIC = {"in": "1\n", "out": "2", "hidden": False}
HIDDEN = {"in": "5\n", "out": "6", "hidden": True}


def _judge(session_factory, tests, results, *, configured=True, already_status=None):
    user_id = make_user(session_factory)
    problem_id = make_problem(session_factory, tests=tests)
    sub_id = uuid.UUID(make_submission(session_factory, user_id, problem_id))
    runner = FakeRunner(results, configured=configured)

    db = session_factory()
    try:
        if already_status:
            db.get(Submission, sub_id).status = already_status
            db.commit()
        sub = judge_submission(db, sub_id, client=runner)
        return sub, runner
    finally:
        db.close()


def test_all_tests_pass_is_accepted(session_factory):
    sub, runner = _judge(session_factory, [PUBLIC, HIDDEN], [run_result(stdout="2\n"), run_result(stdout="6")])
    assert sub.status == S.accepted.value
    assert sub.passed_count == 2 and sub.total_count == 2
    assert sub.failed_test_position is None
    assert sub.runtime_ms == 10 and sub.memory_kb == 2048
    assert len(runner.calls) == 2


def test_output_comparison_ignores_trailing_whitespace_and_crlf():
    assert normalize_output("5 \r\n") == normalize_output("5")
    assert normalize_output("\n\n1 2\n\n") == "1 2"
    assert normalize_output("1\n2") != normalize_output("12")


def test_hidden_wrong_answer_does_not_reveal_input_or_expected_output(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC, HIDDEN], [run_result(stdout="2"), run_result(stdout="9")])
    assert sub.status == S.wrong_answer.value
    assert sub.failed_test_position == 2
    assert sub.passed_count == 1
    assert sub.message == "Wrong answer on hidden test 2 of 2."
    # Neither the hidden input (5), its expected output (6) nor the wrong output (9) may leak.
    for leaked in ("9", "6", "5"):
        assert leaked not in sub.message


def test_public_wrong_answer_shows_input_expected_and_actual(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC], [run_result(stdout="3")])
    assert sub.status == S.wrong_answer.value
    assert "Expected" in sub.message and "'2'" in sub.message and "'3'" in sub.message


def test_compilation_error(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC], [run_result(status_id=6, compile_output="main.py: SyntaxError")])
    assert sub.status == S.compilation_error.value
    assert "SyntaxError" in sub.message


def test_time_limit_exceeded(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC], [run_result(status_id=5)])
    assert sub.status == S.time_limit_exceeded.value


def test_runtime_error_hides_stderr_for_hidden_tests(session_factory):
    sub, _ = _judge(
        session_factory, [PUBLIC, HIDDEN], [run_result(stdout="2"), run_result(status_id=11, stderr="secret trace")]
    )
    assert sub.status == S.runtime_error.value
    assert "secret trace" not in sub.message


def test_memory_limit_exceeded_detected_from_status_description(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC], [run_result(status_id=12, description="Memory limit exceeded")])
    assert sub.status == S.memory_limit_exceeded.value


def test_runner_unreachable_becomes_system_error_not_a_fake_verdict(session_factory):
    sub, _ = _judge(session_factory, [PUBLIC], [ExecutionUnavailable("down")])
    assert sub.status == S.system_error.value
    assert sub.passed_count == 0
    assert "unavailable" in sub.message


def test_unconfigured_runner_is_system_error_and_never_calls_runner(session_factory):
    sub, runner = _judge(session_factory, [PUBLIC], [], configured=False)
    assert sub.status == S.system_error.value
    assert runner.calls == []


def test_judging_is_idempotent_for_finished_submissions(session_factory):
    sub, runner = _judge(session_factory, [PUBLIC], [run_result(stdout="2")], already_status="ACCEPTED")
    assert sub.status == "ACCEPTED"
    assert runner.calls == []
