"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, type ReactNode } from "react";

import { BottomNav } from "@/components/layout/bottom-nav";
import { Sidebar } from "@/components/layout/sidebar";
import { TopBar } from "@/components/layout/top-bar";
import { ErrorState } from "@/components/ui/error-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useMe } from "@/features/auth/hooks";
import { ApiError } from "@/lib/api";

// A single problem page is "focus mode": only the statement, editor and checks are shown.
const FOCUS_PATH = /^\/problems\/([^/]+)\/?$/;

function ShellSkeleton() {
  return (
    <div className="min-h-dvh md:flex" aria-busy="true" aria-label="Loading">
      <div className="hidden w-60 shrink-0 border-r border-border p-5 md:block">
        <Skeleton className="h-8 w-40" />
        <div className="mt-6 space-y-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-11 w-full" />
          ))}
        </div>
      </div>
      <div className="flex-1 space-y-4 p-4 md:p-8">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-40 w-full" />
      </div>
    </div>
  );
}

function FocusShell({ slug, children }: { slug: string; children: ReactNode }) {
  return (
    <div className="flex min-h-dvh flex-col">
      <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-border bg-background/95 px-4 backdrop-blur md:px-6">
        <Link href="/problems" className="text-sm font-medium text-muted-foreground hover:text-foreground">
          ← Back to practice
        </Link>
        <Link href={`/problems/${slug}/discussion`} className="text-sm font-medium text-primary hover:underline">
          Discussion
        </Link>
      </header>
      <main id="main" className="mx-auto w-full max-w-6xl flex-1 p-4 md:p-6">
        {children}
      </main>
    </div>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  const me = useMe();
  const router = useRouter();
  const pathname = usePathname();

  const unauthenticated = me.error instanceof ApiError && me.error.status === 401;

  useEffect(() => {
    if (unauthenticated) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
  }, [unauthenticated, pathname, router]);

  if (me.isPending || unauthenticated) return <ShellSkeleton />;

  if (me.isError) {
    const suspended = me.error instanceof ApiError && me.error.code === "ACCOUNT_SUSPENDED";
    return (
      <main id="main" className="grid min-h-dvh place-items-center">
        <ErrorState
          title={suspended ? "Account not active" : "Couldn't load your account"}
          message={me.error.message}
          onRetry={suspended ? undefined : () => me.refetch()}
        />
      </main>
    );
  }

  const focus = FOCUS_PATH.exec(pathname);
  if (focus) {
    return <FocusShell slug={focus[1]}>{children}</FocusShell>;
  }

  return (
    <div className="min-h-dvh md:flex">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar user={me.data} />
        <main id="main" className="mx-auto w-full max-w-5xl flex-1 p-4 pb-24 md:p-8 md:pb-8">
          {children}
        </main>
      </div>
      <BottomNav />
    </div>
  );
}
