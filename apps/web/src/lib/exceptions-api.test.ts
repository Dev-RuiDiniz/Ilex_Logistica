import { describe, it, expect, vi, beforeEach } from "vitest";
import { getExceptionsPanel } from "./exceptions-api";

describe("Exceptions API", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("Deve chamar endpoint correto", async () => {
    const mockResponse = {
      summary: { total_exceptions: 10, critical_count: 2, late_count: 5, warning_count: 2, unknown_sla_count: 1 },
      items: [],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getExceptionsPanel("test-token");

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/shipments/analytics/exceptions"),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
  });

  it("Deve enviar query params corretamente", async () => {
    const mockResponse = {
      summary: { total_exceptions: 10, critical_count: 2, late_count: 5, warning_count: 2, unknown_sla_count: 1 },
      items: [],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getExceptionsPanel("test-token", {
      carrier_id: 1,
      destination_uf: "SP",
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("carrier_id=1"),
      expect.any(Object)
    );
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("destination_uf=SP"),
      expect.any(Object)
    );
  });

  it("Deve omitir filtros vazios", async () => {
    const mockResponse = {
      summary: { total_exceptions: 10, critical_count: 2, late_count: 5, warning_count: 2, unknown_sla_count: 1 },
      items: [],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getExceptionsPanel("test-token", {
      carrier_id: undefined,
      destination_uf: "",
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/shipments/analytics/exceptions"),
      expect.any(Object)
    );
  });

  it("Deve serializar boolean is_late corretamente", async () => {
    const mockResponse = {
      summary: { total_exceptions: 10, critical_count: 2, late_count: 5, warning_count: 2, unknown_sla_count: 1 },
      items: [],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    await getExceptionsPanel("test-token", {
      is_late: true,
    });

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("is_late=true"),
      expect.any(Object)
    );
  });

  it("Deve tratar erro de API", async () => {
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: false,
      text: async () => "API Error",
    });

    await expect(getExceptionsPanel("test-token")).rejects.toThrow("API Error");
  });
});
