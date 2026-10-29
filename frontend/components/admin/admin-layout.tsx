"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useMe } from "@/features/auth/hooks";
import { cn } from "@/lib/utils";

const TABS = [
  { href: "/admin", label: "Overview" },
  { href: "/admin/students", label: "Students" },
  { href: "/admin/problems", label: "Problems" },
  { href: "/admin/reports", label: "Reports" },
  { href: "/admin/activity", label: "Activity" },
];

/** Hides the admin area from anyone who isn't staff. The server still enforces this on every call. */
export function AdminLayoutShell({ children }: { children: ReactNode }) {
  const { data: me, isPending } = useMe();
  const pathname = usePathname();

  if (isPending) return <Skeleton className="h-64 w-full" />;

  if (!me || (me.role !== "admin" && me.role !== "instructor" && me.role !== "moderator")) {
    return (
      <ErrorState
        title="Staff only"
        message="This area is for staff. Your account doesn't have access."
      />
    );
  }

  const canEdit = me.role === "admin";

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Admin</h1>
        <p className="text-sm text-muted-foreground">
          {canEdit
            ? "You can view and change problems, and handle reports."
            : "You can view everything here and handle reports. Only admins can change problems."}
        </p>
      </header>

      <nav aria-label="Admin sections" className="flex flex-wrap gap-2 border-b border-border pb-3">
        {TABS.map((tab) => {
          const active = tab.href === "/admin" ? pathname === "/admin" : pathname.startsWith(tab.href);
          return (
            <Link
              key={tab.href}
              href={tab.href}
              aria-current={active ? "page" : undefined}
              className={cn(
                "rounded px-3 py-2 text-sm font-medium",
                active ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-muted",
              )}
            >
              {tab.label}
            </Link>
          );
        })}
      </nav>

      {children}
    </div>
  );
}
