"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useAdminStudents } from "@/features/admin/hooks";

function formatWhen(iso: string | null) {
  if (!iso) return "Never";
  return new Date(iso).toLocaleDateString(undefined, { dateStyle: "medium" });
}

export default function AdminStudentsPage() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const { data, isPending, isError, error, refetch, isPlaceholderData } = useAdminStudents(page, q);

  const total = data?.meta.total ?? 0;
  const lastPage = Math.max(1, Math.ceil(total / 25));

  return (
    <div className="space-y-4">
      <div className="max-w-sm">
        <Input
          label="Search by name, username or email"
          type="search"
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setPage(1);
          }}
        />
      </div>

      {isPending && <Skeleton className="h-64 w-full" />}
      {isError && <ErrorState title="Couldn't load students" message={error.message} onRetry={() => refetch()} />}

      {data && data.items.length === 0 && (
        <EmptyState title="No students found." description={q ? "Try a different search." : "No students have signed up yet."} />
      )}

      {data && data.items.length > 0 && (
        <>
          <div className="overflow-x-auto rounded-lg border border-border" aria-busy={isPlaceholderData}>
            <table className="w-full text-left text-sm">
              <thead className="bg-muted text-muted-foreground">
                <tr>
                  <th className="px-4 py-3 font-medium">Name</th>
                  <th className="px-4 py-3 font-medium">Username</th>
                  <th className="px-4 py-3 font-medium">Email</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Joined</th>
                  <th className="px-4 py-3 font-medium">Last login</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((s) => (
                  <tr key={s.id} className="border-t border-border">
                    <td className="px-4 py-3">{s.display_name}</td>
                    <td className="px-4 py-3">@{s.username}</td>
                    <td className="px-4 py-3">{s.email}</td>
                    <td className="px-4 py-3 capitalize">{s.status}</td>
                    <td className="px-4 py-3">{formatWhen(s.created_at)}</td>
                    <td className="px-4 py-3">{formatWhen(s.last_login_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <nav aria-label="Pages" className="flex items-center justify-between">
            <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Previous
            </Button>
            <p className="text-sm text-muted-foreground">
              Page {page} of {lastPage} · {total} students
            </p>
            <Button variant="outline" size="sm" disabled={page >= lastPage} onClick={() => setPage((p) => p + 1)}>
              Next
            </Button>
          </nav>
        </>
      )}
    </div>
  );
}
