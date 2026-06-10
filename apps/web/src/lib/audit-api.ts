import { request } from "./api";

export type AuditSeverity = "info" | "warning" | "critical";
export type AuditStatus = "success" | "failed" | "skipped";
export type AuditAction = "create" | "update" | "delete" | "read";

export interface AuditLog {
  id: number;
  event_type: string;
  entity_type: string;
  entity_id: number | null;
  action: string;
  actor_user_id: number | null;
  actor_email: string | null;
  source: string | null;
  severity: AuditSeverity;
  status: AuditStatus;
  message: string;
  before_json: string | null;
  after_json: string | null;
  metadata_json: string | null;
  request_id: string | null;
  ip_address: string | null;
  user_agent: string | null;
  created_at: string;
}

export interface AuditLogListResponse {
  logs: AuditLog[];
  total: number;
  page: number;
  page_size: number;
}

export interface AuditLogSummaryResponse {
  total_logs: number;
  success_count: number;
  failed_count: number;
  skipped_count: number;
  critical_count: number;
  warning_count: number;
  info_count: number;
  create_count: number;
  update_count: number;
  delete_count: number;
  read_count: number;
}

export interface AuditLogFilters {
  event_type?: string;
  entity_type?: string;
  entity_id?: number;
  action?: string;
  actor_user_id?: number;
  severity?: AuditSeverity;
  status?: AuditStatus;
  page?: number;
  page_size?: number;
}

export async function getAuditLogs(token: string, filters: AuditLogFilters = {}): Promise<AuditLogListResponse> {
  const searchParams = new URLSearchParams();
  
  if (filters.event_type) searchParams.append("event_type", filters.event_type);
  if (filters.entity_type) searchParams.append("entity_type", filters.entity_type);
  if (filters.entity_id) searchParams.append("entity_id", filters.entity_id.toString());
  if (filters.action) searchParams.append("action", filters.action);
  if (filters.actor_user_id) searchParams.append("actor_user_id", filters.actor_user_id.toString());
  if (filters.severity) searchParams.append("severity", filters.severity);
  if (filters.status) searchParams.append("status", filters.status);
  if (filters.page) searchParams.append("page", filters.page.toString());
  if (filters.page_size) searchParams.append("page_size", filters.page_size.toString());
  
  const query = searchParams.toString();
  return request<AuditLogListResponse>(`/audit${query ? `?${query}` : ""}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getAuditLogById(token: string, logId: number): Promise<AuditLog> {
  return request<AuditLog>(`/audit/${logId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function getAuditSummary(token: string): Promise<AuditLogSummaryResponse> {
  return request<AuditLogSummaryResponse>("/audit/summary", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
