export const DIFFICULTIES = ["Easy", "Medium", "Hard"] as const;
export type Difficulty = (typeof DIFFICULTIES)[number];

export type ProblemListItem = {
  number: number;
  slug: string;
  title: string;
  difficulty: Difficulty;
  tags: string[];
  languages: string[];
  time_limit_ms: number;
};

/** An example students can see. The explanation is optional: not every example needs one. */
export type Example = { input: string; output: string; explanation?: string | null };

export type ProblemDetail = ProblemListItem & {
  description: string;
  input_format: string | null;
  output_format: string | null;
  constraints: string | null;
  explanation: string | null;
  memory_limit_mb: number;
  examples: Example[];
  starter_code: Record<string, string>;
  execution_available: boolean;
};

export type SubmissionStatus =
  | "QUEUED"
  | "RUNNING"
  | "ACCEPTED"
  | "WRONG_ANSWER"
  | "COMPILATION_ERROR"
  | "RUNTIME_ERROR"
  | "TIME_LIMIT_EXCEEDED"
  | "MEMORY_LIMIT_EXCEEDED"
  | "SYSTEM_ERROR";

export type Submission = {
  id: string;
  problem_slug: string;
  language: string;
  source_code: string;
  status: SubmissionStatus;
  passed_count: number;
  total_count: number;
  failed_test_position: number | null;
  runtime_ms: number | null;
  memory_kb: number | null;
  message: string | null;
  created_at: string;
  judged_at: string | null;
};

export type PageMeta = { page: number; page_size: number; total: number };
