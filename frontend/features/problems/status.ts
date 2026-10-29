import type { Difficulty, SubmissionStatus } from "./types";

/** Final statuses stop the polling loop. QUEUED and RUNNING keep it going. */
const FINAL: readonly SubmissionStatus[] = [
  "ACCEPTED",
  "WRONG_ANSWER",
  "COMPILATION_ERROR",
  "RUNTIME_ERROR",
  "TIME_LIMIT_EXCEEDED",
  "MEMORY_LIMIT_EXCEEDED",
  "SYSTEM_ERROR",
];

export function isFinal(status: string | undefined | null): boolean {
  return !!status && (FINAL as readonly string[]).includes(status);
}

export type StatusTone = "success" | "warning" | "pending" | "error";

export const STATUS_COPY: Record<SubmissionStatus, { label: string; tone: StatusTone; encouragement: string }> = {
  QUEUED: {
    label: "In the queue",
    tone: "pending",
    encouragement: "Your code is waiting for a judge. This usually takes just a moment.",
  },
  RUNNING: {
    label: "Running",
    tone: "pending",
    encouragement: "Testing your code against every case. Hang tight.",
  },
  ACCEPTED: {
    label: "Accepted",
    tone: "success",
    encouragement: "You solved it. Take a breath and enjoy that. Ready for the next one?",
  },
  WRONG_ANSWER: {
    label: "Not quite yet",
    tone: "warning",
    encouragement: "Your code runs, but the answer differs somewhere. Compare your output with the example. Every wrong answer teaches you something.",
  },
  COMPILATION_ERROR: {
    label: "Didn't compile",
    tone: "warning",
    encouragement: "The computer couldn't read your code. Read the message below, fix the small mistake, and try again.",
  },
  RUNTIME_ERROR: {
    label: "Crashed on one input",
    tone: "warning",
    encouragement: "Your code stopped on one of the inputs. Think about the edge cases, like empty or very large values.",
  },
  TIME_LIMIT_EXCEEDED: {
    label: "Too slow",
    tone: "warning",
    encouragement: "Your answer is right, but it takes too long. Can you find a way that does less work?",
  },
  MEMORY_LIMIT_EXCEEDED: {
    label: "Too much memory",
    tone: "warning",
    encouragement: "Your code stores more than it needs. Try keeping fewer values at once.",
  },
  SYSTEM_ERROR: {
    label: "Something went wrong",
    tone: "error",
    encouragement: "This was a problem on our side, not with your code. Your attempt is saved. Please try again.",
  },
};

export function difficultyStage(difficulty: Difficulty): string {
  return { Easy: "Warm-up", Medium: "Building blocks", Hard: "Level up" }[difficulty];
}
