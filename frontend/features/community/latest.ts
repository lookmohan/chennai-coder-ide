"use client";

import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { Post } from "@/features/community/hooks";

export type LatestThread = {
  post: Post;
  problem_slug: string;
  problem_title: string;
  reply_count: number;
};

export function useLatestThreads(page: number) {
  return useQuery({
    queryKey: ["community", "latest", page],
    queryFn: async () => (await api<LatestThread[]>(`/community/latest?page=${page}`)).data,
  });
}
