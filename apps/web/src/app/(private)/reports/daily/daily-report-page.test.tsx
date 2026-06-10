import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import DailyReportPage from "./page";
import {
  getDailyReports,
  getDailyReportByDate,
  generateDailyReport,
} from "@/lib/daily-report-api";

// Mock the API client
vi.mock("@/lib/daily-report-api");

describe("DailyReportPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
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

    (getDailyReportByDate as vi.Mock).mockResolvedValue(null);

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

    (generateDailyReport as vi.Mock).mockResolvedValue(null);

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
});
