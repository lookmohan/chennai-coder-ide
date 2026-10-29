"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { Logo } from "@/components/layout/logo";
import { NAV_ITEMS } from "@/lib/nav";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r border-border bg-card md:flex">
      <div className="flex h-16 items-center px-5">
        <Logo href="/dashboard" />
      </div>
      <nav aria-label="Main" className="flex-1 space-y-1 px-3 py-2">
        {NAV_ITEMS.map(({ label, href, icon: Icon, available }) => {
          const active = pathname === href || pathname.startsWith(`${href}/`);
          const base = "flex h-11 items-center gap-3 rounded px-3 text-sm font-medium";
          if (!available) {
            return (
              <span
                key={href}
                aria-disabled="true"
                title={`${label} isn't available yet`}
                className={cn(base, "cursor-not-allowed text-muted-foreground/70")}
              >
                <Icon className="h-5 w-5" aria-hidden="true" />
                <span className="flex-1">{label}</span>
                <span className="rounded bg-muted px-1.5 py-0.5 text-xs">Soon</span>
              </span>
            );
          }
          return (
            <Link
              key={href}
              href={href}
              aria-current={active ? "page" : undefined}
              className={cn(base, active ? "bg-primary/10 text-primary" : "text-foreground hover:bg-muted")}
            >
              <Icon className="h-5 w-5" aria-hidden="true" />
              {label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
