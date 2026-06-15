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

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";

/**
 * Get daily reports with optional filters
 */
export async function getDailyReports(
  filters?: DailyReportFilters
): Promise<DailyReportListResponse> {
  const params = new URLSearchParams();

  if (filters?.date_from) params.append("date_from", filters.date_from);
  if (filters?.date_to) params.append("date_to", filters.date_to);
  if (filters?.status) params.append("status", filters.status);
  if (filters?.limit) params.append("limit", filters.limit.toString());
  if (filters?.offset) params.append("offset", filters.offset.toString());

  const queryString = params.toString();
  const url = `${API_BASE}/reports/daily${queryString ? `?${queryString}` : ""}`;

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
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
  reportId: number
): Promise<DailyReport> {
  const response = await fetch(`${API_BASE}/reports/daily/${reportId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
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
  reportDate: string
): Promise<DailyReport> {
  const response = await fetch(
    `${API_BASE}/reports/daily/by-date/${reportDate}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
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
  payload: DailyReportGenerateRequest
): Promise<DailyReport> {
  const response = await fetch(`${API_BASE}/reports/daily/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
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
  } catch (error) {
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
  } catch (error) {
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
  } catch (error) {
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
  } catch (error) {
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
  } catch (error) {
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
  } catch (error) {
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
  payload: DailyReportExportRequest
): Promise<DailyReportExportResponse> {
  const response = await fetch(`${API_BASE}/reports/daily/export`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Failed to export daily reports: ${response.statusText}`);
  }

  return response.json();
}
