import type {
  DashboardFilters,
  DashboardSummaryResponse,
  DashboardTrendResponse,
  DashboardTrendFilters,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${API_BASE}${normalizedPath}`;

  const response = await fetch(url, {
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

export async function getDashboardSummary(
  token: string,
  filters?: DashboardFilters,
): Promise<DashboardSummaryResponse> {
  // Remove undefined and empty string values
  const cleanFilters = Object.fromEntries(
    Object.entries(filters || {}).filter(([, value]) => value !== undefined && value !== "")
  );

  const params = new URLSearchParams();
  Object.entries(cleanFilters).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      params.append(key, String(value));
    }
  });

  const queryString = params.toString();
  const url = `/dashboard/summary${queryString ? `?${queryString}` : ""}`;

  return request<DashboardSummaryResponse>(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function getDashboardTrend(
  token: string,
  filters?: DashboardTrendFilters,
): Promise<DashboardTrendResponse> {
  // Remove undefined and empty string values
  const cleanFilters = Object.fromEntries(
    Object.entries(filters || {}).filter(([, value]) => value !== undefined && value !== "")
  );

  const params = new URLSearchParams();
  Object.entries(cleanFilters).forEach(([key, value]) => {
    if (value !== null && value !== undefined) {
      params.append(key, String(value));
    }
  });

  const queryString = params.toString();
  const url = `/dashboard/trend${queryString ? `?${queryString}` : ""}`;

  return request<DashboardTrendResponse>(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
