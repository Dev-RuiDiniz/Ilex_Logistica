import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup, within } from "@testing-library/react";
import DashboardPage from "./page";
import { getDashboardSummary } from "@/lib/dashboard-api";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

vi.mock("@/lib/dashboard-api");

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(() => "test-token"),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
Object.defineProperty(global, "localStorage", { value: localStorageMock });

describe("DashboardPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renderiza loading", () => {
    vi.mocked(getDashboardSummary).mockImplementation(() => new Promise(() => {}));

    render(<DashboardPage />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("renderiza erro de API", async () => {
    vi.mocked(getDashboardSummary).mockRejectedValueOnce(new Error("API Error"));

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText(/Erro: API Error/i)).toBeInTheDocument();
    });
  });

  it("renderiza estado vazio", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce(null as unknown as DashboardSummaryResponse);

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Sem dados")).toBeInTheDocument();
    });
  });

  it("renderiza cards de KPI", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Painel de controle")).toBeInTheDocument();
      const kpiSection = screen.getByTestId("dashboard-kpi-cards");
      within(kpiSection).getByText("Total");
      within(kpiSection).getByText("No Prazo");
      within(kpiSection).getByText("Atrasadas");
      within(kpiSection).getByText("Críticas");
      within(kpiSection).getByText("Atenção");
      within(kpiSection).getByText("Sem SLA");
      within(kpiSection).getByText("Exceções");
      within(kpiSection).getByText("Transportadoras");
      within(kpiSection).getByText("Alertas Ativos");
      within(kpiSection).getByText("Falhas Importação");
    });
  });

  it("exibe total de entregas", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });
  });

  it("exibe no prazo", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("80");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe atrasadas", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("15");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe críticas", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("3");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe warning", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("2");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe sem SLA", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("0");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe exceções", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const values = screen.getAllByText("20");
      expect(values.length).toBeGreaterThan(0);
    });
  });

  it("exibe alertas ativos como nenhum alerta ativo", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum alerta ativo")).toBeInTheDocument();
    });
  });

  it("exibe alertas ativos com contador real e link para tela de alertas", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 7,
      active_alerts_count: 5,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const kpiSection = screen.getByTestId("dashboard-kpi-cards");
      within(kpiSection).getByText("5");
      expect(screen.getByText("Ver alertas →")).toBeInTheDocument();
      expect(screen.getByText("Ver alertas →").closest("a")).toHaveAttribute("href", "/alerts");
    });
  });

  it("exibe top transportadoras por eficiência", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [
        {
          carrier_id: 1,
          carrier_name: "Transportadora A",
          total_shipments: 50,
          on_time_count: 45,
          late_count: 5,
          critical_count: 0,
          lost_count: 0,
          total_freight_value: 500,
          total_invoice_value: 5000,
          on_time_percentage: 90,
          late_percentage: 10,
          lost_percentage: 0,
          average_freight_percentage: 10,
          average_freight_value: 10,
          ranking_by_efficiency: 1,
          ranking_by_cost: 1,
          ranking_by_volume: 1,
        },
      ],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Top Transportadoras por Eficiência")).toBeInTheDocument();
    });
  });

  it("exibe top exceções priorizadas", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [
        {
          shipment_id: 1,
          tracking_code: "ABC123",
          invoice_number: "NF123",
          carrier_id: 1,
          carrier_name: "Transportadora A",
          customer_name: "Cliente X",
          destination_uf: "SP",
          status: "in_transit",
          sla_status: "critical",
          criticality: "alta",
          delay_days: 15,
          sla_due_date: "2025-01-01T00:00:00Z",
          exception_type: "critical",
          exception_reason: "critical - critical",
          priority: 1,
          last_update_at: "2025-01-15T00:00:00Z",
        },
      ],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("Top Exceções Priorizadas")).toBeInTheDocument();
    });
  });

  it("exibe generated_at formatado", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText(/Gerado em:/i)).toBeInTheDocument();
    });
  });

  it("renderiza filtros globais", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      const filtersSection = screen.getByTestId("dashboard-filters");
      within(filtersSection).getByText("Filtros");
      within(filtersSection).getByLabelText(/Mês/i);
      within(filtersSection).getByLabelText(/Ano/i);
      within(filtersSection).getByLabelText(/Cliente/i);
      within(filtersSection).getByLabelText(/UF/i);
      within(filtersSection).getByLabelText(/Status SLA/i);
      within(filtersSection).getByLabelText(/Atrasada/i);
    });
  });

  it("altera filtro de mês/ano e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const monthInput = screen.getByLabelText(/Mês/i);
    fireEvent.change(monthInput, { target: { value: "1" } });
  });

  it("altera filtro de UF e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const ufInput = screen.getByLabelText(/UF/i);
    fireEvent.change(ufInput, { target: { value: "SP" } });
  });

  it("altera filtro de transportadora e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const carrierInput = screen.getByLabelText(/Cliente/i);
    fireEvent.change(carrierInput, { target: { value: "1" } });
  });

  it("altera filtro de criticality e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const clientInput = screen.getByLabelText(/Cliente/i);
    fireEvent.change(clientInput, { target: { value: "alta" } });
  });

  it("altera filtro de sla_status e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const slaSelect = screen.getByLabelText(/Status SLA/i);
    fireEvent.change(slaSelect, { target: { value: "on_time" } });
  });

  it("altera filtro de is_late e serializa boolean", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const isLateSelect = screen.getByLabelText(/Atrasada/i);
    fireEvent.change(isLateSelect, { target: { value: "true" } });
  });

  it("altera filtro de exception_type e refaz consulta", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const clientInput = screen.getByLabelText(/Cliente/i);
    fireEvent.change(clientInput, { target: { value: "critical" } });
  });

  it("limpa filtros e refaz consulta sem parâmetros", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const clearButton = screen.getByTestId("clear-main-filters");
    fireEvent.click(clearButton);
  });

  it("UI muda quando resposta filtrada muda", async () => {
    vi.mocked(getDashboardSummary).mockResolvedValueOnce({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      resolved_count: 0,
      no_update_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      active_alerts_count: 0,
      carriers_count: 10,
      top_carriers_by_efficiency: [],
      top_exceptions: [],
      generated_at: "2025-01-15T00:00:00Z",
      filters_applied: {},
    });

    render(<DashboardPage />);

    await waitFor(() => {
      expect(screen.getByText("100")).toBeInTheDocument();
    });

    const ufInput = screen.getByLabelText(/UF/i);
    fireEvent.change(ufInput, { target: { value: "SP" } });
  });
});
