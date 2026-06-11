import { afterEach, describe, expect, it, vi } from "vitest";
import { listShipments } from "@/lib/api";
import { ApiError } from "@/lib/api";

vi.mock("@/lib/error-handler", () => ({
  handleApiError: vi.fn((err) => {
    if (err instanceof ApiError && err.status === 401) {
      return "Sessão expirada. Redirecionando para login...";
    }
    if (err instanceof ApiError && err.status === 403) {
      return "Você não tem permissão para acessar este recurso.";
    }
    return err instanceof Error ? err.message : "Erro desconhecido";
  }),
}));

describe("Shipments API — Tratamento 401/403", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("trata 401 no listShipments", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: async () => ({ detail: "Unauthorized" }),
    });
    global.fetch = mockFetch;

    await expect(listShipments("token", {})).rejects.toThrow();
  });

  it("trata 403 no listShipments", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      json: async () => ({ detail: "Forbidden" }),
    });
    global.fetch = mockFetch;

    await expect(listShipments("token", {})).rejects.toThrow();
  });
});
