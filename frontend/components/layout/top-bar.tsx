"use client";

import { LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

import { Logo } from "@/components/layout/logo";
import { ThemeToggle } from "@/components/layout/theme-toggle";
import { Button } from "@/components/ui/button";
import { useLogout } from "@/features/auth/hooks";
import type { User } from "@/features/auth/types";

export function TopBar({ user }: { user: User }) {
  const router = useRouter();
  const logout = useLogout();

  const handleLogout = () =>
    logout.mutate(undefined, {
      onSettled: () => router.replace("/login"),
    });

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border bg-background/95 px-4 backdrop-blur md:px-8">
      <div className="md:hidden">
        <Logo href="/dashboard" showName={false} />
      </div>
      <div className="hidden md:block" />
      <div className="flex items-center gap-1">
        <span className="mr-2 hidden max-w-48 truncate text-sm text-muted-foreground sm:inline">
          {user.profile.display_name}
        </span>
        <ThemeToggle />
        <Button variant="ghost" size="icon" onClick={handleLogout} loading={logout.isPending} aria-label="Log out">
          {!logout.isPending && <LogOut className="h-5 w-5" aria-hidden="true" />}
        </Button>
      </div>
    </header>
  );
}
