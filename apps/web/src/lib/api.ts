import type {
  Carrier,
  CreateShipmentTreatmentRequest,
  DailyReportResponse,
  DeliveryDetail,
  DeliveryListParams,
  DeliveryListResponse,
  ExceptionShipmentListResponse,
  ImportConfirmResponse,
  ShipmentDetail,
  ShipmentListParams,
  ShipmentListResponse,
  ShipmentTreatment,
  UploadResponse,
  UserListItem,
  UserRole,
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
    throw new Error(text || "Falha na API");
  }
  return response.json() as Promise<T>;
}

export async function apiLogin(email: string, password: string) {
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

export async function confirmShipmentsImport(token: string, importId: number): Promise<ImportConfirmResponse> {
  return request<ImportConfirmResponse>("/shipments/import", {
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
  if (params.fiscal_document) searchParams.append("fiscal_document", params.fiscal_document);
  if (params.criticality) searchParams.append("criticality", params.criticality);
  if (params.estimated_delivery_from) searchParams.append("estimated_delivery_from", params.estimated_delivery_from);
  if (params.estimated_delivery_to) searchParams.append("estimated_delivery_to", params.estimated_delivery_to);
  if (params.due_date_from) searchParams.append("due_date_from", params.due_date_from);
  if (params.due_date_to) searchParams.append("due_date_to", params.due_date_to);
  if (params.sort_by) searchParams.append("sort_by", params.sort_by);
  if (params.sort_order) searchParams.append("sort_order", params.sort_order);

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

export async function inactivateUser(token: string, userId: number): Promise<UserListItem> {
  return request<UserListItem>(`/users/${userId}/inactivate`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
}

// LOG-011: Listagem de entregas
export async function listDeliveries(token: string, params: DeliveryListParams = {}): Promise<DeliveryListResponse> {
  const searchParams = new URLSearchParams();
  if (params.page) searchParams.append("page", params.page.toString());
  if (params.page_size) searchParams.append("page_size", params.page_size.toString());
  if (params.nf) searchParams.append("nf", params.nf);
  if (params.transportadora) searchParams.append("transportadora", params.transportadora);
  if (params.data_coleta) searchParams.append("data_coleta", params.data_coleta);

  const query = searchParams.toString();
  return request<DeliveryListResponse>(`/imports/deliveries${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// LOG-012: Detalhe de entrega
export async function getDeliveryDetail(token: string, deliveryId: number): Promise<DeliveryDetail> {
  return request<DeliveryDetail>(`/imports/deliveries/${deliveryId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
