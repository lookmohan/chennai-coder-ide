"""Apply detailed problem content to the database.

    python -m app.seed_content

Finds every batch module in app/content (any file named batch*.py that defines BATCH_* lists),
creates problems that don't exist yet as published problems, and updates the ones that do:
statements, examples, explanations and topic. Test cases are rebuilt from each batch.
Problems not in any batch are left as they are.
"""
import importlib
import pkgutil

from sqlalchemy import select

import app.content as content_pkg
from app.content.topics import SLUG_TOPIC
from app.core.database import get_session_factory
from app.models import Problem, ProblemStatus, ProblemTestCase


def load_batches() -> list[list[dict]]:
    batches: list[list[dict]] = []
    for info in sorted(pkgutil.iter_modules(content_pkg.__path__), key=lambda m: m.name):
        if not info.name.startswith("batch"):
            continue
        module = importlib.import_module(f"app.content.{info.name}")
        for name in sorted(dir(module)):
            if name.startswith("BATCH_"):
                batches.append(getattr(module, name))
    return batches


def main() -> None:
    db = get_session_factory()()
    created = 0
    updated = 0
    try:
        for batch in load_batches():
            for spec in batch:
                problem = db.scalar(select(Problem).where(Problem.slug == spec["slug"]))
                if problem is None:
                    problem = Problem(
                        slug=spec["slug"],
                        difficulty=spec.get("difficulty", "Easy"),
                        status=ProblemStatus.published.value,
                        sort_order=spec.get("sort_order", 1000),
                        tags=spec.get("tags", []),
                        time_limit_ms=2000,
                        memory_limit_mb=256,
                        starter_code={"python": "# Write your solution here\n"},
                    )
                    db.add(problem)
                    created += 1
                else:
                    updated += 1

                problem.title = spec["title"]
                problem.description = spec["description"]
                problem.input_format = spec["input_format"]
                problem.output_format = spec["output_format"]
                problem.constraints = spec["constraints"]
                problem.explanation = spec["explanation"]
                problem.topic_slug = spec.get("topic") or SLUG_TOPIC.get(spec["slug"])

                # Remove the old tests first and flush, so the new ones can reuse their positions.
                for old in list(problem.test_cases):
                    db.delete(old)
                db.flush()
                problem.test_cases = [
                    ProblemTestCase(
                        position=i,
                        stdin=t["in"],
                        expected_output=t["out"],
                        is_hidden=t["hidden"],
                        explanation=t["why"],
                    )
                    for i, t in enumerate(spec["tests"], start=1)
                ]
        db.commit()
    finally:
        db.close()

    print(f"Created {created} and updated {updated} problem(s) from the content batches.")


if __name__ == "__main__":
    main()
