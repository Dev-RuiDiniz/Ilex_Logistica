import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, request } from "./api";

describe("API Auth Error Handling", () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it("request adiciona Authorization header quando token é fornecido", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: "test" }),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    await request("/test", {
      headers: { Authorization: "Bearer test-token" },
    });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer test-token",
        }),
      })
    );
  });

  it("request não adiciona Authorization quando token não é fornecido", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: "test" }),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    await request("/test");

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.not.objectContaining({
          Authorization: expect.any(String),
        }),
      })
    );
  });

  it("lança ApiError com status 401 quando API retorna 401", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      text: () => Promise.resolve("Unauthorized"),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    await expect(request("/test")).rejects.toThrow(ApiError);
    try {
      await request("/test");
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect((error as ApiError).status).toBe(401);
      expect((error as ApiError).statusText).toBe("Unauthorized");
    }
  });

  it("lança ApiError com status 403 quando API retorna 403", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 403,
      statusText: "Forbidden",
      text: () => Promise.resolve("Forbidden"),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    await expect(request("/test")).rejects.toThrow(ApiError);
    try {
      await request("/test");
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect((error as ApiError).status).toBe(403);
      expect((error as ApiError).statusText).toBe("Forbidden");
    }
  });

  it("lança ApiError com mensagem útil quando API retorna erro genérico", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
      text: () => Promise.resolve("Internal Server Error"),
    });
    global.fetch = mockFetch as unknown as typeof fetch;

    await expect(request("/test")).rejects.toThrow(ApiError);
    try {
      await request("/test");
    } catch (error) {
      expect(error).toBeInstanceOf(ApiError);
      expect((error as ApiError).status).toBe(500);
      expect((error as ApiError).message).toBe("Internal Server Error");
    }
  });
});
