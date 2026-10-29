"use client";

import { useState } from "react";

import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useAudit } from "@/features/admin/hooks";
import { ErrorState } from "@/components/ui/error-state";

export default function AdminActivityPage() {
  const { data, isPending, isError, error, refetch } = useAudit();
  const [open, setOpen] = useState<string | null>(null);

  if (isPending) return <Skeleton className="h-64 w-full" />;
  if (isError) return <ErrorState title="Couldn't load activity" message={error.message} onRetry={() => refetch()} />;
  if (data.length === 0) return <EmptyState title="No activity yet." description="Sign-ins and admin changes appear here." />;

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-left text-sm">
        <thead className="bg-muted text-muted-foreground">
          <tr>
            <th className="px-4 py-3 font-medium">When</th>
            <th className="px-4 py-3 font-medium">Action</th>
            <th className="px-4 py-3 font-medium">Details</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id} className="border-t border-border align-top">
              <td className="px-4 py-3 whitespace-nowrap">{new Date(row.created_at).toLocaleString()}</td>
              <td className="px-4 py-3">{row.action}</td>
              <td className="px-4 py-3">
                <button
                  type="button"
                  className="text-left text-primary underline-offset-4 hover:underline"
                  aria-expanded={open === row.id}
                  onClick={() => setOpen(open === row.id ? null : row.id)}
                >
                  {open === row.id ? "Hide" : "Show"}
                </button>
                {open === row.id && (
                  <pre className="mt-2 overflow-x-auto rounded bg-muted p-2 font-mono text-xs">
                    {JSON.stringify(row.metadata, null, 2)}
                  </pre>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
