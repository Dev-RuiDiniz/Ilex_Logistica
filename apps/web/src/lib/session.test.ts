import { beforeEach, describe, expect, it } from "vitest";

import { clearSession, getSession, parseRoleFromEmail, saveSession } from "@/lib/session";

describe("parseRoleFromEmail", () => {
  it("define admin por e-mail admin", () => {
    expect(parseRoleFromEmail("admin@ilex.com")).toBe("admin");
  });

  it("define auditoria por e-mail audit", () => {
    expect(parseRoleFromEmail("audit@ilex.com")).toBe("auditoria");
  });

  it("usa logistica como padrao", () => {
    expect(parseRoleFromEmail("operador@ilex.com")).toBe("logistica");
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
