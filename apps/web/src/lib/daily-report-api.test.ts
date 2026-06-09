import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  getDailyReports,
  getDailyReportById,
  getDailyReportByDate,
  generateDailyReport,
  parseSummary,
  parseKpis,
  parseExceptions,
  parseAlerts,
  parseCarrierEfficiency,
  parseImportFailures,
} from "./daily-report-api";

describe("daily-report-api", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn() as ReturnType<typeof vi.fn>;
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

      const result = await getDailyReports();

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
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

      await getDailyReports(filters);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily?date_from=2025-01-01&date_to=2025-01-31&status=generated",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
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

      await getDailyReports(filters);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Internal Server Error",
      });

      await expect(getDailyReports()).rejects.toThrow(
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

      const result = await getDailyReportById(1);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/1",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Not Found",
      });

      await expect(getDailyReportById(999)).rejects.toThrow(
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

      const result = await getDailyReportByDate("2025-01-21");

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/by-date/2025-01-21",
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Not Found",
      });

      await expect(getDailyReportByDate("2025-01-21")).rejects.toThrow(
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

      const result = await generateDailyReport(payload);

      expect(global.fetch).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/reports/daily/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );
      expect(result).toEqual(mockReport);
    });

    it("should handle API errors", async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        statusText: "Bad Request",
      });

      await expect(
        generateDailyReport({ report_date: "2025-01-21" })
      ).rejects.toThrow("Failed to generate daily report: Bad Request");
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
      const exceptionsJson = JSON.stringify([
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF001",
          carrier_id: 1,
          carrier_name: "Carrier A",
          customer_name: "Customer A",
          destination_uf: "SP",
          status: "late",
          sla_status: "late",
          criticality: "high",
          delay_days: 5,
          sla_due_date: "2025-01-15",
          exception_type: "delay",
          exception_reason: "Delivery delay",
          priority: 1,
          last_update_at: "2025-01-20",
        },
      ]);

      const result = parseExceptions(exceptionsJson);

      expect(result).toHaveLength(1);
      expect(result[0].shipment_id).toBe(1);
      expect(result[0].tracking_code).toBe("ABC123");
    });

    it("should return empty array on parse error", () => {
      const result = parseExceptions("invalid json");

      expect(result).toEqual([]);
    });
  });

  describe("parseAlerts", () => {
    it("should parse valid JSON", () => {
      const alertsJson = JSON.stringify([
        {
          id: 1,
          alert_type: "sla_critical",
          severity: "critical",
          title: "Critical SLA",
          message: "Shipment is critically late",
          source_type: "shipment",
          source_id: 1,
          shipment_id: 1,
          carrier_id: 1,
          status: "active",
          is_read: false,
          is_resolved: false,
          generated_at: "2025-01-20",
        },
      ]);

      const result = parseAlerts(alertsJson);

      expect(result).toHaveLength(1);
      expect(result[0].id).toBe(1);
      expect(result[0].alert_type).toBe("sla_critical");
    });

    it("should return empty array on parse error", () => {
      const result = parseAlerts("invalid json");

      expect(result).toEqual([]);
    });
  });

  describe("parseCarrierEfficiency", () => {
    it("should parse valid JSON", () => {
      const carrierEfficiencyJson = JSON.stringify([
        {
          carrier_id: 1,
          carrier_name: "Carrier A",
          total_shipments: 100,
          on_time_count: 80,
          late_count: 20,
          efficiency: 0.8,
          avg_cost: 50.0,
        },
      ]);

      const result = parseCarrierEfficiency(carrierEfficiencyJson);

      expect(result).toHaveLength(1);
      expect(result[0].carrier_id).toBe(1);
      expect(result[0].carrier_name).toBe("Carrier A");
    });

    it("should return empty array on parse error", () => {
      const result = parseCarrierEfficiency("invalid json");

      expect(result).toEqual([]);
    });
  });

  describe("parseImportFailures", () => {
    it("should parse valid JSON", () => {
      const importFailuresJson = JSON.stringify({
        rejected_count: 5,
      });

      const result = parseImportFailures(importFailuresJson);

      expect(result).toEqual({
        rejected_count: 5,
      });
    });

    it("should return default values on parse error", () => {
      const result = parseImportFailures("invalid json");

      expect(result).toEqual({
        rejected_count: 0,
      });
    });
  });
});
