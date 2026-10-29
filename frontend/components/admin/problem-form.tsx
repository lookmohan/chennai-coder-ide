"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button, buttonClasses } from "@/components/ui/button";
import { Input, Textarea } from "@/components/ui/input";
import { useSaveProblem, type ProblemFull, type ProblemInput, type TestCase } from "@/features/admin/hooks";
import { ApiError } from "@/lib/api";

type FormState = {
  slug: string;
  title: string;
  description: string;
  difficulty: "Easy" | "Medium" | "Hard";
  status: "draft" | "published" | "archived";
  sort_order: string;
  tags: string;
  input_format: string;
  output_format: string;
  constraints: string;
  explanation: string;
  time_limit_ms: string;
  memory_limit_mb: string;
  starter: string;
  tests: TestCase[];
};

const EMPTY_TEST: TestCase = { stdin: "", expected_output: "", is_hidden: false, explanation: null };

function fromProblem(p: ProblemFull | undefined): FormState {
  return {
    slug: p?.slug ?? "",
    title: p?.title ?? "",
    description: p?.description ?? "",
    difficulty: p?.difficulty ?? "Easy",
    status: p?.status ?? "draft",
    sort_order: String(p?.sort_order ?? 1),
    tags: (p?.tags ?? []).join(", "),
    input_format: p?.input_format ?? "",
    output_format: p?.output_format ?? "",
    constraints: p?.constraints ?? "",
    explanation: p?.explanation ?? "",
    time_limit_ms: String(p?.time_limit_ms ?? 2000),
    memory_limit_mb: String(p?.memory_limit_mb ?? 256),
    starter: p?.starter_code?.python ?? "# Write your solution here\n",
    tests: p?.tests.map((t) => ({ ...t })) ?? [{ ...EMPTY_TEST, is_hidden: false }],
  };
}

const nullIfBlank = (value: string) => (value.trim() ? value : null);

export function ProblemForm({ problem }: { problem?: ProblemFull }) {
  const router = useRouter();
  const save = useSaveProblem(problem?.id);
  const [form, setForm] = useState<FormState>(() => fromProblem(problem));
  const [error, setError] = useState<string | null>(null);

  const set = <K extends keyof FormState>(key: K, value: FormState[K]) => setForm((f) => ({ ...f, [key]: value }));

  function setTest(index: number, patch: Partial<TestCase>) {
    setForm((f) => ({ ...f, tests: f.tests.map((t, i) => (i === index ? { ...t, ...patch } : t)) }));
  }

  function submit() {
    setError(null);
    const payload: ProblemInput = {
      slug: form.slug.trim().toLowerCase(),
      title: form.title.trim(),
      description: form.description,
      difficulty: form.difficulty,
      status: form.status,
      sort_order: Number(form.sort_order) || 0,
      tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
      input_format: nullIfBlank(form.input_format),
      output_format: nullIfBlank(form.output_format),
      constraints: nullIfBlank(form.constraints),
      explanation: nullIfBlank(form.explanation),
      time_limit_ms: Number(form.time_limit_ms) || 2000,
      memory_limit_mb: Number(form.memory_limit_mb) || 256,
      starter_code: { python: form.starter },
      tests: form.tests.map((t) => ({
        stdin: t.stdin,
        expected_output: t.expected_output,
        is_hidden: t.is_hidden,
        explanation: nullIfBlank(t.explanation ?? ""),
      })),
    };

    save.mutate(payload, {
      onSuccess: (saved) => {
        router.replace(`/admin/problems/${saved.id}`);
      },
      onError: (err) => {
        if (err instanceof ApiError && err.details?.length) {
          setError(err.details.map((d) => `${d.field}: ${d.message}`).join(" · "));
        } else {
          setError(err instanceof Error ? err.message : "Couldn't save the problem.");
        }
      },
    });
  }

  return (
    <form
      className="space-y-8"
      onSubmit={(e) => {
        e.preventDefault();
        submit();
      }}
      noValidate
    >
      {error && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {error}
        </p>
      )}
      {save.isSuccess && !error && (
        <p role="status" className="text-sm text-success">
          Saved.
        </p>
      )}

      <section className="grid gap-4 md:grid-cols-2" aria-labelledby="basics">
        <h2 id="basics" className="text-lg font-semibold md:col-span-2">
          Basics
        </h2>
        <Input label="Address (slug)" value={form.slug} onChange={(e) => set("slug", e.target.value)} hint="Lower-case letters, numbers and hyphens, e.g. double-it" />
        <Input label="Title" value={form.title} onChange={(e) => set("title", e.target.value)} />
        <div className="space-y-1.5">
          <label htmlFor="difficulty" className="block text-sm font-medium">Level</label>
          <select id="difficulty" value={form.difficulty} onChange={(e) => set("difficulty", e.target.value as FormState["difficulty"])} className="h-11 w-full rounded border border-border bg-background px-3">
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>
        <Input label="Position on the path" type="number" min={0} value={form.sort_order} onChange={(e) => set("sort_order", e.target.value)} />
        <Input label="Tags (comma separated)" value={form.tags} onChange={(e) => set("tags", e.target.value)} />
        <div className="grid grid-cols-2 gap-4">
          <Input label="Time limit (ms)" type="number" value={form.time_limit_ms} onChange={(e) => set("time_limit_ms", e.target.value)} />
          <Input label="Memory (MB)" type="number" value={form.memory_limit_mb} onChange={(e) => set("memory_limit_mb", e.target.value)} />
        </div>
      </section>

      <section className="space-y-4" aria-labelledby="statement">
        <h2 id="statement" className="text-lg font-semibold">Statement</h2>
        <Textarea label="Story and task" rows={6} value={form.description} onChange={(e) => set("description", e.target.value)} />
        <Textarea label="Input format" rows={3} value={form.input_format} onChange={(e) => set("input_format", e.target.value)} />
        <Textarea label="Output format" rows={3} value={form.output_format} onChange={(e) => set("output_format", e.target.value)} />
        <Textarea label="Constraints" rows={3} value={form.constraints} onChange={(e) => set("constraints", e.target.value)} />
        <Textarea label="Hint (shown when a student opens it)" rows={3} value={form.explanation} onChange={(e) => set("explanation", e.target.value)} />
      </section>

      <section className="space-y-4" aria-labelledby="starter">
        <h2 id="starter" className="text-lg font-semibold">Starter code (Python)</h2>
        <Textarea label="Starter code" rows={4} value={form.starter} onChange={(e) => set("starter", e.target.value)} />
      </section>

      <section className="space-y-4" aria-labelledby="tests">
        <div className="flex items-center justify-between">
          <h2 id="tests" className="text-lg font-semibold">Test cases</h2>
          <Button type="button" variant="outline" size="sm" onClick={() => set("tests", [...form.tests, { ...EMPTY_TEST }])}>
            Add test case
          </Button>
        </div>
        <p className="text-sm text-muted-foreground">
          Visible cases appear as examples for students, with their explanations. Hidden cases are only used for grading and are never shown.
        </p>
        {form.tests.map((test, index) => (
          <fieldset key={index} className="space-y-3 rounded-lg border border-border p-4">
            <legend className="px-1 text-sm font-medium">Test {index + 1}</legend>
            <div className="grid gap-3 md:grid-cols-2">
              <Textarea label="Input (stdin)" rows={3} value={test.stdin} onChange={(e) => setTest(index, { stdin: e.target.value })} />
              <Textarea label="Expected output" rows={3} value={test.expected_output} onChange={(e) => setTest(index, { expected_output: e.target.value })} />
            </div>
            <Textarea
              label="Explanation (visible cases only)"
              rows={2}
              value={test.explanation ?? ""}
              onChange={(e) => setTest(index, { explanation: e.target.value })}
            />
            <div className="flex flex-wrap items-center justify-between gap-3">
              <label className="flex items-center gap-2 text-sm">
                <input type="checkbox" checked={test.is_hidden} onChange={(e) => setTest(index, { is_hidden: e.target.checked })} />
                Hidden (not shown to students)
              </label>
              <Button type="button" variant="ghost" size="sm" disabled={form.tests.length <= 1} onClick={() => set("tests", form.tests.filter((_, i) => i !== index))}>
                Remove
              </Button>
            </div>
          </fieldset>
        ))}
      </section>

      <div className="flex flex-wrap items-center gap-3 border-t border-border pt-6">
        <Button type="submit" loading={save.isPending}>
          {problem ? "Save changes" : "Create problem"}
        </Button>
        <Select status={form.status} onChange={(v) => set("status", v)} />
        <Link href="/admin/problems" className={buttonClasses({ variant: "ghost" })}>
          Back to problems
        </Link>
      </div>
    </form>
  );
}

function Select({ status, onChange }: { status: FormState["status"]; onChange: (v: FormState["status"]) => void }) {
  return (
    <label className="flex items-center gap-2 text-sm">
      Status
      <select value={status} onChange={(e) => onChange(e.target.value as FormState["status"])} className="h-11 rounded border border-border bg-background px-3">
        <option value="draft">Draft (hidden from students)</option>
        <option value="published">Published</option>
        <option value="archived">Archived</option>
      </select>
    </label>
  );
}
