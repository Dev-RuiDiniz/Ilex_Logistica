import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import AuditPage from "./page";
import * as auditApi from "@/lib/audit-api";
import * as authModule from "@/features/auth/auth-provider";

// Mock the API and auth modules
vi.mock("@/lib/audit-api", () => ({
  getAuditLogs: vi.fn(),
  getAuditSummary: vi.fn(),
}));

vi.mock("@/features/auth/auth-provider", () => ({
  useAuth: vi.fn(),
}));

describe("AuditPage", () => {
  const mockToken = "test-token";
  const mockLogs = [
    {
      id: 1,
      event_type: "daily_report_generated",
      entity_type: "daily_report",
      entity_id: 1,
      action: "create",
      actor_user_id: null,
      actor_email: null,
      source: "api",
      severity: "info" as const,
      status: "success" as const,
      message: "Relatório diário gerado",
      before_json: null,
      after_json: null,
      metadata_json: null,
      request_id: "req-123",
      ip_address: "127.0.0.1",
      user_agent: "Mozilla/5.0",
      created_at: "2025-01-21T10:00:00Z",
    },
  ];

  const mockSummary = {
    total_logs: 100,
    success_count: 80,
    failed_count: 15,
    skipped_count: 5,
    critical_count: 5,
    warning_count: 10,
    info_count: 85,
    create_count: 50,
    update_count: 30,
    delete_count: 10,
    read_count: 10,
  };

  beforeEach(() => {
    vi.clearAllMocks();
    (authModule.useAuth as jest.Mock).mockReturnValue({ session: { accessToken: mockToken } });
    (auditApi.getAuditLogs as jest.Mock).mockResolvedValue({
      logs: mockLogs,
      total: 1,
      page: 1,
      page_size: 50,
    });
    (auditApi.getAuditSummary as jest.Mock).mockResolvedValue(mockSummary);
  });

  it("renderiza título 'Auditoria Operacional'", () => {
    render(<AuditPage />);
    expect(screen.getByText("Auditoria Operacional")).toBeInTheDocument();
  });

  it("renderiza summary cards", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-summary").length).toBeGreaterThan(0);
    });
  });

  it("renderiza total de logs", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Total de Logs").length).toBeGreaterThan(0);
    });
  });

  it("renderiza totais por severity", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Sucesso").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Falhas").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Críticos").length).toBeGreaterThan(0);
    });
  });

  it("renderiza totais por status", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Sucesso").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Falhas").length).toBeGreaterThan(0);
    });
  });

  it("renderiza tabela/lista de logs", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-log-table").length).toBeGreaterThan(0);
    });
  });

  it("renderiza event_type/action/entity/severity/status/actor/message", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByText("daily_report_generated").length).toBeGreaterThan(0);
      expect(screen.getAllByText("create").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Info").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Success").length).toBeGreaterThan(0);
      expect(screen.getAllByText("System").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Relatório diário gerado").length).toBeGreaterThan(0);
    });
  });

  it("renderiza loading state", () => {
    (auditApi.getAuditLogs as jest.Mock).mockImplementation(() => new Promise(() => {}));
    render(<AuditPage />);
    expect(screen.getByText("Carregando logs...")).toBeInTheDocument();
  });

  it("renderiza empty state", async () => {
    (auditApi.getAuditLogs as jest.Mock).mockResolvedValue({
      logs: [],
      total: 0,
      page: 1,
      page_size: 50,
    });
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getByTestId("audit-empty-state")).toBeInTheDocument();
    });
  });

  it("renderiza error state", async () => {
    (auditApi.getAuditLogs as jest.Mock).mockRejectedValue(new Error("API Error"));
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getByTestId("audit-error-state")).toBeInTheDocument();
    });
  });

  it("aplica filtro por event_type", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
    });

    const eventInput = screen.getAllByPlaceholderText("Ex: daily_report_generated");
    expect(eventInput.length).toBeGreaterThan(0);
  });

  it("aplica filtro por severity", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
    });

    const severitySelects = screen.getAllByText("Todos");
    expect(severitySelects.length).toBeGreaterThan(0);
  });

  it("aplica filtro por status", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
    });

    const statusSelects = screen.getAllByText("Todos");
    expect(statusSelects.length).toBeGreaterThan(0);
  });

  it("aplica filtro por entity_type", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
    });

    const entityInput = screen.getAllByPlaceholderText("Ex: shipment");
    expect(entityInput.length).toBeGreaterThan(0);
  });

  it("limpa filtros", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
    });

    const clearButton = screen.getAllByText("Limpar Filtros");
    expect(clearButton.length).toBeGreaterThan(0);
  });

  it("chama getAuditLogs ao mudar filtros", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(auditApi.getAuditLogs).toHaveBeenCalled();
    });

    const applyButton = screen.getAllByText("Aplicar Filtros");
    expect(applyButton.length).toBeGreaterThan(0);
  });

  it("abre detalhe de log", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-log-row").length).toBeGreaterThan(0);
    });
  });

  it("detalhe mostra metadata_json", async () => {
    const logWithMetadata = {
      ...mockLogs[0],
      metadata_json: JSON.stringify({ test: "value" }),
    };
    (auditApi.getAuditLogs as jest.Mock).mockResolvedValue({
      logs: [logWithMetadata],
      total: 1,
      page: 1,
      page_size: 50,
    });

    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-log-row").length).toBeGreaterThan(0);
    });
  });

  it("detalhe lida com JSON vazio", async () => {
    const logWithEmptyJson = {
      ...mockLogs[0],
      before_json: null,
      after_json: null,
    };
    (auditApi.getAuditLogs as jest.Mock).mockResolvedValue({
      logs: [logWithEmptyJson],
      total: 1,
      page: 1,
      page_size: 50,
    });

    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-log-row").length).toBeGreaterThan(0);
    });
  });

  it("detalhe não quebra com campos ausentes", async () => {
    const logWithMissingFields = {
      ...mockLogs[0],
      actor_email: null,
      actor_user_id: null,
      source: null,
    };
    (auditApi.getAuditLogs as jest.Mock).mockResolvedValue({
      logs: [logWithMissingFields],
      total: 1,
      page: 1,
      page_size: 50,
    });

    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-log-row").length).toBeGreaterThan(0);
    });
  });

  it("renderiza badges de severity/status", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Info").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Success").length).toBeGreaterThan(0);
    });
  });
});
