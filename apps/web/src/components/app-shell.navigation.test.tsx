import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { AppShell } from "./app-shell";
import * as authModule from "@/features/auth/auth-provider";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: () => {} }),
  usePathname: () => "/",
}));

describe("Sidebar Navigation por Permissão", () => {
  const renderWithAuth = (role: string) => {
    vi.spyOn(authModule, "useAuth").mockReturnValue({
      session: { email: "test@example.com", role, accessToken: "test-token" },
      logout: () => {},
    } as ReturnType<typeof authModule.useAuth>);

    return render(
      <AppShell>
        <div>Test Content</div>
      </AppShell>
    );
  };

  it("admin vê itens protegidos", () => {
    renderWithAuth("admin");
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Envios")).toBeInTheDocument();
    expect(screen.getByText("Importar Envios")).toBeInTheDocument();
    expect(screen.getByText("Transportadoras")).toBeInTheDocument();
    expect(screen.getByText("Pedidos e Cotações")).toBeInTheDocument();
    expect(screen.getByText("Relatório Diário")).toBeInTheDocument();
    expect(screen.getByText("Auditoria")).toBeInTheDocument();
    expect(screen.getByText("Usuários")).toBeInTheDocument();
  });

  it("manager vê auditoria, relatórios, alertas e SLA conforme matriz", () => {
    renderWithAuth("manager");
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Envios")).toBeInTheDocument();
    expect(screen.queryByText("Importar Envios")).not.toBeInTheDocument();
    expect(screen.getByText("Transportadoras")).toBeInTheDocument();
    expect(screen.getByText("Relatório Diário")).toBeInTheDocument();
    expect(screen.getByText("Auditoria")).toBeInTheDocument();
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("operator não vê auditoria", () => {
    renderWithAuth("operator");
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Envios")).toBeInTheDocument();
    expect(screen.getByText("Importar Envios")).toBeInTheDocument();
    expect(screen.queryByText("Transportadoras")).not.toBeInTheDocument();
    expect(screen.queryByText("Relatório Diário")).not.toBeInTheDocument();
    expect(screen.queryByText("Auditoria")).not.toBeInTheDocument();
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("operator não vê users", () => {
    renderWithAuth("operator");
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("viewer não vê ações/menus de escrita", () => {
    renderWithAuth("viewer");
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Envios")).toBeInTheDocument();
    expect(screen.queryByText("Importar Envios")).not.toBeInTheDocument();
    expect(screen.getByText("Transportadoras")).toBeInTheDocument();
    expect(screen.getByText("Relatório Diário")).toBeInTheDocument();
    expect(screen.queryByText("Auditoria")).not.toBeInTheDocument();
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("usuário sem permissão não vê item protegido", () => {
    renderWithAuth("operator");
    expect(screen.queryByText("Auditoria")).not.toBeInTheDocument();
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("usuário com audit:read vê Auditoria", () => {
    renderWithAuth("auditoria");
    expect(screen.getByText("Auditoria")).toBeInTheDocument();
  });

  it("usuário com users:read vê Usuários", () => {
    renderWithAuth("admin");
    expect(screen.getByText("Usuários")).toBeInTheDocument();
  });

  it("usuário sem users:read não vê Usuários", () => {
    renderWithAuth("manager");
    expect(screen.queryByText("Usuários")).not.toBeInTheDocument();
  });

  it("imports/shipments/carriers aparecem conforme permissões read", () => {
    renderWithAuth("logistica");
    expect(screen.getByText("Envios")).toBeInTheDocument();
    expect(screen.getByText("Importar Envios")).toBeInTheDocument();
    expect(screen.getByText("Transportadoras")).toBeInTheDocument();
  });
});
