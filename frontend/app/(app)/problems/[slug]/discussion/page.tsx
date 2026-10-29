"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { Discussion } from "@/components/community/discussion";
import { buttonClasses } from "@/components/ui/button";

export default function ProblemDiscussionPage() {
  const { slug } = useParams<{ slug: string }>();
  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <nav aria-label="Breadcrumb" className="flex items-center justify-between gap-3 text-sm">
        <Link href={`/problems/${slug}`} className={buttonClasses({ variant: "outline", size: "sm" })}>
          ← Back to the problem
        </Link>
        <span className="text-muted-foreground">Discussion</span>
      </nav>
      <h1 className="text-2xl font-semibold tracking-tight">Discussion</h1>
      <Discussion slug={slug} />
    </div>
  );
}
