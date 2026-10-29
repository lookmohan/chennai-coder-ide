"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";

export type Post = {
  id: string;
  parent_id: string | null;
  author_username: string;
  author_name: string;
  body: string | null;
  is_removed: boolean;
  created_at: string;
  can_delete: boolean;
  can_report: boolean;
};

export type Thread = { post: Post; replies: Post[] };

export type Report = {
  id: string;
  post_id: string;
  post_body: string | null;
  post_author: string;
  reporter_username: string;
  reason: string;
  status: "open" | "dismissed" | "actioned";
  created_at: string;
};

export function useThreads(slug: string, page: number) {
  return useQuery({
    queryKey: ["discussion", slug, page],
    queryFn: async () => (await api<Thread[]>(`/problems/${encodeURIComponent(slug)}/discussion?page=${page}`)).data,
  });
}

function useInvalidateDiscussion(slug: string) {
  const qc = useQueryClient();
  return () => void qc.invalidateQueries({ queryKey: ["discussion", slug] });
}

export function useCreatePost(slug: string) {
  const refresh = useInvalidateDiscussion(slug);
  return useMutation({
    mutationFn: async (input: { body: string; parent_id: string | null }) =>
      (await api<Post>(`/problems/${encodeURIComponent(slug)}/discussion`, { method: "POST", body: input })).data,
    onSuccess: refresh,
  });
}

export function useDeletePost(slug: string) {
  const refresh = useInvalidateDiscussion(slug);
  return useMutation({
    mutationFn: async (id: string) => (await api<Post>(`/discussion/${id}`, { method: "DELETE" })).data,
    onSuccess: refresh,
  });
}

export function useReportPost(slug: string) {
  const refresh = useInvalidateDiscussion(slug);
  return useMutation({
    mutationFn: async ({ id, reason }: { id: string; reason: string }) =>
      (await api<{ report_id: string; status: string }>(`/discussion/${id}/report`, { method: "POST", body: { reason } })).data,
    onSuccess: refresh,
  });
}

export function useReports(status: Report["status"]) {
  return useQuery({
    queryKey: ["reports", status],
    queryFn: async () => (await api<Report[]>(`/community/reports?status=${status}`)).data,
  });
}

export function useResolveReport() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, action }: { id: string; action: "dismiss" | "remove" }) =>
      (await api<{ report_id: string; status: string }>(`/community/reports/${id}/resolve`, { method: "POST", body: { action } })).data,
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["reports"] }),
  });
}
