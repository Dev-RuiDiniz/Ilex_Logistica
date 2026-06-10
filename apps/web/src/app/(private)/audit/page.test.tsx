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

  it("renderiza título da página", () => {
    render(<AuditPage />);
    expect(screen.getByText("Auditoria Operacional")).toBeInTheDocument();
  });

  it("renderiza loading state", () => {
    (auditApi.getAuditLogs as jest.Mock).mockImplementation(() => new Promise(() => {}));
    render(<AuditPage />);
    expect(screen.getByText("Carregando...")).toBeInTheDocument();
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

  it("renderiza summary, filtros e tabela quando há dados", async () => {
    render(<AuditPage />);
    await waitFor(() => {
      expect(screen.getAllByTestId("audit-summary").length).toBeGreaterThan(0);
      expect(screen.getAllByTestId("audit-filters").length).toBeGreaterThan(0);
      expect(screen.getAllByTestId("audit-log-table").length).toBeGreaterThan(0);
    });
  });
});
