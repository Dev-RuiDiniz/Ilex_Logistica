import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { ApiError } from "./api";
import { useApiErrorHandler } from "./useApiErrorHandler";
import { clearSession } from "./session";

// Mock do session
vi.mock("./session", () => ({
  clearSession: vi.fn(),
}));

describe("useApiErrorHandler", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock window.location
    Reflect.deleteProperty(window, "location");
    Object.defineProperty(window, "location", {
      configurable: true,
      value: { href: "" },
    });
  });

  it("deve redirecionar para login ao receber erro 401", () => {
    const { result } = renderHook(() => useApiErrorHandler());
    const error401 = new ApiError("Unauthorized", 401, "Unauthorized");

    act(() => {
      result.current.handleApiError(error401);
    });

    expect(clearSession).toHaveBeenCalled();
    expect(window.location.href).toBe("/login");
  });

  it("deve exibir AccessDenied ao receber erro 403", () => {
    const { result } = renderHook(() => useApiErrorHandler());
    const error403 = new ApiError("Forbidden", 403, "Forbidden");

    act(() => {
      result.current.handleApiError(error403);
    });

    expect(result.current.accessDenied).toBe(true);
    expect(result.current.accessDeniedMessage).toBe("Forbidden");
  });

  it("deve limpar estado accessDenied ao chamar resetAccessDenied", () => {
    const { result } = renderHook(() => useApiErrorHandler());
    const error403 = new ApiError("Forbidden", 403, "Forbidden");

    act(() => {
      result.current.handleApiError(error403);
    });
    expect(result.current.accessDenied).toBe(true);

    act(() => {
      result.current.resetAccessDenied();
    });
    expect(result.current.accessDenied).toBe(false);
  });

  it("deve preservar mensagem de erro customizada para 403", () => {
    const { result } = renderHook(() => useApiErrorHandler());
    const customMessage = "Você não tem permissão para acessar este recurso";
    const error403 = new ApiError(customMessage, 403, "Forbidden");

    act(() => {
      result.current.handleApiError(error403);
    });

    expect(result.current.accessDeniedMessage).toBe(customMessage);
  });

  it("não deve fazer nada para erros que não sejam 401 ou 403", () => {
    const { result } = renderHook(() => useApiErrorHandler());
    const error500 = new ApiError("Internal Server Error", 500, "Internal Server Error");

    act(() => {
      result.current.handleApiError(error500);
    });

    expect(result.current.accessDenied).toBe(false);
    expect(clearSession).not.toHaveBeenCalled();
    expect(window.location.href).toBe("");
  });
});
