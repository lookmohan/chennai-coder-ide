import { cn } from "@/lib/utils";
import type { Difficulty } from "@/features/problems/types";

const STYLES: Record<Difficulty, string> = {
  Easy: "bg-success/10 text-success",
  Medium: "bg-primary/10 text-primary",
  Hard: "bg-danger/10 text-danger",
};

export function DifficultyBadge({ difficulty, className }: { difficulty: Difficulty; className?: string }) {
  return (
    <span className={cn("rounded px-2 py-0.5 text-xs font-medium", STYLES[difficulty], className)}>
      {difficulty}
    </span>
  );
}
