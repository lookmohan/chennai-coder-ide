"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/input";
import {
  useCreatePost,
  useDeletePost,
  useReportPost,
  useThreads,
  type Post,
} from "@/features/community/hooks";
import { ApiError } from "@/lib/api";

const PAGE_RULES =
  "Keep it kind and on topic. Ask about an idea, not the full answer. Don't post complete solutions, and never share someone else's personal details.";

function PostBody({ post }: { post: Post }) {
  if (post.is_removed) {
    return <p className="text-sm italic text-muted-foreground">This post was removed.</p>;
  }
  // Plain text only, so nothing a student writes can run as markup.
  return <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">{post.body}</p>;
}

function PostActions({ slug, post, onError }: { slug: string; post: Post; onError: (m: string) => void }) {
  const del = useDeletePost(slug);
  const report = useReportPost(slug);
  const [reporting, setReporting] = useState(false);
  const [reason, setReason] = useState("");

  function fail(err: unknown, fallback: string) {
    onError(err instanceof ApiError ? err.message : fallback);
  }

  if (post.is_removed) return null;

  return (
    <div className="flex flex-wrap items-center gap-3 text-xs">
      {post.can_delete && (
        <button
          type="button"
          className="text-danger hover:underline"
          onClick={() => del.mutate(post.id, { onError: (e) => fail(e, "Couldn't delete the post.") })}
        >
          Delete
        </button>
      )}
      {post.can_report && !reporting && (
        <button type="button" className="text-muted-foreground hover:underline" onClick={() => setReporting(true)}>
          Report
        </button>
      )}
      {reporting && (
        <form
          className="flex w-full flex-wrap items-center gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            report.mutate(
              { id: post.id, reason },
              {
                onSuccess: () => {
                  setReporting(false);
                  setReason("");
                  onError("Thanks. A moderator will look at it.");
                },
                onError: (e2) => fail(e2, "Couldn't send the report."),
              },
            );
          }}
        >
          <input
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Why are you reporting this?"
            className="h-9 flex-1 rounded border border-border bg-background px-2"
            aria-label="Reason for reporting"
            minLength={3}
            maxLength={300}
            required
          />
          <Button type="submit" size="sm" variant="outline" loading={report.isPending}>
            Send report
          </Button>
          <Button type="button" size="sm" variant="ghost" onClick={() => setReporting(false)}>
            Cancel
          </Button>
        </form>
      )}
    </div>
  );
}

function ReplyBox({ slug, parentId, onDone }: { slug: string; parentId: string; onDone: () => void }) {
  const [body, setBody] = useState("");
  const [error, setError] = useState<string | null>(null);
  const create = useCreatePost(slug);

  return (
    <form
      className="mt-3 space-y-2 border-l-2 border-border pl-3"
      onSubmit={(e) => {
        e.preventDefault();
        setError(null);
        create.mutate(
          { body, parent_id: parentId },
          {
            onSuccess: () => {
              setBody("");
              onDone();
            },
            onError: (err) => setError(err instanceof ApiError ? err.message : "Couldn't post your reply."),
          },
        );
      }}
    >
      <Textarea label="Your reply" rows={2} maxLength={2000} value={body} onChange={(e) => setBody(e.target.value)} />
      {error && <p role="alert" className="text-sm text-danger">{error}</p>}
      <div className="flex gap-2">
        <Button type="submit" size="sm" loading={create.isPending} disabled={!body.trim()}>
          Reply
        </Button>
        <Button type="button" size="sm" variant="ghost" onClick={onDone}>
          Cancel
        </Button>
      </div>
    </form>
  );
}

export function Discussion({ slug }: { slug: string }) {
  const [page, setPage] = useState(1);
  const threads = useThreads(slug, page);
  const create = useCreatePost(slug);
  const [question, setQuestion] = useState("");
  const [replyTo, setReplyTo] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function postQuestion(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    create.mutate(
      { body: question, parent_id: null },
      {
        onSuccess: () => setQuestion(""),
        onError: (err) => setError(err instanceof ApiError ? err.message : "Couldn't post your question."),
      },
    );
  }

  return (
    <div className="space-y-6">
      <p className="rounded border border-border bg-muted/50 p-3 text-sm text-muted-foreground">{PAGE_RULES}</p>

      <form onSubmit={postQuestion} className="space-y-2">
        <Textarea
          label="Ask a question or share an idea"
          rows={3}
          maxLength={2000}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        {error && <p role="alert" className="text-sm text-danger">{error}</p>}
        <Button type="submit" loading={create.isPending} disabled={!question.trim()}>
          Post
        </Button>
      </form>

      {notice && (
        <p role="status" className="text-sm text-muted-foreground">
          {notice}
        </p>
      )}

      {threads.isPending && <p className="text-sm text-muted-foreground">Loading the discussion…</p>}
      {threads.isError && <p role="alert" className="text-sm text-danger">{threads.error.message}</p>}

      {threads.data && threads.data.length === 0 && (
        <p className="text-sm text-muted-foreground">No questions yet. Be the first to ask one.</p>
      )}

      <ul className="space-y-5">
        {threads.data?.map(({ post, replies }) => (
          <li key={post.id} className="space-y-3 rounded-lg border border-border p-4">
            <p className="text-xs text-muted-foreground">
              {post.author_name} (@{post.author_username})
            </p>
            <PostBody post={post} />
            <PostActions slug={slug} post={post} onError={setNotice} />

            {replies.map((reply) => (
              <div key={reply.id} className="ml-4 border-l-2 border-border pl-3">
                <p className="text-xs text-muted-foreground">
                  {reply.author_name} (@{reply.author_username})
                </p>
                <PostBody post={reply} />
                <PostActions slug={slug} post={reply} onError={setNotice} />
              </div>
            ))}

            {replyTo === post.id ? (
              <ReplyBox slug={slug} parentId={post.id} onDone={() => setReplyTo(null)} />
            ) : (
              !post.is_removed && (
                <button type="button" className="text-sm text-primary hover:underline" onClick={() => setReplyTo(post.id)}>
                  Reply
                </button>
              )
            )}
          </li>
        ))}
      </ul>

      {threads.data && (threads.data.length === 20 || page > 1) && (
        <nav aria-label="Pages" className="flex items-center justify-between">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            Newer
          </Button>
          <p className="text-sm text-muted-foreground">Page {page}</p>
          <Button variant="outline" size="sm" disabled={threads.data.length < 20} onClick={() => setPage((p) => p + 1)}>
            Older
          </Button>
        </nav>
      )}
    </div>
  );
}
