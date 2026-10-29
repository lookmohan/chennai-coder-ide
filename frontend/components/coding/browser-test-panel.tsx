"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { browserPython } from "@/features/practice/browser-python-runner";
import { runExamples, type CaseResult } from "@/features/practice/test-runner";
import type { Example } from "@/features/problems/types";
import { cn } from "@/lib/utils";

type Phase = "idle" | "loading" | "running" | "done";

function ResultCard({ result }: { result: CaseResult }) {
  return (
    <div className={cn("space-y-2 rounded border p-3", result.passed ? "border-success/40" : "border-danger/40")}>
      <p className={cn("font-medium", result.passed ? "text-success" : "text-danger")}>
        Example {result.index}: {result.passed ? "Passed" : result.timedOut ? "Too slow" : "Failed"}
      </p>

      {result.timedOut && (
        <p className="text-sm text-muted-foreground">
          This program took longer than the time limit. Check for loops that never finish, or work that repeats too
          much.
        </p>
      )}

      {!result.passed && !result.timedOut && (
        <div className="grid gap-2 sm:grid-cols-2">
          <div>
            <p className="mb-1 text-xs uppercase tracking-wide text-muted-foreground">Expected</p>
            <pre className="overflow-x-auto rounded bg-muted p-2 font-mono text-sm">{result.expected}</pre>
          </div>
          <div>
            <p className="mb-1 text-xs uppercase tracking-wide text-muted-foreground">Your output</p>
            <pre className="overflow-x-auto rounded bg-muted p-2 font-mono text-sm">{result.actual || " "}</pre>
          </div>
        </div>
      )}

      {result.error && (
        // Plain text only. Error messages are shown exactly as Python produced them.
        <pre className="whitespace-pre-wrap break-words rounded bg-muted p-2 font-mono text-xs text-danger">
          {result.error}
        </pre>
      )}
    </div>
  );
}

export function BrowserTestPanel({
  code,
  examples,
  timeLimitMs,
  onAllPassed,
}: {
  code: string;
  examples: Example[];
  timeLimitMs: number;
  /** Called when every visible example passes in one run. */
  onAllPassed?: () => void;
}) {
  const [phase, setPhase] = useState<Phase>("idle");
  const [results, setResults] = useState<CaseResult[]>([]);

  const busy = phase === "loading" || phase === "running";
  const passedCount = results.filter((r) => r.passed).length;
  const stoppedForTime = results.some((r) => r.timedOut);
  const allPassed = results.length > 0 && passedCount === results.length && !stoppedForTime;
  const seconds = (timeLimitMs / 1000).toFixed(0);

  async function runChecks() {
    setPhase("loading");
    setResults([]);
    const outcomes = await runExamples(examples, (stdin) =>
      browserPython.run(code, stdin, timeLimitMs, { onStarted: () => setPhase("running") }),
    );
    setResults(outcomes);
    setPhase("done");

    const everyPassed = outcomes.length > 0 && outcomes.every((r) => r.passed);
    const anyTimedOut = outcomes.some((r) => r.timedOut);
    if (everyPassed && !anyTimedOut) onAllPassed?.();
  }

  return (
    <section aria-labelledby="browser-check-heading" className="space-y-3 rounded-lg border border-border p-4">
      <div className="space-y-1">
        <h3 id="browser-check-heading" className="font-semibold">
          Check against the examples
        </h3>
        <p className="text-sm text-muted-foreground">
          Runs in your browser, so it&apos;s free and your code isn&apos;t sent anywhere for this check. It only uses
          the visible examples. Hidden tests are graded separately when submissions are connected.
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={runChecks} disabled={busy || code.trim().length === 0} loading={busy}>
          {phase === "loading" ? "Loading Python…" : phase === "running" ? "Running…" : "Run examples"}
        </Button>
        <span className="text-xs text-muted-foreground">Time limit per run: {seconds} seconds</span>
      </div>

      {phase === "loading" && (
        <p role="status" className="text-sm text-muted-foreground">
          Loading Python for the browser. The first time can take 10–20 seconds, then it&apos;s quicker.
        </p>
      )}

      {phase === "done" && results.length > 0 && (
        <div role="status" aria-live="polite" className="space-y-3">
          <p className="font-semibold">
            {passedCount} of {results.length} examples passed
            {allPassed ? " — well done! This problem is marked as solved." : ""}
          </p>

          {stoppedForTime && (
            <p className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
              One run went over the time limit, so the remaining examples were skipped.
            </p>
          )}

          {results.map((result) => (
            <ResultCard key={result.index} result={result} />
          ))}
        </div>
      )}
    </section>
  );
}
