"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { ProblemListItem } from "@/features/problems/types";

export type Level = "Easy" | "Medium" | "Hard";
export const LEVELS: Level[] = ["Easy", "Medium", "Hard"];

export type TopicSummary = {
  slug: string;
  name: string;
  description: string;
  number: number;
  counts: Record<Level, number>;
  targets: Record<Level, number>;
};

export type TopicDetail = TopicSummary & {
  problems: Record<Level, ProblemListItem[]>;
};

export function useTopics() {
  return useQuery({
    queryKey: ["topics"],
    queryFn: async () => (await api<TopicSummary[]>("/topics")).data,
    placeholderData: keepPreviousData,
  });
}

export function useTopic(slug: string) {
  return useQuery({
    queryKey: ["topic", slug],
    queryFn: async () => (await api<TopicDetail>(`/topics/${encodeURIComponent(slug)}`)).data,
    retry: (count, error) => count < 2 && !(error instanceof Error && error.message.includes("doesn't exist")),
  });
}
