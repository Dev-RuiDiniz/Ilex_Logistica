import type {
  Carrier,
  CreateShipmentTreatmentRequest,
  DailyReportResponse,
  DeliveryDetail,
  DeliveryListParams,
  DeliveryListResponse,
  ExceptionShipmentListResponse,
  ImportConfirmResponse,
  ImportPreviewV2Response,
  PromoteDeliveryRequest,
  PromoteDeliveryResponse,
  ShipmentDetail,
  ShipmentListParams,
  ShipmentListResponse,
  ShipmentTreatment,
  UploadResponse,
  UserListItem,
  UserRole,
  SlaRule,
  SlaRuleCreate,
  SlaRuleUpdate,
  SlaRecalculateResponse,
  CarrierEfficiencyResponse,
  CarrierEfficiencyFilters,
  DashboardSummaryResponse,
  DashboardTrendResponse,
} from "@/lib/types";

export function getApiBaseUrl(envValue = process.env.NEXT_PUBLIC_API_URL): string {
  const fallback = "http://127.0.0.1:8000/api/v1";
  const raw = (envValue ?? fallback).trim();
  return raw.endsWith("/") ? raw.slice(0, -1) : raw;
}

export function buildApiUrl(path: string, envValue = process.env.NEXT_PUBLIC_API_URL): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${getApiBaseUrl(envValue)}${normalizedPath}`;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
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
    throw new ApiError(text || "Falha na API", response.status, response.statusText);
  }
  return response.json() as Promise<T>;
}

async function requestMultipart<T>(path: string, formData: FormData, token: string): Promise<T> {
  const response = await fetch(buildApiUrl(path), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new ApiError(text || "Falha na API", response.status, response.statusText);
  }
  return response.json() as Promise<T>;
}

export async function apiLogin(email: string, password: string) {
  // Dev bypass — auto-login without backend
  if (email === "dev@ilex.com" && password === "dev123") {
    return {
      access_token: "dev-token-bypass",
      refresh_token: "dev-refresh-bypass",
      token_type: "bearer",
      roles: ["admin"] as UserRole[],
    };
  }
  return request<{ access_token: string; refresh_token: string; token_type: string; roles: UserRole[] }>("/auth/login", {
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

export async function getDashboardSummary(token: string): Promise<DashboardSummaryResponse> {
  return request<DashboardSummaryResponse>("/dashboard/summary", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getDashboardTrend(token: string, days = 30): Promise<DashboardTrendResponse> {
  return request<DashboardTrendResponse>(`/dashboard/trend?days=${days}`, {
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

export async function uploadShipmentsCsv(token: string, file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return requestMultipart<UploadResponse>("/shipments/upload", formData, token);
}

// BETA-012B: New preview endpoint using /api/v1/imports/preview
// BETA-012C: Added optional source parameter for layout-specific mapping
export async function previewShipmentImport(token: string, file: File, source?: string): Promise<ImportPreviewV2Response> {
  const formData = new FormData();
  formData.append("file", file);
  if (source) {
    formData.append("source", source);
  }
  return requestMultipart<ImportPreviewV2Response>("/imports/preview", formData, token);
}

export async function confirmShipmentsImport(token: string, importId: number): Promise<ImportConfirmResponse> {
  return request<ImportConfirmResponse>("/imports/confirm", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ import_id: importId, confirm: true }),
  });
}

export async function listShipments(token: string, params: ShipmentListParams = {}): Promise<ShipmentListResponse> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.append("page", params.page.toString());
  if (params.page_size) searchParams.append("page_size", params.page_size.toString());
  if (params.status) searchParams.append("status", params.status);
  if (params.carrier_id) searchParams.append("carrier_id", params.carrier_id.toString());
  if (params.tracking_code) searchParams.append("tracking_code", params.tracking_code);
  if (params.invoice_number) searchParams.append("invoice_number", params.invoice_number);
  if (params.invoice_key) searchParams.append("invoice_key", params.invoice_key);
  if (params.fiscal_document) searchParams.append("fiscal_document", params.fiscal_document);
  if (params.criticality) searchParams.append("criticality", params.criticality);
  if (params.estimated_delivery_from) searchParams.append("estimated_delivery_from", params.estimated_delivery_from);
  if (params.estimated_delivery_to) searchParams.append("estimated_delivery_to", params.estimated_delivery_to);
  if (params.due_date_from) searchParams.append("due_date_from", params.due_date_from);
  if (params.due_date_to) searchParams.append("due_date_to", params.due_date_to);
  if (params.collection_departure_from) searchParams.append("collection_departure_from", params.collection_departure_from);
  if (params.collection_departure_to) searchParams.append("collection_departure_to", params.collection_departure_to);
  if (params.customer_name) searchParams.append("customer_name", params.customer_name);
  if (params.destination_uf) searchParams.append("destination_uf", params.destination_uf);
  if (params.month) searchParams.append("month", params.month.toString());
  if (params.year) searchParams.append("year", params.year.toString());
  if (params.search) searchParams.append("search", params.search);
  if (params.sort_by) searchParams.append("sort_by", params.sort_by);
  if (params.sort_order) searchParams.append("sort_order", params.sort_order);
  // BETA-013A: SLA filters
  if (params.sla_status) searchParams.append("sla_status", params.sla_status);
  if (params.is_late !== undefined) searchParams.append("is_late", params.is_late.toString());
  // BETA-031: Filtros fiscais/financeiros
  if (params.freight_value_min !== undefined) searchParams.append("freight_value_min", params.freight_value_min.toString());
  if (params.freight_value_max !== undefined) searchParams.append("freight_value_max", params.freight_value_max.toString());
  if (params.invoice_value_min !== undefined) searchParams.append("invoice_value_min", params.invoice_value_min.toString());
  if (params.invoice_value_max !== undefined) searchParams.append("invoice_value_max", params.invoice_value_max.toString());
  if (params.freight_percentage_min !== undefined) searchParams.append("freight_percentage_min", params.freight_percentage_min.toString());
  if (params.freight_percentage_max !== undefined) searchParams.append("freight_percentage_max", params.freight_percentage_max.toString());
  if (params.amount_min !== undefined) searchParams.append("amount_min", params.amount_min.toString());
  if (params.amount_max !== undefined) searchParams.append("amount_max", params.amount_max.toString());

  const query = searchParams.toString();
  return request<ShipmentListResponse>(`/shipments${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function listExceptionShipments(token: string, params: ShipmentListParams = {}): Promise<ExceptionShipmentListResponse> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.append("page", params.page.toString());
  if (params.page_size) searchParams.append("page_size", params.page_size.toString());
  if (params.status) searchParams.append("status", params.status);
  if (params.criticality) searchParams.append("criticality", params.criticality);
  if (params.estimated_delivery_from) searchParams.append("estimated_delivery_from", params.estimated_delivery_from);
  if (params.estimated_delivery_to) searchParams.append("estimated_delivery_to", params.estimated_delivery_to);
  if (params.due_date_from) searchParams.append("due_date_from", params.due_date_from);
  if (params.due_date_to) searchParams.append("due_date_to", params.due_date_to);
  if (params.sort_by) searchParams.append("sort_by", params.sort_by);
  if (params.sort_order) searchParams.append("sort_order", params.sort_order);
  const query = searchParams.toString();
  return request<ExceptionShipmentListResponse>(`/shipments/exceptions${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getShipmentDetail(token: string, shipmentId: number): Promise<ShipmentDetail> {
  return request<ShipmentDetail>(`/shipments/${shipmentId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function listShipmentTreatments(token: string, shipmentId: number): Promise<ShipmentTreatment[]> {
  return request<ShipmentTreatment[]>(`/shipments/${shipmentId}/treatments`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function createShipmentTreatment(
  token: string,
  shipmentId: number,
  payload: CreateShipmentTreatmentRequest,
): Promise<ShipmentTreatment> {
  return request<ShipmentTreatment>(`/shipments/${shipmentId}/treatments`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function getDailyReport(token: string): Promise<DailyReportResponse> {
  return request<DailyReportResponse>("/reports/daily", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function listUsers(token: string): Promise<UserListItem[]> {
  return request<UserListItem[]>("/users", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function createUser(
  token: string,
  payload: { email: string; full_name: string; password: string; roles: UserRole[] },
): Promise<UserListItem> {
  return request<UserListItem>("/users", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function updateUser(
  token: string,
  userId: number,
  payload: { full_name?: string; roles?: UserRole[]; is_active?: boolean },
): Promise<UserListItem> {
  return request<UserListItem>(`/users/${userId}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function listDeliveries(token: string, params: DeliveryListParams = {}): Promise<DeliveryListResponse> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.append("page", params.page.toString());
  if (params.page_size) searchParams.append("page_size", params.page_size.toString());
  if (params.nf) searchParams.append("nf", params.nf);
  if (params.transportadora) searchParams.append("transportadora", params.transportadora);
  if (params.data_coleta) searchParams.append("data_coleta", params.data_coleta);

  const query = searchParams.toString();
  return request<DeliveryListResponse>(`/deliveries${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getDeliveryDetail(token: string, deliveryId: number): Promise<DeliveryDetail> {
  return request<DeliveryDetail>(`/deliveries/${deliveryId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function promoteDelivery(
  token: string,
  deliveryId: number,
  payload: PromoteDeliveryRequest,
): Promise<PromoteDeliveryResponse> {
  return request<PromoteDeliveryResponse>(`/deliveries/${deliveryId}/promote`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

// BETA-013A: SLA Rules API
export async function listSlaRules(token: string, params?: { carrier_id?: number; destination_uf?: string; is_active?: boolean }): Promise<SlaRule[]> {
  const searchParams = new URLSearchParams();
  if (params?.carrier_id) searchParams.append("carrier_id", params.carrier_id.toString());
  if (params?.destination_uf) searchParams.append("destination_uf", params.destination_uf);
  if (params?.is_active !== undefined) searchParams.append("is_active", params.is_active.toString());

  const query = searchParams.toString();
  return request<SlaRule[]>(`/sla/rules${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function createSlaRule(token: string, payload: SlaRuleCreate): Promise<SlaRule> {
  return request<SlaRule>("/sla/rules", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function updateSlaRule(token: string, ruleId: number, payload: SlaRuleUpdate): Promise<SlaRule> {
  return request<SlaRule>(`/sla/rules/${ruleId}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function recalculateSla(token: string, params?: { carrier_id?: number; destination_uf?: string }): Promise<SlaRecalculateResponse> {
  const searchParams = new URLSearchParams();
  if (params?.carrier_id) searchParams.append("carrier_id", params.carrier_id.toString());
  if (params?.destination_uf) searchParams.append("destination_uf", params.destination_uf);

  const query = searchParams.toString();
  return request<SlaRecalculateResponse>(`/sla/recalculate${query ? `?${query}` : ""}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function recalculateShipmentSla(token: string, shipmentId: number): Promise<SlaRecalculateResponse> {
  return request<SlaRecalculateResponse>(`/sla/recalculate/${shipmentId}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getCarrierEfficiency(token: string, filters: CarrierEfficiencyFilters = {}): Promise<CarrierEfficiencyResponse> {
  const searchParams = new URLSearchParams();
  if (filters.estimated_delivery_from) searchParams.append("estimated_delivery_from", filters.estimated_delivery_from);
  if (filters.estimated_delivery_to) searchParams.append("estimated_delivery_to", filters.estimated_delivery_to);
  if (filters.month) searchParams.append("month", filters.month.toString());
  if (filters.year) searchParams.append("year", filters.year.toString());
  if (filters.customer_name) searchParams.append("customer_name", filters.customer_name);
  if (filters.destination_uf) searchParams.append("destination_uf", filters.destination_uf);
  if (filters.carrier_id) searchParams.append("carrier_id", filters.carrier_id.toString());
  if (filters.status) searchParams.append("status", filters.status);
  if (filters.criticality) searchParams.append("criticality", filters.criticality);
  if (filters.sla_status) searchParams.append("sla_status", filters.sla_status);
  if (filters.is_late !== undefined) searchParams.append("is_late", filters.is_late.toString());

  const query = searchParams.toString();
  return request<CarrierEfficiencyResponse>(`/shipments/analytics/carrier-efficiency${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

