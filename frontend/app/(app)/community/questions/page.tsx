"use client";

import Link from "next/link";
import { useState } from "react";

import { Button, buttonClasses } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useLatestThreads } from "@/features/community/latest";

export default function CommunityQuestionsPage() {
  const [page, setPage] = useState(1);
  const { data, isPending, isError, error, refetch } = useLatestThreads(page);

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Community</h1>
        <div role="tablist" aria-label="Community sections" className="flex gap-2 border-b border-border pb-3">
          <Link href="/community" role="tab" aria-selected={false} className="rounded px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted">
            Chat
          </Link>
          <span role="tab" aria-selected className="rounded bg-primary/10 px-3 py-2 text-sm font-medium text-primary">
            Questions
          </span>
        </div>
        <p className="text-muted-foreground">The newest questions from every problem. Pick one to join the discussion.</p>
      </header>

      {isPending && <Skeleton className="h-48 w-full" />}
      {isError && <ErrorState title="Couldn't load the questions" message={error.message} onRetry={() => refetch()} />}

      {data && data.length === 0 && page === 1 && (
        <EmptyState
          title="No questions yet."
          description="Open any problem and use its Discussion link to ask the first question."
          action={
            <Link href="/problems" className={buttonClasses({ variant: "outline", size: "sm" })}>
              Browse problems
            </Link>
          }
        />
      )}

      <ul className="space-y-3">
        {data?.map((row) => (
          <li key={row.post.id}>
            <Link
              href={`/problems/${row.problem_slug}/discussion`}
              className="block rounded-lg border border-border bg-card p-4 transition-colors hover:bg-muted"
            >
              <p className="text-xs text-muted-foreground">
                {row.problem_title} · {row.post.author_name} (@{row.post.author_username})
              </p>
              <p className="mt-1 line-clamp-2 whitespace-pre-wrap break-words font-medium">{row.post.body}</p>
              <p className="mt-2 text-xs text-muted-foreground">
                {row.reply_count === 1 ? "1 reply" : `${row.reply_count} replies`}
              </p>
            </Link>
          </li>
        ))}
      </ul>

      {data && (page > 1 || data.length === 20) && (
        <nav aria-label="Pages" className="flex items-center justify-between">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            Newer
          </Button>
          <p className="text-sm text-muted-foreground">Page {page}</p>
          <Button variant="outline" size="sm" disabled={data.length < 20} onClick={() => setPage((p) => p + 1)}>
            Older
          </Button>
        </nav>
      )}
    </div>
  );
}
