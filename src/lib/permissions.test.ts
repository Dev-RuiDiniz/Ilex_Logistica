import { describe, expect, it } from "vitest";

import { canEditCarriers, canViewCarriers } from "@/lib/permissions";

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
});
