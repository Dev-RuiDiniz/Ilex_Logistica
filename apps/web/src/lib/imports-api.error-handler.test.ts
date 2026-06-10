import { afterEach, describe, expect, it, vi } from "vitest";
import { previewShipmentImport, confirmShipmentsImport } from "@/lib/api";
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

describe("Imports API — Tratamento 401/403", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("trata 401 no previewShipmentImport", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: async () => ({ detail: "Unauthorized" }),
    });
    global.fetch = mockFetch;

    await expect(previewShipmentImport("token", new File([], "test.csv"))).rejects.toThrow();
  });

  it("trata 403 no confirmShipmentsImport", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      json: async () => ({ detail: "Forbidden" }),
    });
    global.fetch = mockFetch;

    await expect(confirmShipmentsImport("token", 1)).rejects.toThrow();
  });
});
