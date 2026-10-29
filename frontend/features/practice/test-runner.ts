import type { Example } from "@/features/problems/types";
import type { RunOutcome } from "./browser-python-runner";

export type CaseResult = {
  /** 1-based position in the example list, as students see it. */
  index: number;
  passed: boolean;
  input: string;
  expected: string;
  actual: string;
  error: string | null;
  timedOut: boolean;
};

/** Same rules as the backend: ignore line-ending differences, trailing spaces and surrounding blank lines. */
export function normalizeOutput(text: string): string {
  return text
    .replace(/\r\n?/g, "\n")
    .trim()
    .split("\n")
    .map((line) => line.trimEnd())
    .join("\n");
}

/**
 * Run the example tests one after another and compare each output with the expected output.
 * A program that errors is recorded and the next example still runs.
 * A program that goes over the time limit stops the run, since every extra example would wait just as long.
 */
export async function runExamples(
  examples: Example[],
  runOne: (stdin: string) => Promise<RunOutcome>,
): Promise<CaseResult[]> {
  const results: CaseResult[] = [];

  for (const [position, example] of examples.entries()) {
    const index = position + 1;
    const outcome = await runOne(example.input);

    if (outcome.status === "timeout") {
      results.push({
        index,
        passed: false,
        input: example.input,
        expected: example.output,
        actual: "",
        error: null,
        timedOut: true,
      });
      break;
    }

    if (outcome.status === "error") {
      results.push({
        index,
        passed: false,
        input: example.input,
        expected: example.output,
        actual: outcome.stdout,
        error: outcome.message,
        timedOut: false,
      });
      continue;
    }

    results.push({
      index,
      passed: normalizeOutput(outcome.stdout) === normalizeOutput(example.output),
      input: example.input,
      expected: example.output,
      actual: outcome.stdout,
      error: null,
      timedOut: false,
    });
  }

  return results;
}
