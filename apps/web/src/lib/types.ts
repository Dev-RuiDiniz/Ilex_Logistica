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
