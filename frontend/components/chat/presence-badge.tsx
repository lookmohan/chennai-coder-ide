import { cn } from "@/lib/utils";
import type { Presence } from "@/features/chat/hooks";

/** Green dot and wording: "Online", or "Last seen a few minutes ago", and so on. */
export function PresenceBadge({ presence, className }: { presence: Presence; className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-1.5 text-xs text-muted-foreground", className)}>
      <span
        aria-hidden="true"
        className={cn("h-2 w-2 rounded-full", presence.online ? "bg-success" : "bg-muted-foreground/40")}
      />
      <span className={presence.online ? "font-medium text-success" : undefined}>{presence.label}</span>
    </span>
  );
}
