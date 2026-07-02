import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  getDailyReports,
  getDailyReportById,
  getDailyReportByDate,
  generateDailyReport,
  exportDailyReports,
  parseSummary,
  parseKpis,
  parseExceptions,
  parseAlerts,
  parseCarrierEfficiency,
  parseImportFailures,
} from "./daily-report-api";

const token = "test-token";

describe("daily-report-api", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.stubGlobal("fetch", vi.fn());
    vi.stubEnv("NEXT_PUBLIC_API_URL", "http://localhost:8000/api/v1");
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  const expectAuthHeaders = () =>
    expect.objectContaining({
      method: expect.any(String),
      headers: expect.objectContaining({
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      }),
    });

  describe("getDailyReports", () => {
    it("should call the correct endpoint without filters", async () => {
      const mockResponse = {
        reports: [],
        total: 0,
        limit: 10,
        offset: 0,
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await getDailyReports(token);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily",
        expectAuthHeaders()
      );
      expect(result).toEqual(mockResponse);
    });

    it("should send date_from/date_to/status filters when provided", async () => {
      const mockResponse = {
        reports: [],
        total: 0,
        limit: 10,
        offset: 0,
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const filters = {
        date_from: "2025-01-01",
        date_to: "2025-01-31",
        status: "generated" as const,
      };

      await getDailyReports(token, filters);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily?date_from=2025-01-01&date_to=2025-01-31&status=generated",
        expectAuthHeaders()
      );
    });

    it("should omit empty filters", async () => {
      const mockResponse = {
        reports: [],
        total: 0,
        limit: 10,
        offset: 0,
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const filters = {
        date_from: undefined,
        date_to: undefined,
        status: undefined,
      };

      await getDailyReports(token, filters);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily",
        expectAuthHeaders()
      );
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Internal Server Error",
      });

      await expect(getDailyReports(token)).rejects.toThrow(
        "Failed to fetch daily reports: Internal Server Error"
      );
    });
  });

  describe("getDailyReportById", () => {
    it("should call the correct endpoint", async () => {
      const mockReport = {
        id: 1,
        report_date: "2025-01-21",
        status: "generated" as const,
        generated_at: "2025-01-21T10:00:00Z",
        generated_by_user_id: null,
        period_start: null,
        period_end: null,
        summary_json: "{}",
        kpis_json: "{}",
        exceptions_json: "[]",
        alerts_json: "[]",
        carrier_efficiency_json: "[]",
        import_failures_json: "{}",
        notes: null,
        created_at: "2025-01-21T10:00:00Z",
        updated_at: "2025-01-21T10:00:00Z",
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockReport,
      });

      const result = await getDailyReportById(token, 1);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/1",
        expectAuthHeaders()
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Not Found",
      });

      await expect(getDailyReportById(token, 999)).rejects.toThrow(
        "Failed to fetch daily report: Not Found"
      );
    });
  });

  describe("getDailyReportByDate", () => {
    it("should call the correct endpoint", async () => {
      const mockReport = {
        id: 1,
        report_date: "2025-01-21",
        status: "generated" as const,
        generated_at: "2025-01-21T10:00:00Z",
        generated_by_user_id: null,
        period_start: null,
        period_end: null,
        summary_json: "{}",
        kpis_json: "{}",
        exceptions_json: "[]",
        alerts_json: "[]",
        carrier_efficiency_json: "[]",
        import_failures_json: "{}",
        notes: null,
        created_at: "2025-01-21T10:00:00Z",
        updated_at: "2025-01-21T10:00:00Z",
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockReport,
      });

      const result = await getDailyReportByDate(token, "2025-01-21");

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/by-date/2025-01-21",
        expectAuthHeaders()
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Not Found",
      });

      await expect(getDailyReportByDate(token, "2025-01-21")).rejects.toThrow(
        "Failed to fetch daily report by date: Not Found"
      );
    });
  });

  describe("generateDailyReport", () => {
    it("should call the correct endpoint", async () => {
      const mockReport = {
        id: 1,
        report_date: "2025-01-21",
        status: "generated" as const,
        generated_at: "2025-01-21T10:00:00Z",
        generated_by_user_id: null,
        period_start: null,
        period_end: null,
        summary_json: "{}",
        kpis_json: "{}",
        exceptions_json: "[]",
        alerts_json: "[]",
        carrier_efficiency_json: "[]",
        import_failures_json: "{}",
        notes: null,
        created_at: "2025-01-21T10:00:00Z",
        updated_at: "2025-01-21T10:00:00Z",
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockReport,
      });

      const payload = {
        report_date: "2025-01-21",
      };

      const result = await generateDailyReport(token, payload);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/generate",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          }),
          body: JSON.stringify(payload),
        })
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Bad Request",
      });

      await expect(
        generateDailyReport(token, { report_date: "2025-01-21" })
      ).rejects.toThrow("Failed to generate daily report: Bad Request");
    });
  });

  describe("exportDailyReports", () => {
    it("should call the correct endpoint", async () => {
      const mockResponse = {
        content: "csv,content",
        filename: "reports.csv",
        media_type: "text/csv",
      };
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const payload = { format: "csv" as const };
      const result = await exportDailyReports(token, payload);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/export",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          }),
          body: JSON.stringify(payload),
        })
      );
      expect(result).toEqual(mockResponse);
    });
  });

  describe("parseSummary", () => {
    it("should parse valid JSON", () => {
      const summaryJson = JSON.stringify({
        total_shipments: 100,
        on_time_count: 80,
        late_count: 15,
        critical_count: 3,
        warning_count: 2,
        unknown_sla_count: 0,
        exceptions_count: 20,
        import_failure_count: 0,
        carriers_count: 5,
      });

      const result = parseSummary(summaryJson);

      expect(result).toEqual({
        total_shipments: 100,
        on_time_count: 80,
        late_count: 15,
        critical_count: 3,
        warning_count: 2,
        unknown_sla_count: 0,
        exceptions_count: 20,
        import_failure_count: 0,
        carriers_count: 5,
      });
    });

    it("should return default values on parse error", () => {
      const result = parseSummary("invalid json");

      expect(result).toEqual({
        total_shipments: 0,
        on_time_count: 0,
        late_count: 0,
        critical_count: 0,
        warning_count: 0,
        unknown_sla_count: 0,
        exceptions_count: 0,
        import_failure_count: 0,
        carriers_count: 0,
      });
    });
  });

  describe("parseKpis", () => {
    it("should parse valid JSON", () => {
      const kpisJson = JSON.stringify({
        active_alerts_count: 5,
        delivery_rate: 0.8,
      });

      const result = parseKpis(kpisJson);

      expect(result).toEqual({
        active_alerts_count: 5,
        delivery_rate: 0.8,
      });
    });

    it("should return default values on parse error", () => {
      const result = parseKpis("invalid json");

      expect(result).toEqual({
        active_alerts_count: 0,
        delivery_rate: 0,
      });
    });
  });

  describe("parseExceptions", () => {
    it("should parse valid JSON", () => {
      const exceptionsJson = JSON.stringify([{ id: 1, description: "Test" }]);
      const result = parseExceptions(exceptionsJson);
      expect(result).toEqual([{ id: 1, description: "Test" }]);
    });

    it("should return empty array on parse error", () => {
      const result = parseExceptions("invalid json");
      expect(result).toEqual([]);
    });
  });

  describe("parseAlerts", () => {
    it("should parse valid JSON", () => {
      const alertsJson = JSON.stringify([{ id: 1, message: "Test" }]);
      const result = parseAlerts(alertsJson);
      expect(result).toEqual([{ id: 1, message: "Test" }]);
    });

    it("should return empty array on parse error", () => {
      const result = parseAlerts("invalid json");
      expect(result).toEqual([]);
    });
  });

  describe("parseCarrierEfficiency", () => {
    it("should parse valid JSON", () => {
      const json = JSON.stringify([{ carrier_id: 1, efficiency: 0.9 }]);
      const result = parseCarrierEfficiency(json);
      expect(result).toEqual([{ carrier_id: 1, efficiency: 0.9 }]);
    });

    it("should return empty array on parse error", () => {
      const result = parseCarrierEfficiency("invalid json");
      expect(result).toEqual([]);
    });
  });

  describe("parseImportFailures", () => {
    it("should parse valid JSON", () => {
      const json = JSON.stringify({ rejected_count: 3 });
      const result = parseImportFailures(json);
      expect(result).toEqual({ rejected_count: 3 });
    });

    it("should return default values on parse error", () => {
      const result = parseImportFailures("invalid json");
      expect(result).toEqual({ rejected_count: 0 });
    });
  });
});
