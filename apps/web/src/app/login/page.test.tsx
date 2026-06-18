import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";

import LoginPage, { getLoginErrorMessage } from "@/app/login/page";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

describe("login error message", () => {
  it("retorna mensagem padrao de credenciais invalidas", () => {
    expect(getLoginErrorMessage()).toBe("Credenciais invalidas. Verifique e tente novamente.");
  });

  it("renderiza estrutura premium com showcase e painel de acesso", () => {
    render(<LoginPage />);

    expect(screen.getByTestId("login-showcase")).toBeInTheDocument();
    expect(screen.getByTestId("login-form-panel")).toBeInTheDocument();
    expect(screen.getByText(/Torre de controle para exceções/i)).toBeInTheDocument();
    expect(screen.getByText(/Priorize alertas, acompanhe envios e reaja mais rápido/i)).toBeInTheDocument();
  });
});
