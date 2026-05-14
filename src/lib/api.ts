import type { Carrier } from "@/lib/types";

export function getApiBaseUrl(envValue = process.env.NEXT_PUBLIC_API_URL): string {
  const fallback = "http://127.0.0.1:8000/api/v1";
  const raw = (envValue ?? fallback).trim();
  return raw.endsWith("/") ? raw.slice(0, -1) : raw;
}

export function buildApiUrl(path: string, envValue = process.env.NEXT_PUBLIC_API_URL): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${getApiBaseUrl(envValue)}${normalizedPath}`;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(buildApiUrl(path), {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Falha na API");
  }
  return response.json() as Promise<T>;
}

export async function apiLogin(email: string, password: string) {
  return request<{ access_token: string; refresh_token: string; token_type: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function listCarriers(token: string, includeInactive = false): Promise<Carrier[]> {
  const query = includeInactive ? "?include_inactive=true" : "";
  return request<Carrier[]>(`/carriers${query}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function createCarrier(
  token: string,
  payload: { name: string; external_code?: string; integration_metadata: Record<string, unknown> },
): Promise<Carrier> {
  return request<Carrier>("/carriers", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function updateCarrier(
  token: string,
  id: number,
  payload: { name?: string; external_code?: string; integration_metadata?: Record<string, unknown> },
): Promise<Carrier> {
  return request<Carrier>(`/carriers/${id}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function inactivateCarrier(token: string, id: number): Promise<Carrier> {
  return request<Carrier>(`/carriers/${id}/inactivate`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
}
