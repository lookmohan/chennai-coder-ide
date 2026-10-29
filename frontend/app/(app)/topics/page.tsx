"use client";

import Link from "next/link";

import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/ui/error-state";
import { useTopics, LEVELS, type TopicSummary } from "@/features/topics/hooks";
import { cn } from "@/lib/utils";

function LevelBar({ level, ready, target }: { level: string; ready: number; target: number }) {
  const pct = Math.min(100, Math.round((ready / target) * 100));
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{level}</span>
        <span>
          {ready} of {target} ready
        </span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded bg-muted" role="progressbar" aria-label={`${level} progress`} aria-valuemin={0} aria-valuemax={target} aria-valuenow={ready}>
        <div className={cn("h-full rounded", ready === 0 ? "bg-transparent" : "bg-primary")} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function TopicCard({ topic }: { topic: TopicSummary }) {
  const total = LEVELS.reduce((sum, level) => sum + topic.counts[level], 0);
  return (
    <Link
      href={`/topics/${topic.slug}`}
      className="block space-y-4 rounded-lg border border-border bg-card p-5 transition-colors hover:bg-muted"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs text-muted-foreground">Concept {topic.number}</p>
          <h2 className="text-lg font-semibold">{topic.name}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{topic.description}</p>
        </div>
        <span className="shrink-0 rounded bg-muted px-2 py-1 text-xs text-muted-foreground">
          {total === 0 ? "Coming soon" : `${total} ready`}
        </span>
      </div>
      <div className="space-y-3">
        {LEVELS.map((level) => (
          <LevelBar key={level} level={level} ready={topic.counts[level]} target={topic.targets[level]} />
        ))}
      </div>
    </Link>
  );
}

export default function TopicsPage() {
  const topics = useTopics();

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Practice</h1>
        <p className="text-muted-foreground">
          Pick a Python concept and work through it from Easy to Hard. Each concept has 20 Easy, 15 Medium and 10 Hard questions.
        </p>
      </header>

      {topics.isPending && (
        <div className="grid gap-4 md:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-56 w-full" />
          ))}
        </div>
      )}
      {topics.isError && (
        <ErrorState title="Couldn't load the topics" message={topics.error.message} onRetry={() => topics.refetch()} />
      )}

      {topics.data && (
        <div className="grid gap-4 md:grid-cols-2">
          {topics.data.map((topic) => (
            <TopicCard key={topic.slug} topic={topic} />
          ))}
        </div>
      )}
    </div>
  );
}
