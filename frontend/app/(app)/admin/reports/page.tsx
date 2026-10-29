"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useReports, useResolveReport, type Report } from "@/features/community/hooks";
import { ApiError } from "@/lib/api";

export default function AdminReportsPage() {
  const [status, setStatus] = useState<Report["status"]>("open");
  const reports = useReports(status);
  const resolve = useResolveReport();
  const [message, setMessage] = useState<string | null>(null);

  function act(report: Report, action: "dismiss" | "remove") {
    setMessage(null);
    resolve.mutate(
      { id: report.id, action },
      {
        onError: (err) => setMessage(err instanceof ApiError ? err.message : "Couldn't save that decision."),
      },
    );
  }

  return (
    <div className="space-y-4">
      <div role="group" aria-label="Report status" className="flex flex-wrap gap-2">
        {(["open", "actioned", "dismissed"] as const).map((value) => (
          <button
            key={value}
            type="button"
            aria-pressed={status === value}
            onClick={() => setStatus(value)}
            className={`h-11 rounded border px-3 text-sm capitalize ${status === value ? "border-primary bg-primary/10 text-primary" : "border-border"}`}
          >
            {value}
          </button>
        ))}
      </div>

      {message && (
        <p role="alert" className="rounded border border-border bg-muted px-3 py-2 text-sm">
          {message}
        </p>
      )}

      {reports.isPending && <Skeleton className="h-48 w-full" />}
      {reports.isError && <ErrorState title="Couldn't load reports" message={reports.error.message} onRetry={() => reports.refetch()} />}
      {reports.data && reports.data.length === 0 && (
        <EmptyState title={`No ${status} reports.`} description="Reports from students appear here." />
      )}

      <ul className="space-y-4">
        {reports.data?.map((report) => (
          <li key={report.id} className="space-y-3 rounded-lg border border-border p-4">
            <p className="text-sm">
              <span className="font-medium">Reason:</span> {report.reason}
            </p>
            <div className="rounded bg-muted p-3 text-sm">
              <p className="mb-1 text-xs text-muted-foreground">
                Post by @{report.post_author} · reported by @{report.reporter_username}
              </p>
              <p className="whitespace-pre-wrap break-words">{report.post_body ?? "(already removed)"}</p>
            </div>
            {report.status === "open" && (
              <div className="flex flex-wrap gap-2">
                <Button size="sm" variant="danger" onClick={() => act(report, "remove")} loading={resolve.isPending}>
                  Remove post
                </Button>
                <Button size="sm" variant="outline" onClick={() => act(report, "dismiss")} disabled={resolve.isPending}>
                  Dismiss report
                </Button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
