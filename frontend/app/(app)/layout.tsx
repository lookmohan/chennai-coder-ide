import type { Metadata } from "next";
import type { ReactNode } from "react";

import { AppShell } from "@/components/layout/app-shell";
import { Heartbeat } from "@/components/presence/heartbeat";

// The signed-in application must not be indexed.
export const metadata: Metadata = { robots: { index: false, follow: false } };

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <AppShell>
      <Heartbeat />
      {children}
    </AppShell>
  );
}
