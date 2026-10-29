"use client";

import { useEffect, useState } from "react";

import { useMe } from "@/features/auth/hooks";

// Solved problems are saved per account (keyed by user id), so one browser can hold several accounts
// without mixing their progress. This is practice progress, not an official record.
const KEY_PREFIX = "cc-solved-problems";
const CHANGE_EVENT = "cc-solved-change";

/** Map of problem slug -> ISO date when it was first solved. */
export type SolvedMap = Record<string, string>;

const keyFor = (userId: string) => `${KEY_PREFIX}:${userId}`;

export function readSolved(userId: string): SolvedMap {
  try {
    const raw = window.localStorage.getItem(keyFor(userId));
    if (!raw) return {};
    const parsed: unknown = JSON.parse(raw);
    return typeof parsed === "object" && parsed !== null && !Array.isArray(parsed) ? (parsed as SolvedMap) : {};
  } catch {
    // Corrupt or blocked storage should never break the page.
    return {};
  }
}

/** Returns true if this is the first time this account solved the problem. */
export function markSolved(userId: string, slug: string): boolean {
  const current = readSolved(userId);
  if (current[slug]) return false;
  current[slug] = new Date().toISOString();
  try {
    window.localStorage.setItem(keyFor(userId), JSON.stringify(current));
    window.dispatchEvent(new Event(CHANGE_EVENT));
  } catch {
    /* storage full or disabled: the mark simply isn't kept */
    return false;
  }
  return true;
}

/** Solved problems for the signed-in account. Updates live when a problem is solved. */
export function useSolved(): SolvedMap {
  const { data: me } = useMe();
  const userId = me?.id;
  const [solved, setSolved] = useState<SolvedMap>({});

  useEffect(() => {
    if (!userId) {
      setSolved({});
      return;
    }
    const refresh = () => setSolved(readSolved(userId));
    refresh();
    window.addEventListener(CHANGE_EVENT, refresh);
    window.addEventListener("storage", refresh);
    return () => {
      window.removeEventListener(CHANGE_EVENT, refresh);
      window.removeEventListener("storage", refresh);
    };
  }, [userId]);

  return solved;
}
