import Link from "next/link";

import { cn } from "@/lib/utils";

export function Logo({ className, href = "/", showName = true }: { className?: string; href?: string; showName?: boolean }) {
  return (
    <Link href={href} className={cn("inline-flex items-center gap-2.5 rounded", className)} aria-label="Chennai Coder home">
      {/* eslint-disable-next-line @next/next/no-img-element -- static SVG, no optimisation needed */}
      <img src="/logo.svg" alt="" width={32} height={32} className="h-8 w-8" />
      {showName && <span className="text-base font-semibold tracking-tight">Chennai Coder</span>}
    </Link>
  );
}
