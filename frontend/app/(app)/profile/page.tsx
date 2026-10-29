"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { AvatarEditor } from "@/components/profile/avatar-editor";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Textarea } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useMe, useUpdateProfile } from "@/features/auth/hooks";
import { profileSchema, type ProfileInput } from "@/features/auth/schemas";
import type { User } from "@/features/auth/types";
import { ApiError } from "@/lib/api";

function ProfileForm({ user }: { user: User }) {
  const update = useUpdateProfile();
  const p = user.profile;

  const {
    register,
    handleSubmit,
    setError,
    reset,
    formState: { errors, isDirty },
  } = useForm<ProfileInput>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      display_name: p.display_name,
      bio: p.bio ?? "",
      location: p.location ?? "",
      github_url: p.github_url ?? "",
      linkedin_url: p.linkedin_url ?? "",
      website_url: p.website_url ?? "",
    },
  });

  const onSubmit = handleSubmit((values) =>
    update.mutate(values, {
      onSuccess: (saved) =>
        reset({
          display_name: saved.profile.display_name,
          bio: saved.profile.bio ?? "",
          location: saved.profile.location ?? "",
          github_url: saved.profile.github_url ?? "",
          linkedin_url: saved.profile.linkedin_url ?? "",
          website_url: saved.profile.website_url ?? "",
        }),
      onError: (err) => {
        if (err instanceof ApiError)
          err.details?.forEach((d) => {
            if (d.field in values) setError(d.field as keyof ProfileInput, { message: d.message });
          });
      },
    }),
  );

  const generalError =
    update.error && !(update.error instanceof ApiError && update.error.code === "VALIDATION_ERROR")
      ? update.error.message
      : null;

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-4">
      <Input label="Username" value={`@${p.username}`} readOnly disabled hint="Usernames can't be changed yet." />
      <Input label="Name" autoComplete="name" error={errors.display_name?.message} {...register("display_name")} />
      <Textarea label="Bio" rows={4} error={errors.bio?.message} {...register("bio")} />
      <Input label="Location" error={errors.location?.message} {...register("location")} />
      <div className="grid gap-4 md:grid-cols-2">
        <Input label="GitHub" type="url" placeholder="https://github.com/you" error={errors.github_url?.message} {...register("github_url")} />
        <Input label="LinkedIn" type="url" placeholder="https://linkedin.com/in/you" error={errors.linkedin_url?.message} {...register("linkedin_url")} />
      </div>
      <Input label="Website" type="url" placeholder="https://example.com" error={errors.website_url?.message} {...register("website_url")} />

      {generalError && (
        <p role="alert" className="rounded border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {generalError}
        </p>
      )}
      {update.isSuccess && !isDirty && (
        <p role="status" className="text-sm text-success">
          Profile saved.
        </p>
      )}

      <Button type="submit" loading={update.isPending} disabled={!isDirty}>
        Save changes
      </Button>
    </form>
  );
}

export default function ProfilePage() {
  const { data: user } = useMe();
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Profile</h1>
        <p className="mt-1 text-muted-foreground">How you appear to other learners.</p>
      </header>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Profile photo</CardTitle>
        </CardHeader>
        <CardContent>
          {user ? (
            <AvatarEditor user={user} />
          ) : (
            <Skeleton className="h-24 w-24 rounded-full" />
          )}
        </CardContent>
      </Card>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Edit profile</CardTitle>
        </CardHeader>
        <CardContent>
          {user ? (
            <ProfileForm user={user} />
          ) : (
            <div className="space-y-4" aria-busy="true">
              <Skeleton className="h-11 w-full" />
              <Skeleton className="h-11 w-full" />
              <Skeleton className="h-24 w-full" />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
