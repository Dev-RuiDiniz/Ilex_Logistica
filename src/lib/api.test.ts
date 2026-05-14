import { describe, expect, it } from "vitest";

import { buildApiUrl, getApiBaseUrl } from "@/lib/api";

describe("api base url helpers", () => {
  it("normaliza barra final da base", () => {
    expect(getApiBaseUrl("http://localhost:8000/api/v1/")).toBe("http://localhost:8000/api/v1");
  });

  it("usa fallback quando variavel nao existe", () => {
    expect(getApiBaseUrl(undefined)).toBe("http://127.0.0.1:8000/api/v1");
  });

  it("monta URL completa com path sem barra inicial", () => {
    expect(buildApiUrl("auth/login", "http://localhost:8000/api/v1")).toBe(
      "http://localhost:8000/api/v1/auth/login",
    );
  });

  it("monta URL completa com path com barra inicial", () => {
    expect(buildApiUrl("/auth/login", "http://localhost:8000/api/v1")).toBe(
      "http://localhost:8000/api/v1/auth/login",
    );
  });
});
