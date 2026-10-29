"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { OAuthButtons } from "@/features/auth/oauth-buttons";
import { useRegister } from "@/features/auth/hooks";
import { registerSchema, type RegisterInput } from "@/features/auth/schemas";
import { ApiError } from "@/lib/api";

export function RegisterForm() {
  const router = useRouter();
  const registerUser = useRegister();

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<RegisterInput>({ resolver: zodResolver(registerSchema) });

  const onSubmit = handleSubmit((values) =>
    registerUser.mutate(values, {
      onSuccess: () => router.replace("/dashboard"),
      onError: (err) => {
        if (!(err instanceof ApiError)) return;
        // Surface server-side conflicts on the relevant field.
        if (err.code === "EMAIL_TAKEN") setError("email", { message: err.message });
        else if (err.code === "USERNAME_TAKEN") setError("username", { message: err.message });
        else
          err.details?.forEach((d) => {
            if (d.field in values) setError(d.field as keyof RegisterInput, { message: d.message });
          });
      },
    }),
  );

  const fieldLevel =
    registerUser.error instanceof ApiError &&
    ["EMAIL_TAKEN", "USERNAME_TAKEN", "VALIDATION_ERROR"].includes(registerUser.error.code);

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Create your account</h1>
        <p className="mt-1 text-sm text-muted-foreground">Learn. Code. Build.</p>
      </div>

      {registerUser.error && !fieldLevel && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {registerUser.error.message}
        </p>
      )}

      <Input label="Name" autoComplete="name" error={errors.display_name?.message} {...register("display_name")} />
      <Input
        label="Username"
        autoComplete="username"
        autoCapitalize="none"
        hint="Lowercase letters, numbers and underscore."
        error={errors.username?.message}
        {...register("username")}
      />
      <Input label="Email" type="email" autoComplete="email" error={errors.email?.message} {...register("email")} />
      <Input
        label="Password"
        type="password"
        autoComplete="new-password"
        hint="At least 10 characters, with a letter and a number."
        error={errors.password?.message}
        {...register("password")}
      />

      <Button type="submit" className="w-full" loading={registerUser.isPending}>
        Create account
      </Button>

      <OAuthButtons action="Sign up" />

      <p className="text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-primary underline-offset-4 hover:underline">
          Log in
        </Link>
      </p>
    </form>
  );
}
