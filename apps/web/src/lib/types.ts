export type UserRole = "admin" | "logistica" | "gestor" | "auditoria";

export interface SessionData {
  accessToken: string;
  refreshToken: string;
  role: UserRole;
  email: string;
}

export interface Carrier {
  id: number;
  name: string;
  external_code?: string | null;
  integration_metadata: Record<string, unknown>;
  is_active: boolean;
}

// Shipment types
export interface Shipment {
  id: number;
  tracking_code: string;
  carrier_id: number;
  status: string;
  estimated_delivery: string;
  actual_delivery: string | null;
  recipient_name: string;
  recipient_phone: string;
  origin_address: string;
  destination_address: string;
  meta_data: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  invoice_number: string | null;
  invoice_key: string | null;
  fiscal_document: string | null;
  amount: number | null;
  due_date: string | null;
  delay_days: number;
  criticality: string;
  freight_value: number | null;
  invoice_value: number | null;
  freight_percentage: number | null;
  collection_departure_date: string | null;
  customer_name: string | null;
  destination_uf: string | null;
  // BETA-013A: SLA fields (calculados on-demand)
  sla_due_date: string | null;
  sla_status: string | null;
  is_late: boolean;
  sla_rule_id: number | null;
}

export interface CSVRowError {
  row_number: number;
  field: string;
  message: string;
  value?: string;
}

// BETA-012A: Enhanced error type with severity
export interface RowValidationError {
  row_number: number;
  field: string;
  message: string;
  value?: string;
  severity: "error" | "warning";
  is_blocking: boolean;
}

export interface UploadResponse {
  import_id: number | null;
  status: "validated" | "failed";
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  errors: CSVRowError[];
}

// BETA-012A: Validated row data for preview
export interface ValidatedRowData {
  row_number: number;
  data: {
    tracking_code: string;
    carrier_id: number;
    invoice_number: string;
    invoice_value: number;
    freight_value: number;
    collection_departure_date: string;
    customer_name: string;
    destination_uf: string;
  };
}

// BETA-012A: Preview response with enhanced error handling
export interface ImportPreviewV2Response {
  import_id: number;
  filename: string;
  file_type: string;
  file_hash: string;
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_rows: number;
  preview_items: ValidatedRowData[];
  errors: RowValidationError[];
  warnings: RowValidationError[];
  source?: string; // BETA-012C: Import source identifier
}

export interface ImportConfirmRequest {
  import_id: number;
  confirm: boolean;
}

export interface ImportConfirmResponse {
  import_id: number;
  status: "completed" | "failed";
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  imported_count: number;
  rejected_count: number;
  duplicates_count: number;
  created_shipments: number[];
  errors: CSVRowError[];
}

// Shipment list types
export interface ShipmentListParams {
  page?: number;
  page_size?: number;
  status?: string;
  carrier_id?: number;
  tracking_code?: string;
  invoice_number?: string;
  fiscal_document?: string;
  criticality?: string;
  estimated_delivery_from?: string;
  estimated_delivery_to?: string;
  due_date_from?: string;
  due_date_to?: string;
  sort_by?: string;
  sort_order?: string;
  customer_name?: string;
  destination_uf?: string;
  month?: number;
  year?: number;
  search?: string;
  // BETA-013A: SLA filters
  sla_status?: string;
  is_late?: boolean;
}

export interface ShipmentListResponse {
  items: Shipment[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export type ExceptionShipmentListResponse = ShipmentListResponse;
export type ShipmentDetail = Shipment;

export interface ShipmentTreatment {
  id: number;
  shipment_id: number;
  status: string;
  comment: string;
  created_by: number;
  created_at: string;
}

export interface CreateShipmentTreatmentRequest {
  status: string;
  comment: string;
}

export interface DailyReportResponse {
  report_date: string;
  total_shipments: number;
  total_exceptions: number;
  by_criticality: Record<string, number>;
  by_carrier: Array<{ carrier_id: number; count: number }>;
}

export interface UserListItem {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  roles: UserRole[];
}

// Delivery types (LOG-011)
export interface DeliveryListItem {
  id: number;
  nf: string;
  transportadora: string;
  data_coleta: string;
  valor_frete: number;
  percentual_frete: number;
  created_at: string;
}

export interface DeliveryListParams {
  page?: number;
  page_size?: number;
  nf?: string;
  transportadora?: string;
  data_coleta?: string;
}

export interface DeliveryListResponse {
  items: DeliveryListItem[];
  total: number;
  page: number;
  page_size: number;
}

// Delivery detail (LOG-012)
export interface DeliveryDetail {
  id: number;
  nf: string;
  transportadora: string;
  data_coleta: string;
  valor_frete: number;
  percentual_frete: number;
  created_at: string;
}

// Promote Delivery to Shipment (LOG-022)
export interface PromoteDeliveryRequest {
  tracking_code: string;
  carrier_id: number;
  estimated_delivery: string;
  recipient_name: string;
  recipient_phone: string;
  origin_address: string;
  destination_address: string;
  shipment_status?: string;
}

export interface PromoteDeliveryResponse {
  id: number;
  tracking_code: string;
  carrier_id: number;
  status: string;
  estimated_delivery: string;
  recipient_name: string;
  recipient_phone: string;
  origin_address: string;
  destination_address: string;
  amount: number | null;
  invoice_number: string | null;
  created_at: string;
  updated_at: string;
}

// BETA-013A: SLA Rule types
export interface SlaRule {
  id: number;
  carrier_id: number | null;
  destination_uf: string | null;
  transit_days: number;
  warning_threshold_days: number;
  critical_delay_days: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SlaRuleCreate {
  carrier_id?: number | null;
  destination_uf?: string | null;
  transit_days: number;
  warning_threshold_days: number;
  critical_delay_days: number;
  is_active?: boolean;
}

export interface SlaRuleUpdate {
  carrier_id?: number | null;
  destination_uf?: string | null;
  transit_days?: number | null;
  warning_threshold_days?: number | null;
  critical_delay_days?: number | null;
  is_active?: boolean | null;
}

export interface SlaRecalculateResponse {
  processed_count: number;
  updated_count: number;
  skipped_count: number;
  error_count: number;
}

// BETA-014B: Carrier Efficiency types
export interface CarrierEfficiencyMetrics {
  carrier_id: number;
  carrier_name: string | null;
  total_invoices: number;
  total_shipments: number;
  on_time_count: number;
  on_time_percentage: number;
  late_count: number;
  late_percentage: number;
  critical_count: number;
  lost_count: number;
  lost_percentage: number;
  total_freight_value: number;
  total_invoice_value: number;
  average_freight_percentage: number;
  average_freight_value: number;
  ranking_by_efficiency: number;
  ranking_by_cost: number;
  ranking_by_volume: number;
}

export interface CarrierEfficiencyResponse {
  carriers: CarrierEfficiencyMetrics[];
  generated_at: string;
}

export interface CarrierEfficiencyFilters {
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
}

// BETA-015A: Exceptions Panel types
export interface ExceptionPanelFilters {
  carrier_id?: number;
  destination_uf?: string;
  customer_name?: string;
  criticality?: string;
  sla_status?: string;
  is_late?: boolean;
  exception_type?: string;
}

export interface ExceptionPanelResponse {
  items: ExceptionPanelItem[];
  summary: ExceptionPanelSummary;
  generated_at: string;
  filters_applied: ExceptionPanelFilters;
}

export interface ExceptionPanelItem {
  shipment_id: number;
  tracking_code: string;
  invoice_number: string | null;
  carrier_id: number | null;
  carrier_name: string | null;
  customer_name: string | null;
  destination_uf: string | null;
  status: string | null;
  sla_status: string | null;
  criticality: string | null;
  delay_days: number;
  sla_due_date: string | null;
  exception_type: string | null;
  exception_reason: string | null;
  priority: number;
  last_update_at: string | null;
}

export interface ExceptionPanelSummary {
  total_critical: number;
  total_late: number;
  total_warning: number;
  total_unknown: number;
  by_exception_type: Record<string, number>;
}

// BETA-016A: Dashboard types
export interface DashboardSummary {
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  critical_count: number;
  warning_count: number;
  unknown_sla_count: number;
  exceptions_count: number;
  active_alerts_count: number;
  import_failure_count: number;
  top_carriers_by_efficiency: CarrierEfficiencyMetrics[];
  top_exceptions: ExceptionPanelItem[];
  generated_at: string;
  filters_applied: DashboardFilters;
}

export interface DashboardFilters {
  period_from?: string;
  period_to?: string;
  month?: number;
  year?: number;
  customer_name?: string;
  destination_uf?: string;
  carrier_id?: number;
  criticality?: string;
  sla_status?: string;
  is_late?: boolean;
  exception_type?: string;
}

// BETA-017A: Alerts types
export type AlertSeverity = "critical" | "high" | "medium" | "low";
export type AlertStatus = "active" | "resolved" | "archived";
export type AlertType = "sla_critical" | "sla_late" | "sla_warning" | "import_failure" | "system_error";

export interface Alert {
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
  created_at: string;
  updated_at: string;
}

export interface AlertFilters {
  status?: AlertStatus;
  severity?: AlertSeverity;
  alert_type?: AlertType;
  limit?: number;
  offset?: number;
}

export interface AlertSummary {
  total_alerts: number;
  active_alerts: number;
  resolved_alerts: number;
  by_severity: Record<AlertSeverity, number>;
  by_type: Record<AlertType, number>;
}

export interface AlertGenerateResponse {
  total_alerts: number;
  new_alerts: number;
  by_severity: Record<AlertSeverity, number>;
  by_type: Record<AlertType, number>;
}

// BETA-018B: Daily Report types
export type DailyReportStatus = "generated" | "failed" | "stale" | "archived";

export interface DailyReportSummary {
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  critical_count: number;
  warning_count: number;
  unknown_sla_count: number;
  exceptions_count: number;
  import_failure_count: number;
  carriers_count: number;
}

export interface DailyReportKpis {
  active_alerts_count: number;
  delivery_rate: number;
}

export interface DailyReportExceptionItem {
  shipment_id: number;
  tracking_code: string;
  invoice_number: string | null;
  carrier_id: number | null;
  carrier_name: string | null;
  customer_name: string | null;
  destination_uf: string | null;
  status: string | null;
  sla_status: string | null;
  criticality: string | null;
  delay_days: number;
  sla_due_date: string | null;
  exception_type: string | null;
  exception_reason: string | null;
  priority: number;
  last_update_at: string | null;
}

export interface DailyReportAlertItem {
  id: number;
  alert_type: string;
  severity: string;
  title: string;
  message: string;
  source_type: string;
  source_id: number | null;
  shipment_id: number | null;
  carrier_id: number | null;
  status: string;
  is_read: boolean;
  is_resolved: boolean;
  generated_at: string;
}

export interface DailyReportCarrierEfficiencyItem {
  carrier_id: number;
  carrier_name: string;
  total_shipments: number;
  on_time_count: number;
  late_count: number;
  efficiency: number;
  avg_cost: number | null;
}

export interface DailyReportImportFailures {
  rejected_count: number;
}

export interface DailyReport {
  id: number;
  report_date: string;
  status: DailyReportStatus;
  generated_at: string;
  generated_by_user_id: number | null;
  period_start: string | null;
  period_end: string | null;
  summary_json: string;
  kpis_json: string;
  exceptions_json: string;
  alerts_json: string;
  carrier_efficiency_json: string;
  import_failures_json: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface DailyReportListResponse {
  reports: DailyReport[];
  total: number;
  limit: number;
  offset: number;
}

export interface DailyReportGenerateRequest {
  report_date: string;
  period_start?: string;
  period_end?: string;
  generated_by_user_id?: number;
}

export interface DailyReportFilters {
  date_from?: string;
  date_to?: string;
  status?: DailyReportStatus;
  limit?: number;
  offset?: number;
}
