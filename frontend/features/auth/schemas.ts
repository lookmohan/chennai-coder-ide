import { z } from "zod";

// Client-side rules mirror the backend (backend/app/schemas). The backend remains the authority.

export const loginSchema = z.object({
  email: z.string().trim().min(1, "Enter your email").email("Enter a valid email"),
  password: z.string().min(1, "Enter your password"),
});
export type LoginInput = z.infer<typeof loginSchema>;

export const registerSchema = z.object({
  display_name: z.string().trim().min(1, "Enter your name").max(60, "Max 60 characters"),
  username: z
    .string()
    .trim()
    .toLowerCase()
    .regex(/^[a-z0-9_]{3,30}$/, "3-30 characters: lowercase letters, numbers, underscore"),
  email: z.string().trim().min(1, "Enter your email").email("Enter a valid email"),
  password: z
    .string()
    .min(10, "At least 10 characters")
    .max(128, "At most 128 characters")
    .refine((v) => /[A-Za-z]/.test(v) && /\d/.test(v), "Include at least one letter and one number"),
});
export type RegisterInput = z.infer<typeof registerSchema>;

const optionalUrl = z
  .string()
  .trim()
  .max(300, "Max 300 characters")
  .refine((v) => {
    if (!v) return true;
    try {
      const u = new URL(v);
      return u.protocol === "http:" || u.protocol === "https:";
    } catch {
      return false;
    }
  }, "Enter a valid http(s) URL");

export const profileSchema = z.object({
  display_name: z.string().trim().min(1, "Enter your name").max(60, "Max 60 characters"),
  bio: z.string().max(500, "Max 500 characters"),
  location: z.string().max(100, "Max 100 characters"),
  github_url: optionalUrl,
  linkedin_url: optionalUrl,
  website_url: optionalUrl,
});
export type ProfileInput = z.infer<typeof profileSchema>;
