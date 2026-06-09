import { describe, it, expect, vi, beforeEach } from "vitest";
import { getCarrierEfficiency } from "./api";

describe("getCarrierEfficiency", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("Deve chamar endpoint correto", async () => {
    const mockResponse = {
      carriers: [],
      generated_at: "2025-01-01T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getCarrierEfficiency("test-token");

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/shipments/analytics/carrier-efficiency"),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
  });

  it("Deve enviar query params de filtros", async () => {
    const mockResponse = {
      carriers: [],
      generated_at: "2025-01-01T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getCarrierEfficiency("test-token", {
      month: 1,
      year: 2025,
      customer_name: "Cliente X",
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("month=1"),
      expect.any(Object)
    );
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("year=2025"),
      expect.any(Object)
    );
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("customer_name=Cliente+X"),
      expect.any(Object)
    );
  });

  it("Deve omitir filtros vazios", async () => {
    const mockResponse = {
      carriers: [],
      generated_at: "2025-01-01T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getCarrierEfficiency("test-token", {
      month: undefined,
      year: undefined,
      customer_name: "",
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/shipments/analytics/carrier-efficiency"),
      expect.any(Object)
    );
  });

  it("Deve serializar boolean is_late corretamente", async () => {
    const mockResponse = {
      carriers: [],
      generated_at: "2025-01-01T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getCarrierEfficiency("test-token", {
      is_late: true,
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("is_late=true"),
      expect.any(Object)
    );
  });

  it("Deve tratar resposta", async () => {
    const mockResponse = {
      carriers: [
        {
          carrier_id: 1,
          carrier_name: "Transportadora A",
          total_invoices: 10,
          total_shipments: 10,
          on_time_count: 8,
          on_time_percentage: 80,
          late_count: 2,
          late_percentage: 20,
          critical_count: 0,
          lost_count: 0,
          lost_percentage: 0,
          total_freight_value: 1000,
          total_invoice_value: 10000,
          average_freight_percentage: 10,
          average_freight_value: 100,
          ranking_by_efficiency: 1,
          ranking_by_cost: 1,
          ranking_by_volume: 1,
        },
      ],
      generated_at: "2025-01-01T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getCarrierEfficiency("test-token");

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/shipments/analytics/carrier-efficiency"),
      expect.any(Object)
    );
  });

  it("Deve tratar erro", async () => {
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      text: async () => "Erro de API",
    });

    await expect(getCarrierEfficiency("test-token")).rejects.toThrow("Erro de API");
  });
});
