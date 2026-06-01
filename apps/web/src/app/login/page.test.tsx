import { describe, expect, it } from "vitest";

import { getLoginErrorMessage } from "@/app/login/page";

describe("login error message", () => {
  it("retorna mensagem padrao de credenciais invalidas", () => {
    expect(getLoginErrorMessage()).toBe("Credenciais invalidas. Verifique e tente novamente.");
  });
});
