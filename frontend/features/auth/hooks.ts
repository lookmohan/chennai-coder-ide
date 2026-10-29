"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";
import type { LoginInput, ProfileInput, RegisterInput } from "./schemas";
import type { User } from "./types";

export const meKey = ["me"] as const;

export function useMe() {
  return useQuery({
    queryKey: meKey,
    queryFn: async () => (await api<User>("/auth/me")).data,
    retry: false,
    staleTime: 60_000,
  });
}

export function useLogin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: LoginInput) => (await api<User>("/auth/login", { method: "POST", body: input })).data,
    onSuccess: (user) => qc.setQueryData(meKey, user),
  });
}

export function useRegister() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: RegisterInput) =>
      (await api<User>("/auth/register", { method: "POST", body: input })).data,
    onSuccess: (user) => qc.setQueryData(meKey, user),
  });
}

export function useLogout() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async () => (await api("/auth/logout", { method: "POST" })).data,
    // Drop every cached server value so nothing from this session leaks to the next.
    onSettled: () => qc.clear(),
  });
}

/** Empty optional strings are sent as null so the backend clears the field. */
export function useUpdateProfile() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (input: ProfileInput) => {
      const body = {
        display_name: input.display_name,
        bio: input.bio.trim() || null,
        location: input.location.trim() || null,
        github_url: input.github_url.trim() || null,
        linkedin_url: input.linkedin_url.trim() || null,
        website_url: input.website_url.trim() || null,
      };
      return (await api<User>("/users/me", { method: "PATCH", body })).data;
    },
    onSuccess: (user) => qc.setQueryData(meKey, user),
  });
}
