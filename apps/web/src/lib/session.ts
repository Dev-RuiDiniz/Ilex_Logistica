import type { SessionData, UserRole } from "@/lib/types";

const SESSION_KEY = "ilex.session";

export function getPrimaryRole(roles: UserRole[]): UserRole {
  return roles[0] ?? "logistica";
}

export function saveSession(data: SessionData): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(SESSION_KEY, JSON.stringify(data));
  document.cookie = `ilex_token=${data.accessToken}; path=/`;
}

export function getSession(): SessionData | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as SessionData;
  } catch {
    return null;
  }
}

export function clearSession(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(SESSION_KEY);
  document.cookie = "ilex_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}
