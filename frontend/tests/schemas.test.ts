import { describe, expect, it } from "vitest";

import { loginSchema, profileSchema, registerSchema } from "@/features/auth/schemas";
import { greetingForHour, safeNextPath } from "@/lib/utils";

const validRegistration = {
  display_name: "Asha",
  username: "asha_k",
  email: "asha@example.com",
  password: "correct-horse-9",
};

describe("registerSchema", () => {
  it("accepts valid input and lowercases the username", () => {
    const parsed = registerSchema.parse({ ...validRegistration, username: "Asha_K" });
    expect(parsed.username).toBe("asha_k");
  });

  it("rejects short passwords", () => {
    expect(registerSchema.safeParse({ ...validRegistration, password: "abc123" }).success).toBe(false);
  });

  it("requires a letter and a number in the password", () => {
    expect(registerSchema.safeParse({ ...validRegistration, password: "onlyletterslong" }).success).toBe(false);
    expect(registerSchema.safeParse({ ...validRegistration, password: "1234567890123" }).success).toBe(false);
  });

  it("rejects invalid usernames", () => {
    expect(registerSchema.safeParse({ ...validRegistration, username: "no spaces!" }).success).toBe(false);
    expect(registerSchema.safeParse({ ...validRegistration, username: "ab" }).success).toBe(false);
  });

  it("rejects invalid emails", () => {
    expect(registerSchema.safeParse({ ...validRegistration, email: "nope" }).success).toBe(false);
  });
});

describe("loginSchema", () => {
  it("requires email and password", () => {
    expect(loginSchema.safeParse({ email: "", password: "" }).success).toBe(false);
    expect(loginSchema.safeParse({ email: "a@b.co", password: "x" }).success).toBe(true);
  });
});

describe("profileSchema", () => {
  const base = { display_name: "Asha", bio: "", location: "", github_url: "", linkedin_url: "", website_url: "" };

  it("allows empty optional URLs", () => {
    expect(profileSchema.safeParse(base).success).toBe(true);
  });

  it("allows https URLs and rejects javascript: URLs", () => {
    expect(profileSchema.safeParse({ ...base, website_url: "https://example.com" }).success).toBe(true);
    expect(profileSchema.safeParse({ ...base, website_url: "javascript:alert(1)" }).success).toBe(false);
    expect(profileSchema.safeParse({ ...base, github_url: "not a url" }).success).toBe(false);
  });

  it("enforces bio length", () => {
    expect(profileSchema.safeParse({ ...base, bio: "x".repeat(501) }).success).toBe(false);
  });
});

describe("safeNextPath", () => {
  it("keeps same-site relative paths", () => {
    expect(safeNextPath("/profile")).toBe("/profile");
  });

  it("blocks open redirects", () => {
    expect(safeNextPath("//evil.com")).toBe("/dashboard");
    expect(safeNextPath("https://evil.com")).toBe("/dashboard");
    expect(safeNextPath("/\\evil.com")).toBe("/dashboard");
    expect(safeNextPath(null)).toBe("/dashboard");
  });
});

describe("greetingForHour", () => {
  it("picks the right greeting", () => {
    expect(greetingForHour(8)).toBe("Good morning");
    expect(greetingForHour(14)).toBe("Good afternoon");
    expect(greetingForHour(20)).toBe("Good evening");
  });
});
