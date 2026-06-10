import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup, within } from "@testing-library/react";
import DailyReportPage from "./page";
import {
  getDailyReports,
  getDailyReportById,
  getDailyReportByDate,
  generateDailyReport,
  parseSummary,
  parseKpis,
  parseExceptions,
  parseAlerts,
  parseCarrierEfficiency,
  parseImportFailures,
} from "@/lib/daily-report-api";
import type { DailyReport } from "@/lib/types";

// Mock the API client
vi.mock("@/lib/daily-report-api");

// Mock the parsing functions to return actual parsed data
vi.mocked(parseSummary).mockImplementation((json) => JSON.parse(json));
vi.mocked(parseKpis).mockImplementation((json) => JSON.parse(json));
vi.mocked(parseExceptions).mockImplementation((json) => JSON.parse(json));
vi.mocked(parseAlerts).mockImplementation((json) => JSON.parse(json));
vi.mocked(parseCarrierEfficiency).mockImplementation((json) => JSON.parse(json));
vi.mocked(parseImportFailures).mockImplementation((json) => JSON.parse(json));

describe("DailyReportPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  const createMockReport = (overrides?: Partial<DailyReport>): DailyReport => ({
    id: 1,
    report_date: "2025-01-21",
    status: "generated",
    generated_at: "2025-01-21T10:00:00Z",
    generated_by_user_id: null,
    period_start: "2025-01-21T00:00:00Z",
    period_end: "2025-01-21T23:59:59Z",
    summary_json: JSON.stringify({
      total_shipments: 100,
      on_time_count: 80,
      late_count: 15,
      critical_count: 3,
      warning_count: 2,
      unknown_sla_count: 0,
      exceptions_count: 20,
      import_failure_count: 5,
      carriers_count: 5,
    }),
    kpis_json: JSON.stringify({
      active_alerts_count: 5,
      delivery_rate: 0.8,
    }),
    exceptions_json: JSON.stringify([
      {
        tracking_code: "TRACK001",
        carrier_name: "Transportadora A",
        customer_name: "Cliente X",
        destination_uf: "SP",
        delay_days: 5,
        exception_type: "late",
        shipment_id: 1,
      },
      {
        tracking_code: "TRACK002",
        carrier_name: "Transportadora B",
        customer_name: "Cliente Y",
        destination_uf: "RJ",
        delay_days: 10,
        exception_type: "critical",
        shipment_id: 2,
      },
    ]),
    alerts_json: JSON.stringify([
      {
        id: 1,
        alert_type: "sla_critical",
        severity: "critical",
        message: "SLA crítico excedido",
        shipment_id: 123,
        created_at: "2025-01-21T10:00:00Z",
      },
      {
        id: 2,
        alert_type: "sla_late",
        severity: "warning",
        message: "Entrega atrasada",
        shipment_id: 124,
        created_at: "2025-01-21T10:00:00Z",
      },
    ]),
    carrier_efficiency_json: JSON.stringify([
      {
        carrier_name: "Transportadora A",
        total_shipments: 50,
        on_time_count: 45,
        late_count: 5,
        efficiency_rate: 0.9,
      },
      {
        carrier_name: "Transportadora B",
        total_shipments: 30,
        on_time_count: 25,
        late_count: 5,
        efficiency_rate: 0.833,
      },
    ]),
    import_failures_json: JSON.stringify({
      rejected_count: 5,
      rejected_rows: [
        { row_number: 1, error: "Invalid tracking code" },
        { row_number: 2, error: "Missing customer name" },
      ],
    }),
    notes: null,
    created_at: "2025-01-21T10:00:00Z",
    updated_at: "2025-01-21T10:00:00Z",
    ...overrides,
  });

  // 1. renderiza loading
  it("renders loading state", () => {
    (getDailyReports as vi.Mock).mockImplementation(() => new Promise(() => {}));

    render(<DailyReportPage />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  // 2. renderiza erro de API
  it("renders API error", async () => {
    (getDailyReports as vi.Mock).mockRejectedValue(new Error("API Error"));

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Falha ao carregar relatórios diários.")).toBeInTheDocument();
    });
  });

  // 3. renderiza estado vazio
  it("renders empty state", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum relatório encontrado.")).toBeInTheDocument();
    });
  });

  // 4. renderiza filtros
  it("renders filters", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Filtros")).toBeInTheDocument();
      expect(screen.getByText("Data Inicial")).toBeInTheDocument();
      expect(screen.getByText("Data Final")).toBeInTheDocument();
      expect(screen.getByText("Status")).toBeInTheDocument();
      expect(screen.getByText("Limpar Filtros")).toBeInTheDocument();
    });
  });

  // 5. altera filtro date_from/date_to e refaz consulta
  it("changes date_from/date_to filters and refetches", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledTimes(1);
    });

    const dateFromInput = screen.getAllByDisplayValue("")[0];
    const dateToInput = screen.getAllByDisplayValue("")[1];

    fireEvent.change(dateFromInput, { target: { value: "2025-01-01" } });
    fireEvent.change(dateToInput, { target: { value: "2025-01-31" } });

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledWith({
        date_from: "2025-01-01",
        date_to: "2025-01-31",
      });
    });
  });

  // 6. altera filtro status e refaz consulta
  it("changes status filter and refetches", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledTimes(1);
    });

    const statusSelect = screen.getByRole("combobox");
    fireEvent.change(statusSelect, { target: { value: "generated" } });

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledWith({
        status: "generated",
      });
    });
  });

  // 7. limpa filtros e refaz consulta sem parâmetros
  it("clears filters and refetches without parameters", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledTimes(1);
    });

    const dateFromInput = screen.getAllByDisplayValue("")[0];
    const dateToInput = screen.getAllByDisplayValue("")[1];
    const statusSelect = screen.getByRole("combobox");

    fireEvent.change(dateFromInput, { target: { value: "2025-01-01" } });
    fireEvent.change(dateToInput, { target: { value: "2025-01-31" } });
    fireEvent.change(statusSelect, { target: { value: "generated" } });

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledWith({
        date_from: "2025-01-01",
        date_to: "2025-01-31",
        status: "generated",
      });
    });

    const clearButton = screen.getByText("Limpar Filtros");
    fireEvent.click(clearButton);

    await waitFor(() => {
      expect(getDailyReports).toHaveBeenCalledWith({});
    });
  });

  // 8. consulta relatório por data
  it("searches report by date", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (getDailyReportByDate as vi.Mock).mockResolvedValue(createMockReport());

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const searchButton = screen.getByText("Buscar por Data");
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(getDailyReportByDate).toHaveBeenCalledWith("2025-01-21");
    });
  });

  // 9. botão gerar relatório chama generateDailyReport
  it("generate report button calls generateDailyReport", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (generateDailyReport as vi.Mock).mockResolvedValue(createMockReport());

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(generateDailyReport).toHaveBeenCalledWith({
        report_date: "2025-01-21",
      });
    });
  });

  // 10. trata erro ao gerar relatório
  it("handles error when generating report", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (generateDailyReport as vi.Mock).mockRejectedValue(new Error("Generation failed"));

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText("Falha ao gerar relatório diário.")).toBeInTheDocument();
    });
  });

  // 11. trata erro ao buscar por data sem data informada
  it("handles error when searching by date without date", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const searchButton = screen.getByText("Buscar por Data");
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(screen.getByText("Informe uma data para buscar.")).toBeInTheDocument();
    });
  });

  // 12. trata erro ao gerar sem data informada
  it("handles error when generating without date", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText("Informe uma data para gerar o relatório.")).toBeInTheDocument();
    });
  });

  // 13. abre detalhe por id e chama API
  it("opens details by id and calls API", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(getDailyReportById).toHaveBeenCalledWith(1);
    });
  });

  // 14. consulta relatório por data e seleciona relatório
  it("searches report by date and selects report", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (getDailyReportByDate as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const searchButton = screen.getByText("Buscar por Data");
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(getDailyReportByDate).toHaveBeenCalledWith("2025-01-21");
    });
  });

  // 15. UI atualiza após gerar relatório
  it("UI updates after generating report", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock)
      .mockResolvedValueOnce({ reports: [], total: 0, limit: 10, offset: 0 })
      .mockResolvedValueOnce({ reports: [mockReport], total: 1, limit: 10, offset: 0 });

    (generateDailyReport as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(generateDailyReport).toHaveBeenCalledWith({
        report_date: "2025-01-21",
      });
    });
  });

  // 16. botão voltar para lista funciona
  it("back to list button works", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(getDailyReportById).toHaveBeenCalledWith(1);
    });

    const backButton = screen.getByText("Voltar para Lista");
    fireEvent.click(backButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });
  });

  // === TESTES DE DETALHES OPERACIONAIS (BETA-018B) ===

  // 1. renderiza KPIs do relatório selecionado
  it("renders KPIs of selected report", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-kpis")).toBeInTheDocument();
    });
  });

  // 2. renderiza total de entregas
  it("renders total deliveries", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText("Total de Envios")).toBeInTheDocument();
      expect(screen.getByText("100")).toBeInTheDocument();
    });
  });

  // 3. renderiza entregas atrasadas
  it("renders late deliveries", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      const kpisSection = screen.getByTestId("daily-report-kpis");
      within(kpisSection).getByText("Atrasadas");
      within(kpisSection).getByText("15");
    });
  });

  // 4. renderiza entregas críticas
  it("renders critical deliveries", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText("Críticas")).toBeInTheDocument();
      expect(screen.getByText("3")).toBeInTheDocument();
    });
  });

  // 5. renderiza alertas ativos
  it("renders active alerts", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      const kpisSection = screen.getByTestId("daily-report-kpis");
      within(kpisSection).getByText("Alertas Ativos");
    });
  });

  // 6. renderiza exceções priorizadas
  it("renders prioritized exceptions", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-exceptions")).toBeInTheDocument();
      expect(screen.getByText("Exceções Priorizadas")).toBeInTheDocument();
    });
  });

  // 7. renderiza lista de alertas do relatório
  it("renders alert list from report", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-alerts")).toBeInTheDocument();
      expect(screen.getByText("Alertas Críticos/Ativos")).toBeInTheDocument();
      expect(screen.getByText("sla_critical")).toBeInTheDocument();
      expect(screen.getByText("SLA crítico excedido")).toBeInTheDocument();
    });
  });

  // 8. renderiza eficiência por transportadora
  it("renders carrier efficiency", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      const carriersSection = screen.getByTestId("daily-report-carriers");
      within(carriersSection).getByText("Top Transportadoras por Eficiência");
      within(carriersSection).getByText("Transportadora A");
      within(carriersSection).getByText("90.0%");
    }, { timeout: 3000 });
  });

  // 9. renderiza falhas de importação
  it("renders import failures", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      const importFailuresSection = screen.getByTestId("daily-report-import-failures");
      within(importFailuresSection).getByText("Falhas de Importação");
      within(importFailuresSection).getByText("Invalid tracking code");
    }, { timeout: 3000 });
  });

  // 10. renderiza período do relatório
  it("renders report period", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText(/Período:/)).toBeInTheDocument();
    });
  });

  // 11. abre detalhe por id e atualiza a UI
  it("opens detail by id and updates UI", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [mockReport],
      total: 1,
      limit: 10,
      offset: 0,
    });

    (getDailyReportById as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-list")).toBeInTheDocument();
    });

    const viewButton = await screen.findByText("Ver Detalhes");
    fireEvent.click(viewButton);

    await waitFor(() => {
      expect(getDailyReportById).toHaveBeenCalledWith(1);
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
      expect(screen.queryByTestId("daily-report-list")).not.toBeInTheDocument();
    });
  });

  // 12. consulta relatório por data e exibe detalhe
  it("searches report by date and displays detail", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (getDailyReportByDate as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const searchButton = screen.getByText("Buscar por Data");
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(getDailyReportByDate).toHaveBeenCalledWith("2025-01-21");
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
      expect(screen.getByTestId("daily-report-kpis")).toBeInTheDocument();
    });
  });

  // 13. botão gerar relatório chama generateDailyReport
  it("generate report button calls generateDailyReport and updates UI", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock)
      .mockResolvedValueOnce({ reports: [], total: 0, limit: 10, offset: 0 })
      .mockResolvedValueOnce({ reports: [mockReport], total: 1, limit: 10, offset: 0 });

    (generateDailyReport as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(generateDailyReport).toHaveBeenCalledWith({
        report_date: "2025-01-21",
      });
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
    });
  });

  // 14. UI atualiza lista e detalhe após gerar relatório
  it("UI updates list and detail after generating report", async () => {
    const mockReport = createMockReport();

    (getDailyReports as vi.Mock)
      .mockResolvedValueOnce({ reports: [], total: 0, limit: 10, offset: 0 })
      .mockResolvedValueOnce({ reports: [mockReport], total: 1, limit: 10, offset: 0 });

    (generateDailyReport as vi.Mock).mockResolvedValue(mockReport);

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(generateDailyReport).toHaveBeenCalled();
    });

    await waitFor(() => {
      expect(screen.getByTestId("daily-report-detail")).toBeInTheDocument();
      expect(screen.getByTestId("daily-report-kpis")).toBeInTheDocument();
    });
  });

  // 15. trata erro ao gerar relatório
  it("handles error when generating report and shows error message", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (generateDailyReport as vi.Mock).mockRejectedValue(new Error("Generation failed"));

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const generateButton = screen.getByText("Gerar Relatório");
    fireEvent.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText("Falha ao gerar relatório diário.")).toBeInTheDocument();
    });
  });

  // 16. diferencia relatório inexistente de relatório vazio
  it("differentiates non-existent report from empty report", async () => {
    (getDailyReports as vi.Mock).mockResolvedValue({
      reports: [],
      total: 0,
      limit: 10,
      offset: 0,
    });

    (getDailyReportByDate as vi.Mock).mockRejectedValue(new Error("Not found"));

    render(<DailyReportPage />);

    await waitFor(() => {
      expect(screen.getByText("Gerar ou Buscar Relatório")).toBeInTheDocument();
    });

    const dateInput = screen.getAllByDisplayValue("")[2];
    fireEvent.change(dateInput, { target: { value: "2025-01-21" } });

    const searchButton = screen.getByText("Buscar por Data");
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(screen.getByText("Relatório não encontrado para a data informada.")).toBeInTheDocument();
    });
  });
});
