from pydantic import BaseModel


class ProblemListItem(BaseModel):
    number: int  # position on the learning path (1 = first)
    slug: str
    title: str
    difficulty: str
    tags: list[str]
    languages: list[str]
    time_limit_ms: int


class Example(BaseModel):
    input: str
    output: str
    explanation: str | None = None


class ProblemDetail(ProblemListItem):
    description: str
    input_format: str | None = None
    output_format: str | None = None
    constraints: str | None = None
    explanation: str | None = None
    memory_limit_mb: int
    examples: list[Example]
    starter_code: dict[str, str]
    # Lets the UI show an honest "setup needed" state instead of a Submit button that fails.
    execution_available: bool
