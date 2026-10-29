import { describe, expect, it } from "vitest";

import type { RunOutcome } from "@/features/practice/browser-python-runner";
import { normalizeOutput, runExamples } from "@/features/practice/test-runner";

const examples = [
  { input: "2 3\n", output: "5" },
  { input: "10 -4\n", output: "6" },
];

const ok = (stdout: string): RunOutcome => ({ status: "ok", stdout });

describe("normalizeOutput (same rules as the backend)", () => {
  it("ignores line-ending differences and trailing spaces", () => {
    expect(normalizeOutput("5 \r\n")).toBe(normalizeOutput("5"));
  });

  it("ignores surrounding blank lines", () => {
    expect(normalizeOutput("\n\n1 2\n\n")).toBe("1 2");
  });

  it("keeps real differences", () => {
    expect(normalizeOutput("1\n2")).not.toBe(normalizeOutput("12"));
  });
});

describe("runExamples", () => {
  it("passes every example when outputs match", async () => {
    const outputs = ["5\n", "6"];
    const results = await runExamples(examples, async () => ok(outputs.shift() ?? ""));
    expect(results.map((r) => r.passed)).toEqual([true, true]);
  });

  it("shows expected and actual output for a wrong answer", async () => {
    const results = await runExamples(examples, async () => ok("99"));
    expect(results[0].passed).toBe(false);
    expect(results[0].expected).toBe("5");
    expect(results[0].actual).toBe("99");
  });

  it("records a runtime error and still runs the next example", async () => {
    const outcomes: RunOutcome[] = [
      { status: "error", stdout: "", message: "NameError: name 'x' is not defined" },
      ok("6"),
    ];
    const results = await runExamples(examples, async () => outcomes.shift() as RunOutcome);
    expect(results[0].error).toContain("NameError");
    expect(results[0].passed).toBe(false);
    expect(results[1].passed).toBe(true);
  });

  it("stops after a timeout, because the rest would wait just as long", async () => {
    let calls = 0;
    const results = await runExamples(examples, async () => {
      calls += 1;
      return { status: "timeout" };
    });
    expect(calls).toBe(1);
    expect(results).toHaveLength(1);
    expect(results[0].timedOut).toBe(true);
  });

  it("gives each example its own input", async () => {
    const seen: string[] = [];
    await runExamples(examples, async (stdin) => {
      seen.push(stdin);
      return ok("");
    });
    expect(seen).toEqual(["2 3\n", "10 -4\n"]);
  });
});
