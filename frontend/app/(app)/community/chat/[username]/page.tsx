"use client";

import Link from "next/link";

import { buttonClasses } from "@/components/ui/button";

/** Direct messages were removed. Chat is now one public room on the Community page. */
export default function RetiredDirectMessagePage() {
  return (
    <div className="space-y-4 text-center">
      <p className="text-muted-foreground">Private messages aren&apos;t available. Chat happens in the public room.</p>
      <Link href="/community" className={buttonClasses({ variant: "outline" })}>
        Go to the community room
      </Link>
    </div>
  );
}
