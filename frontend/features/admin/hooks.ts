"use client";

import { keepPreviousData, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";

export type Overview = {
  students: number;
  active_students_7d: number;
  problems_published: number;
  problems_draft: number;
  problems_archived: number;
};

export type AdminStudent = {
  id: string;
  email: string;
  username: string;
  display_name: string;
  status: string;
  created_at: string;
  last_login_at: string | null;
};

export type ProblemRow = {
  id: string;
  slug: string;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  status: "draft" | "published" | "archived";
  sort_order: number;
  test_count: number;
  visible_count: number;
  updated_at: string;
};

export type TestCase = {
  stdin: string;
  expected_output: string;
  is_hidden: boolean;
  explanation: string | null;
};

export type ProblemFull = Omit<ProblemRow, "test_count" | "visible_count"> & {
  description: string;
  tags: string[];
  input_format: string | null;
  output_format: string | null;
  constraints: string | null;
  explanation: string | null;
  time_limit_ms: number;
  memory_limit_mb: number;
  starter_code: Record<string, string>;
  tests: (TestCase & { position: number })[];
};

/** What the editor sends. Tests have no position: the server numbers them. */
export type ProblemInput = Omit<ProblemFull, "id" | "updated_at" | "tests"> & { tests: TestCase[] };

export type Meta = { page: number; page_size: number; total: number };

export function useOverview() {
  return useQuery({
    queryKey: ["admin", "overview"],
    queryFn: async () => (await api<Overview>("/admin/overview")).data,
  });
}

export function useAdminStudents(page: number, q: string) {
  return useQuery({
    queryKey: ["admin", "students", page, q],
    queryFn: async () => {
      const search = new URLSearchParams({ page: String(page), page_size: "25" });
      if (q.trim()) search.set("q", q.trim());
      const res = await api<AdminStudent[]>(`/admin/students?${search.toString()}`);
      return { items: res.data, meta: res.meta as Meta };
    },
    placeholderData: keepPreviousData,
  });
}

export function useAdminProblems(page: number, q: string, status: string) {
  return useQuery({
    queryKey: ["admin", "problems", page, q, status],
    queryFn: async () => {
      const search = new URLSearchParams({ page: String(page), page_size: "25" });
      if (q.trim()) search.set("q", q.trim());
      if (status) search.set("status", status);
      const res = await api<ProblemRow[]>(`/admin/problems?${search.toString()}`);
      return { items: res.data, meta: res.meta as Meta };
    },
    placeholderData: keepPreviousData,
  });
}

export function useAdminProblem(id: string) {
  return useQuery({
    queryKey: ["admin", "problem", id],
    queryFn: async () => (await api<ProblemFull>(`/admin/problems/${id}`)).data,
  });
}

export function useSaveProblem(id?: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: ProblemInput) =>
      (
        await api<ProblemFull>(id ? `/admin/problems/${id}` : "/admin/problems", {
          method: id ? "PUT" : "POST",
          body: input,
        })
      ).data,
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["admin"] });
    },
  });
}

export function useSetProblemStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, status }: { id: string; status: ProblemRow["status"] }) =>
      (await api<ProblemFull>(`/admin/problems/${id}/status`, { method: "POST", body: { status } })).data,
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["admin"] });
    },
  });
}

export type AuditRow = {
  id: string;
  action: string;
  entity_type: string | null;
  entity_id: string | null;
  actor_id: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
};

export function useAudit() {
  return useQuery({
    queryKey: ["admin", "audit"],
    queryFn: async () => (await api<AuditRow[]>("/admin/audit?limit=50")).data,
  });
}
