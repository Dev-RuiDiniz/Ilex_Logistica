import { buildApiUrl } from "./api";

export interface ExceptionSummary {
  total_exceptions: number;
  critical_count: number;
  late_count: number;
  warning_count: number;
  unknown_sla_count: number;
}

export interface ExceptionItem {
  shipment_id: number;
  tracking_code: string;
  invoice_number: string | null;
  carrier_id: number;
  carrier_name: string | null;
  customer_name: string | null;
  destination_uf: string | null;
  status: string;
  sla_status: string | null;
  criticality: string;
  delay_days: number;
  sla_due_date: string | null;
  exception_type: string;
  exception_reason: string;
  priority: number;
  last_update_at: string;
}

export interface ExceptionsPanelResponse {
  summary: ExceptionSummary;
  items: ExceptionItem[];
  filters_applied: Record<string, unknown>;
  generated_at: string;
}

export interface ExceptionsPanelFilters {
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

export async function getExceptionsPanel(
  accessToken: string,
  filters: ExceptionsPanelFilters = {}
): Promise<ExceptionsPanelResponse> {
  // Remove undefined and empty string values
  const cleanFilters = Object.fromEntries(
    Object.entries(filters).filter(([_, value]) => value !== undefined && value !== "")
  );

  // Build query string
  const queryParams = new URLSearchParams();
  Object.entries(cleanFilters).forEach(([key, value]) => {
    queryParams.append(key, String(value));
  });

  const url = buildApiUrl(`/shipments/analytics/exceptions${queryParams.toString() ? `?${queryParams.toString()}` : ""}`);

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Erro ao buscar painel de exceções");
  }

  return response.json();
}
