"use client";

import { cn } from "@/lib/utils";
import { STATUS_COPY, type StatusTone } from "@/features/problems/status";
import type { Submission } from "@/features/problems/types";

const TONE: Record<StatusTone, string> = {
  success: "text-success",
  warning: "text-foreground",
  pending: "text-primary",
  error: "text-danger",
};

export function SubmissionPanel({ submission, pending }: { submission: Submission | null; pending: boolean }) {
  if (pending && !submission) {
    return (
      <p role="status" className="text-sm text-muted-foreground">
        Sending your code to the judge…
      </p>
    );
  }
  if (!submission) {
    return (
      <p className="text-sm text-muted-foreground">
        Your results will appear here after you submit. Mistakes are part of learning, so experiment freely.
      </p>
    );
  }

  const copy = STATUS_COPY[submission.status];
  return (
    <div role="status" aria-live="polite" className="space-y-3 rounded border border-border p-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className={cn("font-semibold", TONE[copy.tone])}>{copy.label}</p>
        <p className="text-sm text-muted-foreground">
          {submission.passed_count} of {submission.total_count} tests passed
        </p>
      </div>
      <p className="text-sm">{copy.encouragement}</p>
      {submission.message && (
        // Plain text only. Never render judge output as HTML.
        <pre className="whitespace-pre-wrap break-words rounded bg-muted p-3 font-mono text-sm">{submission.message}</pre>
      )}
      {submission.runtime_ms !== null && (
        <p className="text-xs text-muted-foreground">
          Runtime {submission.runtime_ms} ms
          {submission.memory_kb ? ` · Memory ${Math.max(1, Math.round(submission.memory_kb / 1024))} MB` : ""}
        </p>
      )}
    </div>
  );
}
