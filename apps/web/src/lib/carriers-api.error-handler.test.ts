import { afterEach, describe, expect, it, vi } from "vitest";
import { listCarriers, createCarrier } from "@/lib/api";
import { ApiError } from "@/lib/api";
import type { CarrierCreate } from "@/lib/types";

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

describe("Carriers API — Tratamento 401/403", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("trata 401 no listCarriers", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: async () => ({ detail: "Unauthorized" }),
    });
    global.fetch = mockFetch;

    await expect(listCarriers("token")).rejects.toThrow();
  });

  it("trata 403 no createCarrier", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      json: async () => ({ detail: "Forbidden" }),
    });
    global.fetch = mockFetch;

    await expect(createCarrier("token", {} as CarrierCreate)).rejects.toThrow();
  });
});
