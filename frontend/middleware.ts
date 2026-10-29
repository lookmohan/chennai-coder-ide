import { NextResponse, type NextRequest } from "next/server";

// UX convenience only: skip the flash of the app shell when there is clearly no session.
// Real authentication and authorization are enforced by the backend on every API call.
export function middleware(req: NextRequest) {
  if (!req.cookies.get("cc_access")) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.search = `?next=${encodeURIComponent(req.nextUrl.pathname)}`;
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = { matcher: ["/dashboard/:path*", "/profile/:path*"] };
