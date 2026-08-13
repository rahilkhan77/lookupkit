import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    const session = request.cookies.get("lk_session");
    if (!session?.value) {
      const login = new URL("/login", request.url);
      login.searchParams.set("next", request.nextUrl.pathname);
      return NextResponse.redirect(login);
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
