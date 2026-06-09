import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ExceptionsPanelPage from "./page";
import { getExceptionsPanel } from "@/lib/exceptions-api";

vi.mock("@/lib/session", () => ({
  useSession: () => ({ accessToken: "test-token" }),
}));

vi.mock("@/lib/exceptions-api");

describe("ExceptionsPanelPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("Deve renderizar loading", () => {
    vi.mocked(getExceptionsPanel).mockImplementation(() => new Promise(() => {}));

    render(<ExceptionsPanelPage />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("Deve renderizar erro de API", async () => {
    vi.mocked(getExceptionsPanel).mockRejectedValueOnce(new Error("API Error"));

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getByText(/Erro: API Error/i)).toBeInTheDocument();
    });
  });

  it("Deve renderizar estado vazio", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce(null as unknown as ExceptionsPanelResponse);

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getByText("Sem dados")).toBeInTheDocument();
    });
  });

  it("Deve renderizar cards de resumo", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce({
      summary: { total_exceptions: 10, critical_count: 2, late_count: 5, warning_count: 2, unknown_sla_count: 1 },
      items: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF123",
          carrier_id: 1,
          carrier_name: "Transportadora A",
          customer_name: "Cliente X",
          destination_uf: "SP",
          status: "delivered",
          sla_status: "critical",
          criticality: "alta",
          delay_days: 15,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "critical",
          exception_reason: "Atraso crítico de 15 dias",
          priority: 1,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    });

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getByText("Total")).toBeInTheDocument();
      expect(screen.getByText("Críticas")).toBeInTheDocument();
      expect(screen.getByText("Atrasadas")).toBeInTheDocument();
      expect(screen.getAllByText("Atenção").length).toBeGreaterThan(0);
      expect(screen.getAllByText("Sem SLA").length).toBeGreaterThan(0);
    });
  });

  it("Deve renderizar lista/tabela de exceções", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce({
      summary: { total_exceptions: 1, critical_count: 1, late_count: 0, warning_count: 0, unknown_sla_count: 0 },
      items: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF123",
          carrier_id: 1,
          carrier_name: "Transportadora A",
          customer_name: "Cliente X",
          destination_uf: "SP",
          status: "delivered",
          sla_status: "critical",
          criticality: "alta",
          delay_days: 15,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "critical",
          exception_reason: "Atraso crítico de 15 dias",
          priority: 1,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    });

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getByText("ABC123")).toBeInTheDocument();
      expect(screen.getByText("NF123")).toBeInTheDocument();
      expect(screen.getByText("Transportadora A")).toBeInTheDocument();
    });
  });

  it("Deve destacar critical", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce({
      summary: { total_exceptions: 1, critical_count: 1, late_count: 0, warning_count: 0, unknown_sla_count: 0 },
      items: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF123",
          carrier_id: 1,
          carrier_name: "Transportadora A",
          customer_name: "Cliente X",
          destination_uf: "SP",
          status: "delivered",
          sla_status: "critical",
          criticality: "alta",
          delay_days: 15,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "critical",
          exception_reason: "Atraso crítico de 15 dias",
          priority: 1,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    });

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      const criticalBadges = screen.getAllByText("critical");
      expect(criticalBadges.length).toBeGreaterThan(0);
    });
  });

  it("Deve exibir atraso em dias", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce({
      summary: { total_exceptions: 1, critical_count: 0, late_count: 1, warning_count: 0, unknown_sla_count: 0 },
      items: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF123",
          carrier_id: 1,
          carrier_name: "Transportadora A",
          customer_name: "Cliente X",
          destination_uf: "SP",
          status: "delivered",
          sla_status: "late",
          criticality: "media",
          delay_days: 10,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "late",
          exception_reason: "Atraso de 10 dias",
          priority: 2,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    });

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getByText("10")).toBeInTheDocument();
    });
  });



  it("Deve respeitar payload parcialmente ausente", async () => {
    vi.mocked(getExceptionsPanel).mockResolvedValueOnce({
      summary: { total_exceptions: 1, critical_count: 0, late_count: 1, warning_count: 0, unknown_sla_count: 0 },
      items: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: null,
          carrier_id: 1,
          carrier_name: null,
          customer_name: null,
          destination_uf: null,
          status: "delivered",
          sla_status: "late",
          criticality: "media",
          delay_days: 10,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "late",
          exception_reason: "Atraso de 10 dias",
          priority: 2,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      filters_applied: {},
      generated_at: "2025-01-15T00:00:00Z",
    });

    render(<ExceptionsPanelPage />);

    await waitFor(() => {
      expect(screen.getAllByText(/-/i).length).toBeGreaterThan(0);
    });
  });

});
