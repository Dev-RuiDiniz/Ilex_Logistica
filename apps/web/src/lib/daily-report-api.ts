import { buildApiUrl } from "@/lib/api";
import type {
  DailyReport,
  DailyReportAlertItem,
  DailyReportCarrierEfficiencyItem,
  DailyReportExceptionItem,
  DailyReportFilters,
  DailyReportGenerateRequest,
  DailyReportImportFailures,
  DailyReportKpis,
  DailyReportListResponse,
  DailyReportSummary,
  DailyReportExportRequest,
  DailyReportExportResponse,
} from "./types";

function authHeaders(token: string) {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

function buildReportsDailyUrl(path: string, query?: string): string {
  const normalizedPath = path.startsWith("/") ? path : path ? `/${path}` : "";
  return buildApiUrl(`/reports/daily${normalizedPath}${query ? `?${query}` : ""}`);
}

/**
 * Get daily reports with optional filters
 */
export async function getDailyReports(
  token: string,
  filters?: DailyReportFilters
): Promise<DailyReportListResponse> {
  const params = new URLSearchParams();

  if (filters?.date_from) params.append("date_from", filters.date_from);
  if (filters?.date_to) params.append("date_to", filters.date_to);
  if (filters?.status) params.append("status", filters.status);
  if (filters?.limit) params.append("limit", filters.limit.toString());
  if (filters?.offset) params.append("offset", filters.offset.toString());

  const queryString = params.toString();
  const url = buildReportsDailyUrl("", queryString);

  const response = await fetch(url, {
    method: "GET",
    headers: authHeaders(token),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch daily reports: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get daily report by ID
 */
export async function getDailyReportById(
  token: string,
  reportId: number
): Promise<DailyReport> {
  const response = await fetch(buildReportsDailyUrl(`/${reportId}`), {
    method: "GET",
    headers: authHeaders(token),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch daily report: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get daily report by date
 */
export async function getDailyReportByDate(
  token: string,
  reportDate: string
): Promise<DailyReport> {
  const response = await fetch(
    buildReportsDailyUrl(`/by-date/${reportDate}`),
    {
      method: "GET",
      headers: authHeaders(token),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch daily report by date: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Generate a daily report
 */
export async function generateDailyReport(
  token: string,
  payload: DailyReportGenerateRequest
): Promise<DailyReport> {
  const response = await fetch(buildReportsDailyUrl("/generate"), {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to generate daily report: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Parse summary JSON from daily report
 */
export function parseSummary(summaryJson: string): DailyReportSummary {
  try {
    return JSON.parse(summaryJson);
  } catch {
    // Silent error handling for production
    return {
      total_shipments: 0,
      on_time_count: 0,
      late_count: 0,
      critical_count: 0,
      warning_count: 0,
      unknown_sla_count: 0,
      exceptions_count: 0,
      import_failure_count: 0,
      carriers_count: 0,
    };
  }
}

/**
 * Parse KPIs JSON from daily report
 */
export function parseKpis(kpisJson: string): DailyReportKpis {
  try {
    return JSON.parse(kpisJson);
  } catch {
    // Silent error handling for production
    return {
      active_alerts_count: 0,
      delivery_rate: 0,
    };
  }
}

/**
 * Parse exceptions JSON from daily report
 */
export function parseExceptions(
  exceptionsJson: string
): DailyReportExceptionItem[] {
  try {
    return JSON.parse(exceptionsJson);
  } catch {
    // Silent error handling for production
    return [];
  }
}

/**
 * Parse alerts JSON from daily report
 */
export function parseAlerts(alertsJson: string): DailyReportAlertItem[] {
  try {
    return JSON.parse(alertsJson);
  } catch {
    // Silent error handling for production
    return [];
  }
}

/**
 * Parse carrier efficiency JSON from daily report
 */
export function parseCarrierEfficiency(
  carrierEfficiencyJson: string
): DailyReportCarrierEfficiencyItem[] {
  try {
    return JSON.parse(carrierEfficiencyJson);
  } catch {
    // Silent error handling for production
    return [];
  }
}

/**
 * Parse import failures JSON from daily report
 */
export function parseImportFailures(
  importFailuresJson: string
): DailyReportImportFailures {
  try {
    return JSON.parse(importFailuresJson);
  } catch {
    // Silent error handling for production
    return {
      rejected_count: 0,
    };
  }
}

/**
 * Export daily reports to CSV or JSON
 */
export async function exportDailyReports(
  token: string,
  payload: DailyReportExportRequest
): Promise<DailyReportExportResponse> {
  const response = await fetch(buildReportsDailyUrl("/export"), {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to export daily reports: ${response.statusText}`);
  }

  return response.json();
}
