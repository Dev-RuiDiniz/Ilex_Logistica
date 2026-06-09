export interface DashboardFilters {
  estimated_delivery_from?: string;
  estimated_delivery_to?: string;
  month?: number;
  year?: number;
  customer_name?: string;
  destination_uf?: string;
  carrier_id?: number;
  status?: string;
  criticality?: string;
  sla_status?: string;
  is_late?: boolean;
  exception_type?: string;
}

export interface DashboardFiltersApplied {
  estimated_delivery_from?: string | null;
  estimated_delivery_to?: string | null;
  month?: number | null;
  year?: number | null;
  customer_name?: string | null;
  destination_uf?: string | null;
  carrier_id?: number | null;
  status?: string | null;
  criticality?: string | null;
  sla_status?: string | null;
  is_late?: boolean | null;
  exception_type?: string | null;
}

export interface DashboardKpis {
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  critical_count: number;
  warning_count: number;
  unknown_sla_count: number;
  resolved_count: number;
  no_update_count: number;
  exceptions_count: number;
  import_failure_count: number;
  active_alerts_count: number;
  carriers_count: number;
}

export interface DashboardCarrierEfficiencyItem {
  carrier_id: number;
  carrier_name: string | null;
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  critical_count: number;
  lost_count: number;
  total_freight_value: number;
  total_invoice_value: number;
  on_time_percentage: number;
  late_percentage: number;
  lost_percentage: number;
  average_freight_percentage: number;
  average_freight_value: number;
  ranking_by_efficiency: number;
  ranking_by_cost: number;
  ranking_by_volume: number;
}

export interface DashboardExceptionItem {
  shipment_id: number;
  tracking_code: string;
  invoice_number: string | null;
  carrier_id: number;
  carrier_name: string | null;
  customer_name: string | null;
  destination_uf: string | null;
  status: string;
  sla_status: string;
  criticality: string;
  delay_days: number;
  sla_due_date: string | null;
  exception_type: string | null;
  exception_reason: string | null;
  priority: number;
  last_update_at: string;
}

export interface DashboardSummaryResponse {
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  critical_count: number;
  warning_count: number;
  unknown_sla_count: number;
  resolved_count: number;
  no_update_count: number;
  exceptions_count: number;
  import_failure_count: number;
  active_alerts_count: number;
  carriers_count: number;
  top_carriers_by_efficiency: DashboardCarrierEfficiencyItem[];
  top_exceptions: DashboardExceptionItem[];
  generated_at: string;
  filters_applied: DashboardFiltersApplied;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${baseUrl}${normalizedPath}`;

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
