import { describe, expect, it } from "vitest";

import { getRoleUiLabel } from "@/components/app-shell";

describe("app shell role labels", () => {
  it("retorna label de acesso para perfis com permissao", () => {
    expect(getRoleUiLabel("admin")).toBe("(acesso)");
    expect(getRoleUiLabel("gestor")).toBe("(acesso)");
    expect(getRoleUiLabel("logistica")).toBe("(acesso)");
    expect(getRoleUiLabel("manager")).toBe("(acesso)");
    expect(getRoleUiLabel("viewer")).toBe("(acesso)");
    expect(getRoleUiLabel("auditoria")).toBe("(acesso)");
  });

  it("retorna label de sem acesso para perfis sem permissao", () => {
    expect(getRoleUiLabel("operator")).toBe("(sem acesso)");
  });
});
