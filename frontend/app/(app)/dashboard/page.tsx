"use client";

import { BarChart3, Code2, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { buttonClasses } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { useMe } from "@/features/auth/hooks";
import { useSolved } from "@/features/progress/solved";
import { formatDate, greetingForHour } from "@/lib/utils";

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-4 py-2 text-sm">
      <dt className="text-muted-foreground">{label}</dt>
      <dd className="truncate font-medium">{value}</dd>
    </div>
  );
}

export default function DashboardPage() {
  const { data: user } = useMe();
  const solved = useSolved();
  const solvedCount = Object.keys(solved).length;

  // Computed after mount so server and client markup never disagree about the hour.
  const [greeting, setGreeting] = useState("Welcome");
  useEffect(() => setGreeting(greetingForHour(new Date().getHours())), []);

  if (!user) {
    return (
      <div className="space-y-4" aria-busy="true">
        <Skeleton className="h-9 w-72" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  const isStaff = user.role === "admin" || user.role === "instructor";

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">
          {greeting}, {user.profile.display_name}
        </h1>
        <p className="mt-1 text-muted-foreground">Continue your learning journey.</p>
      </header>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Your progress</CardTitle>
          </CardHeader>
          <CardContent>
            {solvedCount === 0 ? (
              <EmptyState
                icon={BarChart3}
                title="No problems solved yet."
                description="Solve a problem by passing every example, and your progress will show here."
              />
            ) : (
              <div className="space-y-3">
                <p className="text-3xl font-semibold">{solvedCount}</p>
                <p className="text-sm text-muted-foreground">
                  {solvedCount === 1 ? "problem" : "problems"} solved in this browser. A problem counts when every
                  visible example passes. This is practice progress, not an official record.
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Practice</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3">
              <Code2 className="h-6 w-6 text-primary" aria-hidden="true" />
              <p className="text-sm text-muted-foreground">
                Pick a Python concept, then work through it from Easy to Hard.
              </p>
            </div>
            <Link href="/topics" className={buttonClasses({ className: "w-full" })}>
              Start practicing
            </Link>
          </CardContent>
        </Card>

        {isStaff && (
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle>Admin</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <ShieldCheck className="h-6 w-6 text-primary" aria-hidden="true" />
                <p className="text-sm text-muted-foreground">
                  View students and problems
                  {user.role === "admin" ? ", and manage the problems students see." : "."}
                </p>
              </div>
              <Link href="/admin" className={buttonClasses({ variant: "outline" })}>
                Open admin
              </Link>
            </CardContent>
          </Card>
        )}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your account</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="divide-y divide-border">
            <Row label="Username" value={`@${user.profile.username}`} />
            <Row label="Email" value={user.email} />
            <Row label="Role" value={user.role} />
            <Row label="Member since" value={formatDate(user.created_at)} />
            <Row label="Last login" value={formatDate(user.last_login_at)} />
          </dl>
        </CardContent>
      </Card>
    </div>
  );
}
