"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { meKey } from "@/features/auth/hooks";
import type { User } from "@/features/auth/types";
import { api } from "@/lib/api";

const MAX_BYTES = 512 * 1024;

function readCookie(name: string): string {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : "";
}

export function AvatarEditor({ user }: { user: User }) {
  const qc = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const name = user.profile.display_name;
  const initials = name
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  async function upload(file: File) {
    setError(null);
    if (file.size > MAX_BYTES) {
      setError("Please choose an image under 512 KB.");
      return;
    }
    setBusy(true);
    try {
      const body = new FormData();
      body.append("file", file);
      // Multipart upload, so this uses fetch directly. The CSRF header is still required.
      const res = await fetch("/api/v1/users/me/avatar", {
        method: "POST",
        body,
        headers: { "X-CSRF-Token": readCookie("cc_csrf") },
        credentials: "same-origin",
      });
      const json = await res.json().catch(() => null);
      if (!res.ok || !json?.success) {
        throw new Error(json?.error?.message ?? "Upload failed. Please try again.");
      }
      qc.setQueryData(meKey, json.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed. Please try again.");
    } finally {
      setBusy(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  async function remove() {
    setError(null);
    setBusy(true);
    try {
      const res = await api<User>("/users/me/avatar", { method: "DELETE" });
      qc.setQueryData(meKey, res.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't remove the photo.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
      {user.profile.avatar_url ? (
        <>
          {/* eslint-disable-next-line @next/next/no-img-element -- user photo served by our API, not optimised by Next */}
          <img
            src={user.profile.avatar_url}
            alt={`${name}'s profile photo`}
            width={96}
            height={96}
            className="h-24 w-24 rounded-full border border-border object-cover"
          />
        </>
      ) : (
        <div
          aria-label={`${name}'s initials`}
          className="flex h-24 w-24 items-center justify-center rounded-full bg-primary/10 text-2xl font-semibold text-primary"
        >
          {initials || "?"}
        </div>
      )}

      <div className="space-y-2">
        <p className="text-sm text-muted-foreground">PNG, JPEG or WebP, up to 512 KB.</p>
        <div className="flex flex-wrap gap-2">
          <input
            ref={inputRef}
            id="avatar-file"
            type="file"
            accept="image/png,image/jpeg,image/webp"
            className="sr-only"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) void upload(file);
            }}
          />
          <Button variant="outline" size="sm" loading={busy} onClick={() => inputRef.current?.click()}>
            {user.profile.avatar_url ? "Change photo" : "Upload photo"}
          </Button>
          {user.profile.avatar_url && (
            <Button variant="ghost" size="sm" disabled={busy} onClick={remove}>
              Remove
            </Button>
          )}
        </div>
        {error && (
          <p role="alert" className="text-sm text-danger">
            {error}
          </p>
        )}
      </div>
    </div>
  );
}
