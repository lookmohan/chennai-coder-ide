"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { OAuthButtons } from "@/features/auth/oauth-buttons";
import { useLogin, useMe } from "@/features/auth/hooks";
import { loginSchema, type LoginInput } from "@/features/auth/schemas";
import { safeNextPath } from "@/lib/utils";

// Friendly text for errors that come back from Google/GitHub sign-in.
const SIGN_IN_ERRORS: Record<string, string> = {
  oauth_state: "That sign-in link expired. Please try again.",
  oauth_failed: "Sign-in with that account didn't work. Please try again.",
  oauth_no_verified_email: "Your GitHub account needs a verified email before you can sign in with it.",
  oauth_not_configured: "That sign-in method isn't set up yet.",
  email_in_use: "An account with this email already exists. Log in with your password instead.",
  account_suspended: "This account is not active. Contact support.",
};

export function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const next = safeNextPath(params.get("next"));
  const oauthError = params.get("error");
  const me = useMe();
  const login = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginInput>({ resolver: zodResolver(loginSchema) });

  // Already signed in? Skip the form.
  useEffect(() => {
    if (me.data) router.replace(next);
  }, [me.data, next, router]);

  const onSubmit = handleSubmit((values) =>
    login.mutate(values, { onSuccess: () => router.replace(next) }),
  );

  const oauthMessage = oauthError ? (SIGN_IN_ERRORS[oauthError] ?? "Sign-in didn't work. Please try again.") : null;

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Welcome back</h1>
        <p className="mt-1 text-sm text-muted-foreground">Log in to continue your learning.</p>
      </div>

      {oauthMessage && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {oauthMessage}
        </p>
      )}

      {login.error && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {login.error.message}
        </p>
      )}

      <Input label="Email" type="email" autoComplete="email" error={errors.email?.message} {...register("email")} />
      <Input
        label="Password"
        type="password"
        autoComplete="current-password"
        error={errors.password?.message}
        {...register("password")}
      />

      <Button type="submit" className="w-full" loading={login.isPending}>
        Log in
      </Button>

      <OAuthButtons action="Log in" />

      <p className="text-center text-sm text-muted-foreground">
        New to Chennai Coder?{" "}
        <Link href="/register" className="font-medium text-primary underline-offset-4 hover:underline">
          Create an account
        </Link>
      </p>
    </form>
  );
}
