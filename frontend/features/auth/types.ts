export type Profile = {
  username: string;
  display_name: string;
  avatar_url: string | null;
  bio: string | null;
  github_url: string | null;
  linkedin_url: string | null;
  website_url: string | null;
  location: string | null;
};

export type Role = "student" | "instructor" | "admin" | "moderator";

export type User = {
  id: string;
  email: string;
  role: Role;
  status: string;
  created_at: string;
  last_login_at: string | null;
  profile: Profile;
};
