import type { MetadataRoute } from "next";

const base = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";

// Only pages that exist. /courses, /about, /contact are added when they are built.
export default function sitemap(): MetadataRoute.Sitemap {
  return ["/", "/login", "/register"].map((path) => ({ url: `${base}${path}` }));
}
