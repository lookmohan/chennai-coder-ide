"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "@/lib/api";

export type Presence = { online: boolean; label: string; last_seen_at: string | null };

export type Person = {
  username: string;
  display_name: string;
  avatar_url: string | null;
  presence: Presence;
};

export type RoomMessage = {
  id: string;
  body: string;
  created_at: string;
  author_username: string;
  author_name: string;
  mine: boolean;
  can_delete: boolean;
};

/** The public room. Refreshes every 3 seconds. */
export function useRoom() {
  return useQuery({
    queryKey: ["chat", "room"],
    queryFn: async () => (await api<RoomMessage[]>("/chat/room")).data,
    refetchInterval: 3_000,
  });
}

export function useSendToRoom() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (body: string) => (await api<RoomMessage>("/chat/room", { method: "POST", body: { body } })).data,
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["chat", "room"] }),
  });
}

export function useDeleteFromRoom() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => (await api<{ deleted: boolean }>(`/chat/room/${id}`, { method: "DELETE" })).data,
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["chat", "room"] }),
  });
}

/** Everyone else, most recently active first. Refreshes every 15 seconds so "Online" stays current. */
export function usePeople(q: string) {
  return useQuery({
    queryKey: ["chat", "people", q],
    queryFn: async () => {
      const search = q.trim() ? `?q=${encodeURIComponent(q.trim())}` : "";
      return (await api<Person[]>(`/chat/people${search}`)).data;
    },
    refetchInterval: 15_000,
  });
}
