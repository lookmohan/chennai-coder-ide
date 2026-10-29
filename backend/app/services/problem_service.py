from app.models import Problem
from app.schemas.problem import Example, ProblemDetail, ProblemListItem
from app.services.judge0_client import SUPPORTED_LANGUAGES


def supported_languages(problem: Problem) -> list[str]:
    return sorted(lang for lang in (problem.starter_code or {}) if lang in SUPPORTED_LANGUAGES)


def to_list_item(problem: Problem) -> ProblemListItem:
    return ProblemListItem(
        number=problem.sort_order,
        slug=problem.slug,
        title=problem.title,
        difficulty=problem.difficulty,
        tags=list(problem.tags or []),
        languages=supported_languages(problem),
        time_limit_ms=problem.time_limit_ms,
    )


def to_detail(problem: Problem, *, execution_available: bool) -> ProblemDetail:
    # Only visible examples leave the server. Hidden tests are never serialised.
    examples = [
        Example(input=t.stdin, output=t.expected_output, explanation=t.explanation)
        for t in sorted(problem.test_cases, key=lambda t: t.position)
        if not t.is_hidden
    ]
    base = to_list_item(problem)
    return ProblemDetail(
        **base.model_dump(),
        description=problem.description,
        input_format=problem.input_format,
        output_format=problem.output_format,
        constraints=problem.constraints,
        explanation=problem.explanation,
        memory_limit_mb=problem.memory_limit_mb,
        examples=examples,
        starter_code={lang: problem.starter_code[lang] for lang in base.languages},
        execution_available=execution_available,
    )
