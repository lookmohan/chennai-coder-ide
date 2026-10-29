"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";

import { DifficultyBadge } from "@/components/coding/difficulty-badge";
import { buttonClasses } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { LEVELS, useTopic, type Level } from "@/features/topics/hooks";
import { cn } from "@/lib/utils";
import { ApiError } from "@/lib/api";

export default function TopicPage() {
  const { slug } = useParams<{ slug: string }>();
  const topic = useTopic(slug);
  const [level, setLevel] = useState<Level>("Easy");

  if (topic.isPending) {
    return <Skeleton className="h-96 w-full" />;
  }

  if (topic.isError) {
    const notFound = topic.error instanceof ApiError && topic.error.status === 404;
    return (
      <div className="space-y-4">
        <ErrorState
          title={notFound ? "Topic not found" : "Couldn't load this topic"}
          message={topic.error.message}
          onRetry={notFound ? undefined : () => topic.refetch()}
        />
        <p className="text-center">
          <Link href="/topics" className={buttonClasses({ variant: "outline" })}>
            Back to practice
          </Link>
        </p>
      </div>
    );
  }

  const data = topic.data;
  const problems = data.problems[level];
  const ready = data.counts[level];
  const target = data.targets[level];

  return (
    <div className="space-y-6">
      <nav aria-label="Breadcrumb" className="text-sm text-muted-foreground">
        <Link href="/topics" className="hover:text-foreground">
          Practice
        </Link>
        <span aria-hidden="true"> / </span>
        <span>{data.name}</span>
      </nav>

      <header className="space-y-1">
        <p className="text-xs text-muted-foreground">Concept {data.number}</p>
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">{data.name}</h1>
        <p className="text-muted-foreground">{data.description}</p>
      </header>

      <div role="tablist" aria-label="Difficulty" className="flex flex-wrap gap-2 border-b border-border pb-3">
        {LEVELS.map((value) => (
          <button
            key={value}
            type="button"
            role="tab"
            aria-selected={level === value}
            onClick={() => setLevel(value)}
            className={cn(
              "rounded px-4 py-2 text-sm font-medium",
              level === value ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-muted",
            )}
          >
            {value} <span className="ml-1 text-xs opacity-80">{data.counts[value]}/{data.targets[value]}</span>
          </button>
        ))}
      </div>

      <p className="text-sm text-muted-foreground">
        {ready} of {target} {level} questions are ready.
        {ready < target && " More are being written, so check back soon."}
      </p>

      {problems.length === 0 ? (
        <p className="rounded-lg border border-dashed border-border p-6 text-center text-sm text-muted-foreground">
          {level} questions for this concept are coming soon.
        </p>
      ) : (
        <ul className="space-y-3">
          {problems.map((problem) => (
            <li key={problem.slug}>
              <Link
                href={`/problems/${problem.slug}`}
                className="flex items-center gap-4 rounded-lg border border-border bg-card p-4 transition-colors hover:bg-muted"
              >
                <span className="w-10 shrink-0 text-center text-sm font-semibold text-muted-foreground">
                  {problem.number}
                </span>
                <span className="min-w-0 flex-1 truncate font-medium">{problem.title}</span>
                <DifficultyBadge difficulty={problem.difficulty} />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
