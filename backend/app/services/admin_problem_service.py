from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import AuditLog, Problem, ProblemTestCase, User
from app.repositories import problem_repository as problems
from app.schemas.admin import ProblemAdminOut, ProblemIn, ProblemRowOut, TestCaseOut
from app.services import audit_service


def _slug_taken(db: Session, slug: str, except_id=None) -> bool:
    stmt = select(Problem.id).where(Problem.slug == slug)
    if except_id is not None:
        stmt = stmt.where(Problem.id != except_id)
    return db.scalar(stmt) is not None


def _apply(db: Session, problem: Problem, data: ProblemIn) -> None:
    problem.slug = data.slug
    problem.title = data.title
    problem.description = data.description
    problem.difficulty = data.difficulty
    problem.status = data.status
    problem.sort_order = data.sort_order
    problem.tags = data.tags
    problem.input_format = data.input_format
    problem.output_format = data.output_format
    problem.constraints = data.constraints
    problem.explanation = data.explanation
    problem.time_limit_ms = data.time_limit_ms
    problem.memory_limit_mb = data.memory_limit_mb
    problem.starter_code = data.starter_code

    # Replace the tests: remove the old rows and flush first, so new positions can reuse them.
    for old in list(problem.test_cases):
        db.delete(old)
    db.flush()
    problem.test_cases = [
        ProblemTestCase(
            position=i,
            stdin=t.stdin,
            expected_output=t.expected_output,
            is_hidden=t.is_hidden,
            explanation=t.explanation,
        )
        for i, t in enumerate(data.tests, start=1)
    ]


def to_admin_out(problem: Problem) -> ProblemAdminOut:
    tests = sorted(problem.test_cases, key=lambda t: t.position)
    return ProblemAdminOut(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        description=problem.description,
        difficulty=problem.difficulty,
        status=problem.status,
        sort_order=problem.sort_order,
        tags=list(problem.tags or []),
        input_format=problem.input_format,
        output_format=problem.output_format,
        constraints=problem.constraints,
        explanation=problem.explanation,
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
        starter_code=dict(problem.starter_code or {}),
        tests=[
            TestCaseOut(
                position=t.position,
                stdin=t.stdin,
                expected_output=t.expected_output,
                is_hidden=t.is_hidden,
                explanation=t.explanation,
            )
            for t in tests
        ],
        updated_at=problem.updated_at,
    )


def to_row_out(problem: Problem) -> ProblemRowOut:
    tests = problem.test_cases
    return ProblemRowOut(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        difficulty=problem.difficulty,
        status=problem.status,
        sort_order=problem.sort_order,
        test_count=len(tests),
        visible_count=sum(1 for t in tests if not t.is_hidden),
        updated_at=problem.updated_at,
    )


def list_problems(db: Session, *, page: int, page_size: int, q: str | None, status: str | None):
    return problems.list_all(db, page=page, page_size=page_size, q=q, status=status)


def get_problem(db: Session, problem_id) -> Problem:
    problem = problems.get_by_id(db, problem_id)
    if problem is None:
        raise AppError("PROBLEM_NOT_FOUND", "Problem not found.", 404)
    return problem


def create_problem(db: Session, actor: User, data: ProblemIn, *, ip: str | None) -> Problem:
    if _slug_taken(db, data.slug):
        raise AppError("SLUG_TAKEN", "A problem with this address (slug) already exists.", 409)

    problem = Problem(created_by=actor.id)
    _apply(db, problem, data)
    db.add(problem)
    db.flush()
    audit_service.record(
        db,
        "problem.create",
        actor_id=actor.id,
        entity_type="problem",
        entity_id=str(problem.id),
        metadata={"slug": data.slug, "status": data.status},
        ip=ip,
    )
    db.commit()
    db.refresh(problem)
    return problem


def update_problem(db: Session, actor: User, problem: Problem, data: ProblemIn, *, ip: str | None) -> Problem:
    if _slug_taken(db, data.slug, except_id=problem.id):
        raise AppError("SLUG_TAKEN", "A problem with this address (slug) already exists.", 409)

    _apply(db, problem, data)
    audit_service.record(
        db,
        "problem.update",
        actor_id=actor.id,
        entity_type="problem",
        entity_id=str(problem.id),
        metadata={"slug": data.slug, "status": data.status},
        ip=ip,
    )
    db.commit()
    db.refresh(problem)
    return problem


def set_status(db: Session, actor: User, problem: Problem, status: str, *, ip: str | None) -> Problem:
    if status == "published" and not any(not t.is_hidden for t in problem.test_cases):
        # A problem students can open must show at least one example to explain itself.
        raise AppError(
            "PROBLEM_NOT_READY",
            "Add at least one visible example before publishing.",
            409,
        )
    previous = problem.status
    problem.status = status
    audit_service.record(
        db,
        "problem.status",
        actor_id=actor.id,
        entity_type="problem",
        entity_id=str(problem.id),
        metadata={"from": previous, "to": status, "slug": problem.slug},
        ip=ip,
    )
    db.commit()
    db.refresh(problem)
    return problem


def overview(db: Session) -> dict:
    now = datetime.now(timezone.utc)
    students = db.scalar(select(func.count(User.id)).where(User.role == "student")) or 0
    active = (
        db.scalar(
            select(func.count(User.id)).where(
                User.role == "student", User.last_login_at >= now - timedelta(days=7)
            )
        )
        or 0
    )
    counts = dict(db.execute(select(Problem.status, func.count(Problem.id)).group_by(Problem.status)).all())
    return {
        "students": students,
        "active_students_7d": active,
        "problems_published": counts.get("published", 0),
        "problems_draft": counts.get("draft", 0),
        "problems_archived": counts.get("archived", 0),
    }


def recent_audit(db: Session, limit: int) -> list[AuditLog]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)).all())
