"use client";

import { ProblemForm } from "@/components/admin/problem-form";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useAdminProblem } from "@/features/admin/hooks";
import { useParams } from "next/navigation";

export default function EditProblemPage() {
  const { id } = useParams<{ id: string }>();
  const { data, isPending, isError, error, refetch } = useAdminProblem(id);

  if (isPending) return <Skeleton className="h-96 w-full" />;
  if (isError) return <ErrorState title="Couldn't load this problem" message={error.message} onRetry={() => refetch()} />;
  return <ProblemForm key={data.id} problem={data} />;
}
