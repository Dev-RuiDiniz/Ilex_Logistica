import { describe, expect, it, vi, beforeEach } from "vitest";
import { listSlaRules, createSlaRule, updateSlaRule, recalculateSla } from "./api";

// Mock global fetch
global.fetch = vi.fn();

describe("SLA API client", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("listSlaRules chama endpoint correto", async () => {
    const mockResponse = [
      { id: 1, carrier_id: null, destination_uf: null, transit_days: 5, warning_threshold_days: 2, critical_delay_days: 3, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
    ];
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await listSlaRules("test-token");

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sla/rules"),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it("createSlaRule envia payload correto", async () => {
    const mockResponse = { id: 1, carrier_id: null, destination_uf: null, transit_days: 5, warning_threshold_days: 2, critical_delay_days: 3, is_active: true, created_at: "2025-01-01", updated_at: "2025-01-01" };
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const payload = {
      transit_days: 5,
      warning_threshold_days: 2,
      critical_delay_days: 3,
      carrier_id: null,
      destination_uf: null,
      is_active: true,
    };

    const result = await createSlaRule("test-token", payload);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sla/rules"),
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
        body: JSON.stringify(payload),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it("updateSlaRule envia payload correto", async () => {
    const mockResponse = { id: 1, carrier_id: null, destination_uf: null, transit_days: 5, warning_threshold_days: 2, critical_delay_days: 3, is_active: false, created_at: "2025-01-01", updated_at: "2025-01-01" };
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const payload = { is_active: false };

    const result = await updateSlaRule("test-token", 1, payload);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sla/rules/1"),
      expect.objectContaining({
        method: "PUT",
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
        body: JSON.stringify(payload),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it("disable/inactivate rule envia payload correto", async () => {
    const mockResponse = { id: 1, carrier_id: null, destination_uf: null, transit_days: 5, warning_threshold_days: 2, critical_delay_days: 3, is_active: false, created_at: "2025-01-01", updated_at: "2025-01-01" };
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const payload = { is_active: false };

    const result = await updateSlaRule("test-token", 1, payload);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sla/rules/1"),
      expect.objectContaining({
        method: "PUT",
        body: JSON.stringify(payload),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it("recalculateSla chama endpoint correto", async () => {
    const mockResponse = { processed_count: 100, updated_count: 50, skipped_count: 30, error_count: 20 };
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await recalculateSla("test-token");

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/sla/recalculate"),
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
    expect(result).toEqual(mockResponse);
  });

  it("erros de API são tratados", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      text: async () => "API Error",
    } as Response);

    await expect(listSlaRules("test-token")).rejects.toThrow();
  });
});
