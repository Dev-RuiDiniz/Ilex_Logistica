import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PRIVATE_ROUTES = ["/", "/carriers", "/shipments", "/audit", "/reports", "/users", "/alerts", "/exceptions"];

export function isPrivatePath(pathname: string): boolean {
  return PRIVATE_ROUTES.some((route) => pathname === route || pathname.startsWith(`${route}/`));
}

export function shouldRedirectToLogin(pathname: string, hasToken: boolean): boolean {
  return isPrivatePath(pathname) && !hasToken;
}

export function shouldRedirectToHome(pathname: string, hasToken: boolean): boolean {
  return pathname === "/login" && hasToken;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("ilex_token")?.value;
  const hasToken = Boolean(token);

  if (shouldRedirectToLogin(pathname, hasToken)) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (shouldRedirectToHome(pathname, hasToken)) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/login", "/carriers/:path*", "/shipments/:path*", "/orders/:path*", "/quote-rounds/:path*", "/audit/:path*", "/reports/:path*", "/users/:path*", "/alerts/:path*", "/exceptions/:path*"],
};
