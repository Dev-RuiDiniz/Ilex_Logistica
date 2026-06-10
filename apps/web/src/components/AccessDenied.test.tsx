import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { AccessDenied } from "./AccessDenied";

describe("AccessDenied Component", () => {
  it("renderiza título de acesso negado", () => {
    render(<AccessDenied />);
    expect(screen.getByText("Acesso Negado")).toBeInTheDocument();
  });

  it("renderiza mensagem padrão", () => {
    render(<AccessDenied />);
    expect(screen.getByText(/Você não tem permissão para acessar esta página/)).toBeInTheDocument();
  });

  it("renderiza mensagem customizada quando fornecida", () => {
    render(<AccessDenied message="Acesso restrito a administradores" />);
    expect(screen.getByText("Acesso restrito a administradores")).toBeInTheDocument();
  });

  it("exibe botão de voltar ao dashboard por padrão", () => {
    render(<AccessDenied />);
    const button = screen.getByRole("link", { name: /Voltar ao Dashboard/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveAttribute("href", "/");
  });

  it("não exibe botão quando showBackButton é false", () => {
    render(<AccessDenied showBackButton={false} />);
    expect(screen.queryByRole("link", { name: /Voltar ao Dashboard/i })).not.toBeInTheDocument();
  });

  it("renderiza corretamente sem props opcionais", () => {
    render(<AccessDenied />);
    expect(screen.getByText("Acesso Negado")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Voltar ao Dashboard/i })).toBeInTheDocument();
  });

  it("não vaza detalhes técnicos sensíveis", () => {
    render(<AccessDenied />);
    const content = document.body.textContent || "";
    expect(content).not.toMatch(/error|exception|stack|trace|debug|console/i);
  });
});
