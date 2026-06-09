/* eslint-disable @typescript-eslint/no-explicit-any */
import { describe, it, expect, vi, beforeEach } from "vitest";
import { getDashboardSummary, type DashboardFilters } from "./dashboard-api";

// Mock global fetch
global.fetch = vi.fn() as any;

describe("dashboard-api", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("deve chamar endpoint correto", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    } as Response);

    await getDashboardSummary("test-token");

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/dashboard/summary"),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
  });

  it("deve enviar query params corretamente", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    } as Response);

    const filters: DashboardFilters = {
      month: 1,
      year: 2025,
      customer_name: "Test",
      destination_uf: "SP",
    };

    await getDashboardSummary("test-token", filters);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("month=1&year=2025&customer_name=Test&destination_uf=SP"),
      expect.any(Object)
    );
  });

  it("deve omitir filtros vazios", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    } as Response);

    const filters: DashboardFilters = {
      customer_name: "",
      destination_uf: "",
    };

    await getDashboardSummary("test-token", filters);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/dashboard/summary"),
      expect.any(Object)
    );
  });

  it("deve serializar boolean is_late corretamente", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    } as Response);

    const filters: DashboardFilters = {
      is_late: true,
    };

    await getDashboardSummary("test-token", filters);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("is_late=true"),
      expect.any(Object)
    );
  });

  it("deve tratar erro de API", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: false,
      text: async () => "API Error",
    } as Response);

    await expect(getDashboardSummary("test-token")).rejects.toThrow("API Error");
  });

  it("deve parseia resposta com KPIs, top transportadoras e top exceções", async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        total_shipments: 100,
        on_time_count: 80,
        late_count: 15,
        critical_count: 3,
        warning_count: 2,
        unknown_sla_count: 0,
        resolved_count: 0,
        no_update_count: 0,
        exceptions_count: 20,
        import_failure_count: 5,
        active_alerts_count: 0,
        carriers_count: 10,
        top_carriers_by_efficiency: [
          {
            carrier_id: 1,
            carrier_name: "Transportadora A",
            total_shipments: 50,
            on_time_count: 45,
            late_count: 5,
            critical_count: 0,
            lost_count: 0,
            total_freight_value: 500,
            total_invoice_value: 5000,
            on_time_percentage: 90,
            late_percentage: 10,
            lost_percentage: 0,
            average_freight_percentage: 10,
            average_freight_value: 10,
            ranking_by_efficiency: 1,
            ranking_by_cost: 1,
            ranking_by_volume: 1,
          },
        ],
        top_exceptions: [
          {
            shipment_id: 1,
            tracking_code: "ABC123",
            invoice_number: "NF123",
            carrier_id: 1,
            carrier_name: "Transportadora A",
            customer_name: "Cliente X",
            destination_uf: "SP",
            status: "in_transit",
            sla_status: "critical",
            criticality: "alta",
            delay_days: 15,
            sla_due_date: "2025-01-01T00:00:00Z",
            exception_type: "critical",
            exception_reason: "critical - critical",
            priority: 1,
            last_update_at: "2025-01-15T00:00:00Z",
          },
        ],
        generated_at: "2025-01-15T00:00:00Z",
        filters_applied: {},
      }),
    } as Response);

    const result = await getDashboardSummary("test-token");

    expect(result.total_shipments).toBe(100);
    expect(result.on_time_count).toBe(80);
    expect(result.top_carriers_by_efficiency).toHaveLength(1);
    expect(result.top_exceptions).toHaveLength(1);
  });
});
/* eslint-enable @typescript-eslint/no-explicit-any */
