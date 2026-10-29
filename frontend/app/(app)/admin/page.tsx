"use client";

import { useOverview } from "@/features/admin/hooks";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-3xl font-semibold">{value}</p>
      </CardContent>
    </Card>
  );
}

export default function AdminOverviewPage() {
  const { data, isPending, isError, error, refetch } = useOverview();

  if (isPending) return <Skeleton className="h-40 w-full" />;
  if (isError) {
    return <ErrorState title="Couldn't load the overview" message={error.message} onRetry={() => refetch()} />;
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <Stat label="Students" value={data.students} />
      <Stat label="Active students (last 7 days)" value={data.active_students_7d} />
      <Stat label="Published problems" value={data.problems_published} />
      <Stat label="Draft problems" value={data.problems_draft} />
      <Stat label="Archived problems" value={data.problems_archived} />
    </div>
  );
}
