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
}

export interface CSVRowError {
  row_number: number;
  field: string;
  message: string;
  value?: string;
}

export interface UploadResponse {
  import_id: number | null;
  status: "validated" | "failed";
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  errors: CSVRowError[];
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

// Daily Report types (BETA-018B)
export type DailyReportStatus = "pending" | "generating" | "generated" | "failed";

export interface DailyReportKpis {
  total_shipments?: number;
  total_exceptions?: number;
  avg_delay_days?: number;
  on_time_rate?: number;
  active_alerts_count?: number;
  delivery_rate?: number;
  [key: string]: any;
}

export interface DailyReportSummary {
  total_envios?: number;
  total_atrasos?: number;
  total_criticos?: number;
  percentual_atraso?: number;
  total_shipments?: number;
  on_time_count?: number;
  late_count?: number;
  critical_count?: number;
  exceptions_count?: number;
  import_failures_count?: number;
  [key: string]: any;
}

export interface DailyReportExceptionItem {
  shipment_id: number;
  tracking_code: string;
  carrier_name: string;
  status: string;
  delay_days: number;
  criticality: string;
  [key: string]: any;
}

export interface DailyReportAlertItem {
  id: number;
  type: string;
  message: string;
  severity: string;
  created_at: string;
  [key: string]: any;
}

export interface DailyReportCarrierEfficiencyItem {
  carrier_id: number;
  carrier_name: string;
  total_shipments: number;
  on_time_count: number;
  efficiency_rate: number;
  [key: string]: any;
}

export interface DailyReportImportFailures {
  total_imports?: number;
  failed_imports?: number;
  failure_rate?: number;
  top_errors?: Array<{ error: string; count: number }>;
  rejected_count?: number;
  [key: string]: any;
}

export interface DailyReport {
  id: number;
  report_date: string;
  status: DailyReportStatus;
  summary_json: string;
  kpis_json: string;
  exceptions_json: string;
  alerts_json: string;
  carrier_efficiency_json: string;
  import_failures_json: string;
  generated_at: string;
  period_start?: string;
  period_end?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface DailyReportFilters {
  date_from?: string;
  date_to?: string;
  status?: DailyReportStatus;
  limit?: number;
  offset?: number;
}

export interface DailyReportGenerateRequest {
  report_date: string;
  force_regenerate?: boolean;
}

export interface DailyReportListResponse {
  reports: DailyReport[];
  total: number;
  limit: number;
  offset: number;
}

// SLA Rule types (BETA-013A)
export interface SlaRule {
  id: number;
  carrier_id: number;
  destination_uf: string;
  transit_days: number;
  warning_threshold_days: number;
  critical_delay_days: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SlaRuleCreate {
  carrier_id: number | null;
  destination_uf: string | null;
  transit_days: number;
  warning_threshold_days: number;
  critical_delay_days: number;
  is_active?: boolean;
}

export interface SlaRuleUpdate {
  carrier_id?: number;
  destination_uf?: string;
  transit_days?: number;
  warning_threshold_days?: number;
  critical_delay_days?: number;
  is_active?: boolean;
}

export interface SlaRecalculateResponse {
  processed_count: number;
  updated_count: number;
  skipped_count: number;
  error_count: number;
}

// Import types (BETA-012A/B/C)
export interface RowValidationError {
  row_number: number;
  field: string;
  message: string;
  is_blocking?: boolean;
  value?: string | number | null;
  severity?: string;
}

export interface ValidatedRowData {
  row_number: number;
  data: {
    tracking_code?: string;
    invoice_number?: string;
    customer_name?: string;
    destination_uf?: string;
    collection_departure_date?: string;
    invoice_value?: number;
    freight_value?: number;
    freight_percentage?: number;
    carrier_name?: string;
    expected_delivery_date?: string;
    status?: string;
    [key: string]: any;
  };
}

export interface ImportPreviewV2Response {
  import_id: number;
  source: string | null;
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_count: number;
  duplicate_rows: number;
  preview_items: ValidatedRowData[];
  errors: RowValidationError[];
  warnings: RowValidationError[];
}

// Carrier Efficiency types (BETA-014A)
export interface CarrierEfficiencyFilters {
  carrier_id?: number;
  date_from?: string;
  date_to?: string;
  estimated_delivery_from?: string;
  estimated_delivery_to?: string;
  month?: number;
  year?: number;
  customer_name?: string;
  destination_uf?: string;
  status?: string;
  criticality?: string;
  sla_status?: string;
  is_late?: boolean;
}

export interface CarrierEfficiencyItem {
  carrier_id: number;
  carrier_name: string;
  total_invoices: number;
  total_shipments: number;
  on_time_percentage: number;
  late_percentage: number;
  total_freight_value: number;
  average_freight_percentage: number;
  ranking_by_efficiency: number;
  ranking_by_cost: number;
  ranking_by_volume: number;
}

export interface CarrierEfficiencyResponse {
  carriers: CarrierEfficiencyItem[];
}
