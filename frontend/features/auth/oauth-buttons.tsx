"use client";

import { useQuery } from "@tanstack/react-query";

import { buttonClasses } from "@/components/ui/button";
import { api } from "@/lib/api";

const PROVIDERS = [
  { id: "google", name: "Google" },
  { id: "github", name: "GitHub" },
] as const;

/** Shows only the sign-in methods the server has set up. Nothing appears if none are configured. */
export function OAuthButtons({ action }: { action: "Log in" | "Sign up" }) {
  const { data } = useQuery({
    queryKey: ["oauth-providers"],
    queryFn: async () => (await api<Record<string, boolean>>("/auth/oauth/providers")).data,
    staleTime: 5 * 60_000,
  });

  const available = PROVIDERS.filter((p) => data?.[p.id]);
  if (available.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3 text-xs uppercase tracking-wide text-muted-foreground">
        <span className="h-px flex-1 bg-border" aria-hidden="true" />
        or
        <span className="h-px flex-1 bg-border" aria-hidden="true" />
      </div>
      {available.map((provider) => (
        // A plain link (not fetch), because the server must redirect the browser to the provider.
        <a
          key={provider.id}
          href={`/api/v1/auth/oauth/${provider.id}/start`}
          className={buttonClasses({ variant: "outline", className: "w-full" })}
        >
          {action === "Log in" ? "Log in" : "Sign up"} with {provider.name}
        </a>
      ))}
    </div>
  );
}
