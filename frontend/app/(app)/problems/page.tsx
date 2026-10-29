"use client";

import { CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

import { DifficultyBadge } from "@/components/coding/difficulty-badge";
import { Button, buttonClasses } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useProblems } from "@/features/problems/hooks";
import { difficultyStage } from "@/features/problems/status";
import { DIFFICULTIES, type Difficulty, type ProblemListItem } from "@/features/problems/types";
import { useSolved, type SolvedMap } from "@/features/progress/solved";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 20;

function ProblemRow({ problem, solved }: { problem: ProblemListItem; solved: boolean }) {
  return (
    <Link
      href={`/problems/${problem.slug}`}
      className="flex items-center gap-4 rounded-lg border border-border bg-card p-4 transition-colors hover:bg-muted"
    >
      <span className="w-10 shrink-0 text-center text-sm font-semibold text-muted-foreground">
        {problem.number}
      </span>
      <div className="min-w-0 flex-1">
        <p className="truncate font-medium">{problem.title}</p>
        <p className="mt-0.5 text-xs text-muted-foreground">
          {difficultyStage(problem.difficulty)} · {problem.tags.join(", ") || "General"}
        </p>
      </div>
      {solved && (
        <span className="flex items-center gap-1 text-xs font-medium text-success" aria-label="Solved in this browser">
          <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
          <span className="hidden sm:inline">Solved</span>
        </span>
      )}
      <DifficultyBadge difficulty={problem.difficulty} />
    </Link>
  );
}

export default function ProblemsPage() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [difficulty, setDifficulty] = useState<Difficulty | "">("");
  const solved: SolvedMap = useSolved();

  const { data, isPending, isError, error, refetch, isPlaceholderData } = useProblems({ page, q, difficulty });

  const filtersActive = q.trim() !== "" || difficulty !== "";
  const total = data?.meta.total ?? 0;
  const lastPage = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const solvedCount = data ? data.items.filter((p) => solved[p.slug]).length : 0;

  function clearFilters() {
    setQ("");
    setDifficulty("");
    setPage(1);
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Practice</h1>
        <p className="mt-1 text-muted-foreground">
          Start with Problem 1. Each problem builds on the one before it, so there is no rush.
        </p>
      </header>

      {!filtersActive && (
        <Card className="border-primary/30 bg-primary/5 p-4">
          <p className="font-medium">New here? Begin with Problem 1.</p>
          <p className="mt-1 text-sm text-muted-foreground">
            The first problems are short. Getting one right is a real win, and every wrong answer shows you what to
            look at next.
          </p>
          {data && solvedCount > 0 && (
            <p className="mt-2 text-sm text-success">You&apos;ve solved {solvedCount} on this page. Keep going!</p>
          )}
        </Card>
      )}

      <div className="flex flex-col gap-3 md:flex-row md:items-end">
        <div className="md:max-w-xs md:flex-1">
          <Input
            label="Search by title"
            type="search"
            value={q}
            placeholder="e.g. palindrome"
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <div role="group" aria-label="Filter by level" className="flex flex-wrap gap-2">
          {(["", ...DIFFICULTIES] as const).map((level) => (
            <button
              key={level || "all"}
              type="button"
              aria-pressed={difficulty === level}
              onClick={() => {
                setDifficulty(level);
                setPage(1);
              }}
              className={cn(
                "h-11 rounded border px-4 text-sm font-medium transition-colors",
                difficulty === level ? "border-primary bg-primary/10 text-primary" : "border-border hover:bg-muted",
              )}
            >
              {level || "All levels"}
            </button>
          ))}
        </div>
      </div>

      {isPending && (
        <div className="space-y-3" aria-busy="true" aria-label="Loading problems">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      )}

      {isError && (
        <ErrorState
          title="Couldn't load problems"
          message={error instanceof Error ? error.message : "Please try again."}
          onRetry={() => refetch()}
        />
      )}

      {data && data.items.length === 0 && (
        <EmptyState
          title={filtersActive ? "No problems match those filters." : "Problems are coming soon."}
          description={
            filtersActive
              ? "Try a different search or level."
              : "The first problems haven't been published yet. Check back soon."
          }
          action={
            filtersActive ? (
              <Button variant="outline" size="sm" onClick={clearFilters}>
                Clear filters
              </Button>
            ) : undefined
          }
        />
      )}

      {data && data.items.length > 0 && (
        <>
          <div className={cn("space-y-3", isPlaceholderData && "opacity-60")} aria-busy={isPlaceholderData}>
            {data.items.map((problem) => (
              <ProblemRow key={problem.slug} problem={problem} solved={Boolean(solved[problem.slug])} />
            ))}
          </div>

          <nav aria-label="Pages" className="flex items-center justify-between gap-3 pt-2">
            <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Previous
            </Button>
            <p className="text-sm text-muted-foreground">
              Page {page} of {lastPage}
            </p>
            <Button variant="outline" size="sm" disabled={page >= lastPage} onClick={() => setPage((p) => p + 1)}>
              Next
            </Button>
          </nav>
        </>
      )}

      <p className="text-center text-sm text-muted-foreground">
        <Link href="/dashboard" className={buttonClasses({ variant: "ghost", size: "sm" })}>
          Back to dashboard
        </Link>
      </p>
    </div>
  );
}
