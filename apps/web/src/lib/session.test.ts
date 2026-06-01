import { beforeEach, describe, expect, it } from "vitest";

import { clearSession, getPrimaryRole, getSession, saveSession } from "@/lib/session";

describe("getPrimaryRole", () => {
  it("retorna primeiro role vindo do backend", () => {
    expect(getPrimaryRole(["admin"])).toBe("admin");
  });

  it("usa logistica como fallback", () => {
    expect(getPrimaryRole([])).toBe("logistica");
  });
});

describe("session storage", () => {
  beforeEach(() => {
    localStorage.clear();
    document.cookie = "ilex_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  });

  it("salva e recupera sessao", () => {
    saveSession({
      email: "admin@ilex.com",
      accessToken: "access-token",
      refreshToken: "refresh-token",
      role: "admin",
    });

    expect(getSession()).toEqual({
      email: "admin@ilex.com",
      accessToken: "access-token",
      refreshToken: "refresh-token",
      role: "admin",
    });
  });

  it("limpa sessao e cookie de token", () => {
    saveSession({
      email: "admin@ilex.com",
      accessToken: "access-token",
      refreshToken: "refresh-token",
      role: "admin",
    });

    clearSession();

    expect(getSession()).toBeNull();
    expect(document.cookie).not.toContain("ilex_token=access-token");
  });
});
