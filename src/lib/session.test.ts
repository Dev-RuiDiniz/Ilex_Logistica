import { describe, expect, it } from "vitest";

import { parseRoleFromEmail } from "@/lib/session";

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
