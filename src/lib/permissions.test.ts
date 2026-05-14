import { describe, expect, it } from "vitest";

import { canEditCarriers, canViewCarriers, getCarriersAccessMode } from "@/lib/permissions";

describe("permissions", () => {
  it("permite edicao para admin, logistica e gestor", () => {
    expect(canEditCarriers("admin")).toBe(true);
    expect(canEditCarriers("logistica")).toBe(true);
    expect(canEditCarriers("gestor")).toBe(true);
  });

  it("bloqueia edicao para auditoria e permite leitura", () => {
    expect(canEditCarriers("auditoria")).toBe(false);
    expect(canViewCarriers("auditoria")).toBe(true);
  });

  it("retorna modo de acesso textual para a UI", () => {
    expect(getCarriersAccessMode("admin")).toBe("edit");
    expect(getCarriersAccessMode("auditoria")).toBe("read");
  });
});
