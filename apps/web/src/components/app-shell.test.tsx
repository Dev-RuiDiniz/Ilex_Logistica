import { describe, expect, it } from "vitest";

import { getRoleUiLabel } from "@/components/app-shell";

describe("app shell role labels", () => {
  it("retorna label de edicao para perfis com permissao", () => {
    expect(getRoleUiLabel("admin")).toBe("(edicao)");
    expect(getRoleUiLabel("gestor")).toBe("(edicao)");
    expect(getRoleUiLabel("logistica")).toBe("(edicao)");
  });

  it("retorna label de somente leitura para auditoria", () => {
    expect(getRoleUiLabel("auditoria")).toBe("(somente leitura)");
  });
});
