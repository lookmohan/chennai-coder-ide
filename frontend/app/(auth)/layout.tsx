import type { Metadata } from "next";
import type { ReactNode } from "react";

import { Logo } from "@/components/layout/logo";

export const metadata: Metadata = { robots: { index: true, follow: true } };

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-dvh flex-col items-center px-4 py-8">
      <Logo />
      <main id="main" className="mt-10 w-full max-w-sm">
        {children}
      </main>
    </div>
  );
}
