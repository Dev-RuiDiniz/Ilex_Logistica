import { afterEach, describe, expect, it, vi } from "vitest";
import { handleApiError, isApiError } from "@/lib/error-handler";
import { ApiError } from "@/lib/api";

describe("Error Handler — Tratamento 401/403", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("redireciona para login em 401", () => {
    const mockLocation = { href: "" };
    vi.stubGlobal("window", { location: mockLocation });

    const error = new ApiError("Unauthorized", 401, "Unauthorized");
    const result = handleApiError(error);
    expect(result).toContain("Sessão expirada");
    expect(mockLocation.href).toBe("/login");
  });

  it("retorna mensagem de permissão em 403", () => {
    const error = new ApiError("Forbidden", 403, "Forbidden");
    const result = handleApiError(error);
    expect(result).toContain("permissão");
  });

  it("preserva mensagem útil em erros genéricos", () => {
    const error = new Error("Erro interno do servidor");
    const result = handleApiError(error);
    expect(result).toBe("Erro interno do servidor");
  });

  it("lida com erros desconhecidos", () => {
    const result = handleApiError("string error");
    expect(result).toBe("Erro desconhecido");
  });

  it("identifica ApiError corretamente", () => {
    const apiError = new ApiError("Test", 403, "Forbidden");
    const normalError = new Error("Test");
    expect(isApiError(apiError)).toBe(true);
    expect(isApiError(normalError)).toBe(false);
  });
});
