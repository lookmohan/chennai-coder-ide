"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { ApiError, api } from "@/lib/api";
import type { Difficulty, PageMeta, ProblemDetail, ProblemListItem } from "./types";

export function useProblems(params: { page: number; q: string; difficulty: Difficulty | "" }) {
  return useQuery({
    queryKey: ["problems", params],
    queryFn: async () => {
      const search = new URLSearchParams({ page: String(params.page), page_size: "20" });
      if (params.q.trim()) search.set("q", params.q.trim());
      if (params.difficulty) search.set("difficulty", params.difficulty);
      const res = await api<ProblemListItem[]>(`/problems?${search.toString()}`);
      return { items: res.data, meta: res.meta as PageMeta };
    },
    placeholderData: keepPreviousData,
  });
}

export function useProblem(slug: string) {
  return useQuery({
    queryKey: ["problem", slug],
    queryFn: async () => (await api<ProblemDetail>(`/problems/${encodeURIComponent(slug)}`)).data,
    // A missing problem will not appear on retry, so don't retry 404s.
    retry: (count, error) => !(error instanceof ApiError && error.status === 404) && count < 2,
  });
}
