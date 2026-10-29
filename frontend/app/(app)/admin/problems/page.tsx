"use client";

import Link from "next/link";
import { useState } from "react";

import { Button, buttonClasses } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useAdminProblems, useSetProblemStatus, type ProblemRow } from "@/features/admin/hooks";
import { ApiError } from "@/lib/api";
import { useMe } from "@/features/auth/hooks";

const STATUS_STYLE: Record<ProblemRow["status"], string> = {
  draft: "bg-muted text-muted-foreground",
  published: "bg-success/10 text-success",
  archived: "bg-danger/10 text-danger",
};

export default function AdminProblemsPage() {
  const { data: me } = useMe();
  const canEdit = me?.role === "admin";
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [status, setStatus] = useState("");
  const list = useAdminProblems(page, q, status);
  const setStatusMutation = useSetProblemStatus();
  const [message, setMessage] = useState<string | null>(null);

  function changeStatus(row: ProblemRow, next: ProblemRow["status"]) {
    setMessage(null);
    setStatusMutation.mutate(
      { id: row.id, status: next },
      {
        onError: (err) => setMessage(err instanceof ApiError ? err.message : "Couldn't change the status."),
      },
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div className="flex flex-col gap-3 md:flex-row md:items-end">
          <div className="md:w-64">
            <Input
              label="Search by title"
              type="search"
              value={q}
              onChange={(e) => {
                setQ(e.target.value);
                setPage(1);
              }}
            />
          </div>
          <div role="group" aria-label="Filter by status" className="flex flex-wrap gap-2">
            {["", "draft", "published", "archived"].map((value) => (
              <button
                key={value || "all"}
                type="button"
                aria-pressed={status === value}
                onClick={() => {
                  setStatus(value);
                  setPage(1);
                }}
                className={`h-11 rounded border px-3 text-sm ${status === value ? "border-primary bg-primary/10 text-primary" : "border-border"}`}
              >
                {value ? value[0].toUpperCase() + value.slice(1) : "All"}
              </button>
            ))}
          </div>
        </div>
        {canEdit && (
          <Link href="/admin/problems/new" className={buttonClasses({ size: "md" })}>
            New problem
          </Link>
        )}
      </div>

      {message && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {message}
        </p>
      )}

      {list.isPending && <Skeleton className="h-64 w-full" />}
      {list.isError && (
        <ErrorState title="Couldn't load problems" message={list.error.message} onRetry={() => list.refetch()} />
      )}

      {list.data && list.data.items.length === 0 && (
        <EmptyState
          title="No problems here yet."
          description={canEdit ? "Create the first problem with New problem." : "Problems appear here once they're created."}
        />
      )}

      {list.data && list.data.items.length > 0 && (
        <div className="overflow-x-auto rounded-lg border border-border">
          <table className="w-full text-left text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                <th className="px-4 py-3 font-medium">#</th>
                <th className="px-4 py-3 font-medium">Title</th>
                <th className="px-4 py-3 font-medium">Level</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Tests</th>
                <th className="px-4 py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {list.data.items.map((row) => (
                <tr key={row.id} className="border-t border-border align-middle">
                  <td className="px-4 py-3">{row.sort_order}</td>
                  <td className="px-4 py-3">
                    <p className="font-medium">{row.title}</p>
                    <p className="text-xs text-muted-foreground">{row.slug}</p>
                  </td>
                  <td className="px-4 py-3">{row.difficulty}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded px-2 py-0.5 text-xs font-medium capitalize ${STATUS_STYLE[row.status]}`}>
                      {row.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {row.test_count} ({row.visible_count} visible)
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-2">
                      {canEdit && (
                        <Link href={`/admin/problems/${row.id}`} className={buttonClasses({ variant: "outline", size: "sm" })}>
                          Edit
                        </Link>
                      )}
                      {row.status !== "published" && canEdit && (
                        <Button size="sm" onClick={() => changeStatus(row, "published")} disabled={setStatusMutation.isPending}>
                          Publish
                        </Button>
                      )}
                      {row.status === "published" && canEdit && (
                        <Button variant="outline" size="sm" onClick={() => changeStatus(row, "draft")} disabled={setStatusMutation.isPending}>
                          Unpublish
                        </Button>
                      )}
                      {row.status !== "archived" && canEdit && (
                        <Button variant="ghost" size="sm" onClick={() => changeStatus(row, "archived")} disabled={setStatusMutation.isPending}>
                          Archive
                        </Button>
                      )}
                      {row.status === "published" && (
                        <Link href={`/problems/${row.slug}`} className={buttonClasses({ variant: "ghost", size: "sm" })}>
                          Preview
                        </Link>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {list.data && list.data.meta.total > 25 && (
        <nav aria-label="Pages" className="flex items-center justify-between">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            Previous
          </Button>
          <p className="text-sm text-muted-foreground">Page {page}</p>
          <Button variant="outline" size="sm" disabled={page * 25 >= list.data.meta.total} onClick={() => setPage((p) => p + 1)}>
            Next
          </Button>
        </nav>
      )}
    </div>
  );
}
