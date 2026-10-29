"use client";

import Link from "next/link";
import { useEffect, useRef, useState, type KeyboardEvent } from "react";

import { PresenceBadge } from "@/components/chat/presence-badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useDeleteFromRoom, usePeople, useRoom, useSendToRoom, type Person } from "@/features/chat/hooks";
import { useLatestThreads } from "@/features/community/latest";
import { ApiError } from "@/lib/api";
import { cn } from "@/lib/utils";

function timeLabel(iso: string) {
  return new Date(iso).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

function PersonRow({ person }: { person: Person }) {
  return (
    <li className="flex items-center gap-3 rounded-lg border border-border bg-card p-3">
      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary">
        {person.display_name.slice(0, 1).toUpperCase()}
      </span>
      <span className="min-w-0 flex-1">
        <span className="block truncate text-sm font-medium">{person.display_name}</span>
        <span className="block truncate text-xs text-muted-foreground">@{person.username}</span>
        <PresenceBadge presence={person.presence} className="mt-0.5" />
      </span>
    </li>
  );
}

function RoomChat() {
  const room = useRoom();
  const send = useSendToRoom();
  const remove = useDeleteFromRoom();
  const [draft, setDraft] = useState("");
  const [error, setError] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const count = room.data?.length ?? 0;
  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" });
  }, [count]);

  function submit() {
    const body = draft.trim();
    if (!body || send.isPending) return;
    setError(null);
    send.mutate(body, {
      onSuccess: () => setDraft(""),
      onError: (err) => setError(err instanceof ApiError ? err.message : "Couldn't send your message. Try again."),
    });
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  }

  return (
    <section aria-labelledby="room-heading" className="flex min-w-0 flex-col gap-3">
      <div className="flex items-center justify-between">
        <h2 id="room-heading" className="font-semibold">Community room</h2>
        <p className="text-xs text-muted-foreground">Everyone signed in can read and post here.</p>
      </div>

      <div className="flex h-[55vh] min-h-[320px] flex-col gap-3 overflow-y-auto rounded-lg border border-border bg-card p-4">
        {room.isPending && <Skeleton className="h-40 w-full" />}
        {room.isError && <p role="alert" className="text-sm text-danger">{room.error.message}</p>}
        {room.data && room.data.length === 0 && (
          <p className="m-auto text-sm text-muted-foreground">No messages yet. Say hello to the room.</p>
        )}
        {room.data?.map((message) => (
          <div key={message.id} className={cn("flex flex-col", message.mine ? "items-end" : "items-start")}>
            <p className="mb-0.5 text-xs text-muted-foreground">
              {message.mine ? "You" : `${message.author_name} (@${message.author_username})`} · {timeLabel(message.created_at)}
            </p>
            <div
              className={cn(
                "max-w-[85%] rounded-2xl px-3 py-2 text-sm",
                message.mine ? "rounded-br-sm bg-primary text-primary-foreground" : "rounded-bl-sm bg-muted",
              )}
            >
              <p className="whitespace-pre-wrap break-words">{message.body}</p>
            </div>
            {message.can_delete && (
              <button
                type="button"
                className="mt-0.5 text-xs text-muted-foreground hover:text-danger"
                onClick={() => remove.mutate(message.id)}
              >
                Delete
              </button>
            )}
          </div>
        ))}
        <div ref={endRef} />
      </div>

      <form
        className="space-y-2"
        onSubmit={(e) => {
          e.preventDefault();
          submit();
        }}
      >
        <div className="flex items-end gap-2">
          <textarea
            aria-label="Message the community room"
            rows={2}
            maxLength={500}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Write a message. Enter to send, Shift+Enter for a new line."
            className="min-h-[44px] flex-1 resize-y rounded border border-border bg-background px-3 py-2 text-sm"
          />
          <Button type="submit" loading={send.isPending} disabled={!draft.trim()}>
            Send
          </Button>
        </div>
        {error && <p role="alert" className="text-sm text-danger">{error}</p>}
      </form>
    </section>
  );
}

function PeoplePanel() {
  const [q, setQ] = useState("");
  const people = usePeople(q);
  return (
    <aside aria-labelledby="people-heading" className="space-y-3">
      <h2 id="people-heading" className="font-semibold">People</h2>
      <Input label="Search people" type="search" value={q} onChange={(e) => setQ(e.target.value)} />
      {people.isPending && <Skeleton className="h-40 w-full" />}
      {people.data && people.data.length === 0 && (
        <Card className="p-4 text-sm text-muted-foreground">No one matches that search yet.</Card>
      )}
      <ul className="space-y-2">
        {people.data?.map((person) => (
          <PersonRow key={person.username} person={person} />
        ))}
      </ul>
    </aside>
  );
}

export default function CommunityPage() {
  const questions = useLatestThreads(1);
  const [tab, setTab] = useState<"chat" | "questions">("chat");

  return (
    <div className="space-y-6">
      <header className="space-y-3">
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Community</h1>
        <div role="tablist" aria-label="Community sections" className="flex gap-2 border-b border-border pb-3">
          <button
            type="button"
            role="tab"
            aria-selected={tab === "chat"}
            onClick={() => setTab("chat")}
            className={cn("rounded px-3 py-2 text-sm font-medium", tab === "chat" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-muted")}
          >
            Chat
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === "questions"}
            onClick={() => setTab("questions")}
            className={cn("rounded px-3 py-2 text-sm font-medium", tab === "questions" ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-muted")}
          >
            Questions
          </button>
        </div>
      </header>

      {tab === "chat" && (
        <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_280px]">
          <RoomChat />
          <PeoplePanel />
        </div>
      )}

      {tab === "questions" && (
        <div className="space-y-3">
          <p className="text-sm text-muted-foreground">
            The newest questions from every problem.{" "}
            <Link href="/problems" className="text-primary hover:underline">Browse problems</Link> to join a discussion.
          </p>
          {questions.isPending && <Skeleton className="h-40 w-full" />}
          {questions.data && questions.data.length === 0 && (
            <EmptyState title="No questions yet." description="Open a problem and use its Discussion link to ask the first one." />
          )}
          <ul className="space-y-3">
            {questions.data?.map((row) => (
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
        </div>
      )}
    </div>
  );
}
