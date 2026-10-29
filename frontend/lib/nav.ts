"use client";

import { BookOpen, Code2, Home, MessageSquare, Swords, Trophy, User, type LucideIcon } from "lucide-react";

export type NavItem = {
  label: string;
  href: string;
  icon: LucideIcon;
  /** false = feature not built yet: rendered disabled with a "Soon" badge, never a dead link. */
  available: boolean;
  mobile: boolean;
};

export const NAV_ITEMS: NavItem[] = [
  { label: "Home", href: "/dashboard", icon: Home, available: true, mobile: true },
  { label: "Practice", href: "/topics", icon: Code2, available: true, mobile: true },
  { label: "Courses", href: "/courses", icon: BookOpen, available: false, mobile: true },
  { label: "Community", href: "/community", icon: MessageSquare, available: true, mobile: true },
  { label: "Contests", href: "/contests", icon: Swords, available: false, mobile: false },
  { label: "Leaderboard", href: "/leaderboard", icon: Trophy, available: false, mobile: false },
  { label: "Profile", href: "/profile", icon: User, available: true, mobile: true },
];
