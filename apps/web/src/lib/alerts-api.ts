export type AlertType = 'sla_critical' | 'sla_late' | 'sla_warning' | 'unknown_sla' | 'import_failure';

export type AlertSeverity = 'critical' | 'warning' | 'info';

export type AlertStatus = 'active' | 'read' | 'resolved' | 'dismissed';

export interface AlertItem {
  id: number;
  alert_type: AlertType;
  severity: AlertSeverity;
  title: string;
  message: string;
  source_type: string;
  source_id: number | null;
  shipment_id: number | null;
  carrier_id: number | null;
  status: AlertStatus;
  is_read: boolean;
  is_resolved: boolean;
  generated_at: string;
  read_at: string | null;
  resolved_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface AlertsSummary {
  total_alerts: number;
  active_count: number;
  read_count: number;
  resolved_count: number;
  critical_count: number;
  warning_count: number;
  info_count: number;
}

export interface AlertsFilters {
  status?: AlertStatus;
  severity?: AlertSeverity;
  alert_type?: AlertType;
  is_read?: boolean;
  is_resolved?: boolean;
  carrier_id?: number;
  shipment_id?: number;
  limit?: number;
  offset?: number;
}

export interface GenerateAlertsResponse {
  success: boolean;
  processed_count: number;
  created_count: number;
  skipped_count: number;
  resolved_count: number;
  error_count: number;
}

export interface MarkAlertReadResponse {
  success: boolean;
  message: string;
}

export interface ResolveAlertResponse {
  success: boolean;
  message: string;
}

export async function getAlerts(filters: AlertsFilters = {}): Promise<{ alerts: AlertItem[]; total: number }> {
  const params = new URLSearchParams();

  if (filters.status) params.append('status', filters.status);
  if (filters.severity) params.append('severity', filters.severity);
  if (filters.alert_type) params.append('alert_type', filters.alert_type);
  if (filters.is_read !== undefined) params.append('is_read', String(filters.is_read));
  if (filters.is_resolved !== undefined) params.append('is_resolved', String(filters.is_resolved));
  if (filters.carrier_id) params.append('carrier_id', String(filters.carrier_id));
  if (filters.shipment_id) params.append('shipment_id', String(filters.shipment_id));
  if (filters.limit) params.append('limit', String(filters.limit));
  if (filters.offset) params.append('offset', String(filters.offset));

  const queryString = params.toString();
  const url = `/api/v1/alerts${queryString ? `?${queryString}` : ''}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch alerts: ${response.status}`);
  }

  return response.json();
}

export async function getAlertsSummary(): Promise<AlertsSummary> {
  const response = await fetch('/api/v1/alerts/summary', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch alerts summary: ${response.status}`);
  }

  return response.json();
}

export async function generateAlerts(): Promise<GenerateAlertsResponse> {
  const response = await fetch('/api/v1/alerts/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to generate alerts: ${response.status}`);
  }

  return response.json();
}

export async function markAlertAsRead(alertId: number): Promise<MarkAlertReadResponse> {
  const response = await fetch(`/api/v1/alerts/${alertId}/read`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to mark alert as read: ${response.status}`);
  }

  return response.json();
}

export async function resolveAlert(alertId: number): Promise<ResolveAlertResponse> {
  const response = await fetch(`/api/v1/alerts/${alertId}/resolve`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to resolve alert: ${response.status}`);
  }

  return response.json();
}
