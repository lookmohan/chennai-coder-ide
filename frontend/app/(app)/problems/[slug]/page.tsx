"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState, type CSSProperties, type KeyboardEvent as ReactKeyboardEvent, type PointerEvent as ReactPointerEvent } from "react";

import { BrowserTestPanel } from "@/components/coding/browser-test-panel";
import { CodeEditor } from "@/components/coding/code-editor";
import { DifficultyBadge } from "@/components/coding/difficulty-badge";
import { Button, buttonClasses } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useMe } from "@/features/auth/hooks";
import { useProblem } from "@/features/problems/hooks";
import { difficultyStage } from "@/features/problems/status";
import { markSolved, useSolved } from "@/features/progress/solved";
import { ApiError } from "@/lib/api";
import { cn } from "@/lib/utils";

// Practice is Python-only for now.
const LANGUAGE = "python";

type ViewMode = "split" | "question" | "code";

const SPLIT_MIN = 30;
const SPLIT_MAX = 70;
const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

// Drafts are kept per account, in this browser only.
const draftKey = (userId: string, slug: string) => `cc-draft:${userId}:${slug}:${LANGUAGE}`;

function loadDraft(userId: string, slug: string): string | null {
  try {
    return window.localStorage.getItem(draftKey(userId, slug));
  } catch {
    return null;
  }
}

function saveDraft(userId: string, slug: string, value: string) {
  try {
    window.localStorage.setItem(draftKey(userId, slug), value);
  } catch {
    /* storage can be full or disabled; the code still works in the editor */
  }
}

function clearDraft(userId: string, slug: string) {
  try {
    window.localStorage.removeItem(draftKey(userId, slug));
  } catch {
    /* ignore */
  }
}

const VIEW_OPTIONS: { mode: ViewMode; label: string }[] = [
  { mode: "split", label: "Split view" },
  { mode: "question", label: "Question only" },
  { mode: "code", label: "Code only" },
];

export default function ProblemPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: me } = useMe();
  const userId = me?.id ?? "";
  const problemQuery = useProblem(slug);
  const problem = problemQuery.data;
  const solved = useSolved();

  const [code, setCode] = useState("");
  const [mode, setMode] = useState<ViewMode>("split");
  const [leftPct, setLeftPct] = useState(46);
  const containerRef = useRef<HTMLDivElement>(null);

  // Load this account's draft, or the starter code, when the problem or account is known.
  const loadedSlug = problem?.slug;
  useEffect(() => {
    if (!userId) return;
    const starter = problem?.starter_code[LANGUAGE] ?? "";
    setCode(loadDraft(userId, slug) ?? starter);
    // Only reload when a different problem or account is opened, not on every refetch.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug, loadedSlug, userId]);

  if (!problem) {
    if (problemQuery.isError) {
      const notFound = problemQuery.error instanceof ApiError && problemQuery.error.status === 404;
      return (
        <div className="space-y-4">
          <ErrorState
            title={notFound ? "Problem not found" : "Couldn't load this problem"}
            message={
              notFound
                ? "It may have been moved or isn't published yet. Pick another problem to keep going."
                : problemQuery.error.message
            }
            onRetry={notFound ? undefined : () => problemQuery.refetch()}
          />
          <p className="text-center">
            <Link href="/problems" className={buttonClasses({ variant: "outline" })}>
              Back to practice
            </Link>
          </p>
        </div>
      );
    }
    return (
      <div className="space-y-4" aria-busy="true" aria-label="Loading problem">
        <Skeleton className="h-6 w-40" />
        <Skeleton className="h-10 w-2/3" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  const isSolved = Boolean(solved[problem.slug]);

  function handleChange(value: string) {
    setCode(value);
    if (userId) saveDraft(userId, slug, value);
  }

  function handleReset() {
    if (userId) clearDraft(userId, slug);
    setCode(problem?.starter_code[LANGUAGE] ?? "");
  }

  // Drag the divider to change how much room the question and the editor get.
  function startDrag(event: ReactPointerEvent<HTMLDivElement>) {
    event.preventDefault();
    const move = (e: PointerEvent) => {
      const rect = containerRef.current?.getBoundingClientRect();
      if (!rect || rect.width === 0) return;
      setLeftPct(clamp(((e.clientX - rect.left) / rect.width) * 100, SPLIT_MIN, SPLIT_MAX));
    };
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  }

  function handleDividerKeys(event: ReactKeyboardEvent<HTMLDivElement>) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      setLeftPct((p) => clamp(p - 2, SPLIT_MIN, SPLIT_MAX));
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      setLeftPct((p) => clamp(p + 2, SPLIT_MIN, SPLIT_MAX));
    }
  }

  const showQuestion = mode !== "code";
  const showEditor = mode !== "question";
  const editorHeight = mode === "code" ? "h-[600px] lg:h-[calc(100dvh-12rem)]" : "h-[440px] lg:h-[calc(100dvh-16rem)]";

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <nav aria-label="Breadcrumb" className="text-sm text-muted-foreground">
          <Link href="/problems" className="hover:text-foreground">
            Practice
          </Link>
          <span aria-hidden="true"> / </span>
          <span>Problem {problem.number}</span>
        </nav>

        <div role="group" aria-label="Layout" className="flex flex-wrap gap-2">
          {VIEW_OPTIONS.map((option) => (
            <Button
              key={option.mode}
              variant={mode === option.mode ? "primary" : "outline"}
              size="sm"
              aria-pressed={mode === option.mode}
              onClick={() => setMode(option.mode)}
            >
              {option.label}
            </Button>
          ))}
        </div>
      </div>

      <header className="space-y-2">
        <div className="flex flex-wrap items-center gap-2">
          <DifficultyBadge difficulty={problem.difficulty} />
          <span className="text-sm text-muted-foreground">{difficultyStage(problem.difficulty)}</span>
          {isSolved && (
            <span className="rounded bg-success/10 px-2 py-0.5 text-xs font-medium text-success">
              ✓ Solved in this browser
            </span>
          )}
        </div>
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">{problem.title}</h1>
      </header>

      <div
        ref={containerRef}
        className={cn(
          "grid grid-cols-1 gap-8",
          mode === "split" && "lg:gap-0 lg:grid-cols-[var(--split-left)_10px_minmax(0,1fr)]",
          mode !== "split" && "lg:grid-cols-[minmax(0,1fr)]",
        )}
        style={{ "--split-left": `${leftPct}%` } as CSSProperties}
      >
        {/* Question */}
        {showQuestion && (
          <section
            aria-labelledby="statement-heading"
            className={cn("min-w-0 space-y-6", mode === "question" && "mx-auto w-full max-w-4xl")}
          >
            <h2 id="statement-heading" className="sr-only">
              Problem statement
            </h2>

            <div className="space-y-3">
              <p className="whitespace-pre-line text-base leading-relaxed">{problem.description}</p>
            </div>

            {problem.input_format && (
              <div>
                <h3 className="font-semibold">Input format</h3>
                <p className="mt-1 whitespace-pre-line text-sm leading-relaxed">{problem.input_format}</p>
              </div>
            )}
            {problem.output_format && (
              <div>
                <h3 className="font-semibold">Output format</h3>
                <p className="mt-1 whitespace-pre-line text-sm leading-relaxed">{problem.output_format}</p>
              </div>
            )}
            {problem.constraints && (
              <div>
                <h3 className="font-semibold">Constraints</h3>
                <p className="mt-1 whitespace-pre-line font-mono text-sm">{problem.constraints}</p>
              </div>
            )}

            {problem.examples.map((example, index) => (
              <div key={index} className="space-y-2 rounded-lg border border-border p-4">
                <h3 className="font-semibold">Example {index + 1}</h3>
                <div className="grid gap-3 sm:grid-cols-2">
                  <div>
                    <p className="mb-1 text-xs uppercase tracking-wide text-muted-foreground">Input</p>
                    <pre className="overflow-x-auto rounded bg-muted p-3 font-mono text-sm">{example.input || " "}</pre>
                  </div>
                  <div>
                    <p className="mb-1 text-xs uppercase tracking-wide text-muted-foreground">Output</p>
                    <pre className="overflow-x-auto rounded bg-muted p-3 font-mono text-sm">{example.output}</pre>
                  </div>
                </div>
                {example.explanation && (
                  <div>
                    <p className="mb-1 text-xs uppercase tracking-wide text-muted-foreground">Explanation</p>
                    <p className="whitespace-pre-line text-sm leading-relaxed">{example.explanation}</p>
                  </div>
                )}
              </div>
            ))}

            {problem.explanation && (
              <details className="rounded border border-border p-4">
                <summary className="cursor-pointer font-medium">Stuck? Open a hint</summary>
                <p className="mt-3 text-sm text-muted-foreground">{problem.explanation}</p>
              </details>
            )}
          </section>
        )}

        {/* Divider between the question and the editor (split view on wide screens only) */}
        {mode === "split" && (
          <div
            role="separator"
            aria-orientation="vertical"
            aria-label="Resize the question and the editor. Use the left and right arrow keys."
            aria-valuemin={SPLIT_MIN}
            aria-valuemax={SPLIT_MAX}
            aria-valuenow={Math.round(leftPct)}
            tabIndex={0}
            onPointerDown={startDrag}
            onKeyDown={handleDividerKeys}
            className="hidden cursor-col-resize items-stretch justify-center rounded hover:bg-muted lg:flex"
          >
            <span className="w-1 rounded-full bg-border" aria-hidden="true" />
          </div>
        )}

        {/* Editor and checks */}
        {showEditor && (
          <section aria-labelledby="solve-heading" className="min-w-0 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 id="solve-heading" className="font-semibold">
                Your Python solution
              </h2>
              <Button variant="outline" size="sm" onClick={handleReset}>
                Reset to starter code
              </Button>
            </div>

            <div className={cn("lg:sticky lg:top-4", editorHeight)}>
              <CodeEditor
                language={LANGUAGE}
                value={code}
                onChange={handleChange}
                label="Your Python solution"
                className="h-full"
              />
            </div>

            <BrowserTestPanel
              code={code}
              examples={problem.examples}
              timeLimitMs={problem.time_limit_ms}
              onAllPassed={() => {
                if (userId) markSolved(userId, problem.slug);
              }}
            />
          </section>
        )}
      </div>
    </div>
  );
}
