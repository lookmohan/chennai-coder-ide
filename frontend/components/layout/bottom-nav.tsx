"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { NAV_ITEMS } from "@/lib/nav";
import { cn } from "@/lib/utils";

export function BottomNav() {
  const pathname = usePathname();
  const items = NAV_ITEMS.filter((i) => i.mobile);
  return (
    <nav
      aria-label="Main"
      className="safe-bottom fixed inset-x-0 bottom-0 z-40 border-t border-border bg-card md:hidden"
    >
      <ul className="grid grid-cols-5">
        {items.map(({ label, href, icon: Icon, available }) => {
          const active = pathname === href || pathname.startsWith(`${href}/`);
          const base = "flex h-14 flex-col items-center justify-center gap-0.5 text-xs font-medium";
          return (
            <li key={href}>
              {available ? (
                <Link
                  href={href}
                  aria-current={active ? "page" : undefined}
                  className={cn(base, active ? "text-primary" : "text-muted-foreground")}
                >
                  <Icon className="h-5 w-5" aria-hidden="true" />
                  {label}
                </Link>
              ) : (
                <span
                  aria-disabled="true"
                  title={`${label} isn't available yet`}
                  className={cn(base, "cursor-not-allowed text-muted-foreground/50")}
                >
                  <Icon className="h-5 w-5" aria-hidden="true" />
                  {label}
                </span>
              )}
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
