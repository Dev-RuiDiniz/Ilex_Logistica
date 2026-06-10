import { afterEach, describe, expect, it, vi } from "vitest";
import { getDailyReports, generateDailyReport } from "@/lib/daily-report-api";
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

describe("Daily Report API — Tratamento 401/403", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("trata 401 no getDailyReports", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: async () => ({ detail: "Unauthorized" }),
    });
    global.fetch = mockFetch;

    await expect(getDailyReports({})).rejects.toThrow();
  });

  it("trata 403 no generateDailyReport", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      json: async () => ({ detail: "Forbidden" }),
    });
    global.fetch = mockFetch;

    await expect(generateDailyReport({})).rejects.toThrow();
  });
});
