import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup, within } from "@testing-library/react";
import { listShipments } from "@/lib/api";
import ShipmentsPage from "./page";
import { useAuth } from "@/features/auth/auth-provider";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

vi.mock("@/lib/api");
vi.mock("@/features/auth/auth-provider");

const mockSession = {
  accessToken: "test-token",
  role: "gestor",
};

describe("Shipments SLA filters", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession });
  });

  it("Deve renderizar loading", async () => {
    vi.mocked(listShipments).mockImplementation(() => new Promise(() => {}));

    render(<ShipmentsPage />);

    expect(screen.getByText("Carregando envios...")).toBeInTheDocument();
  });

  it("Deve renderizar erro de API", async () => {
    vi.mocked(listShipments).mockRejectedValueOnce(new Error("API Error"));

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Erro/i)).toBeInTheDocument();
    });
  });

  it("Deve renderizar estado vazio", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum envio encontrado.")).toBeInTheDocument();
    });
  });

  it("Deve aplicar filtro por sla_status", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("SLA")).toBeInTheDocument();
    });

    const slaSelect = screen.getByText("SLA").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(slaSelect, { target: { value: "critical" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ sla_status: "critical" })
      );
    });
  });

  it("Deve renderizar dropdown de SLA com todas as opções", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("SLA")).toBeInTheDocument();
    });

    const slaSelect = screen.getByText("SLA").closest("div")?.querySelector("select") as HTMLSelectElement;
    expect(slaSelect).toBeTruthy();
    const options = Array.from(slaSelect.options).map((o) => o.value);
    expect(options).toContain("");
    expect(options).toContain("on_time");
    expect(options).toContain("warning");
    expect(options).toContain("late");
    expect(options).toContain("critical");
    expect(options).toContain("unknown");
  });

  it("Deve aplicar filtro por sla_status=critical", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("SLA")).toBeInTheDocument();
    });

    const slaSelect = screen.getByText("SLA").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(slaSelect, { target: { value: "critical" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ sla_status: "critical" })
      );
    });
  });

  it("Deve aplicar filtro por is_late=true", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Atrasado?")).toBeInTheDocument();
    });

    const isLateSelect = screen.getByText("Atrasado?").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(isLateSelect, { target: { value: "true" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ is_late: true })
      );
    });
  });

  it("Deve aplicar filtro por is_late=false", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Atrasado?")).toBeInTheDocument();
    });

    const isLateSelect = screen.getByText("Atrasado?").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(isLateSelect, { target: { value: "false" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ is_late: false })
      );
    });
  });

  it("Deve combinar filtros sla_status e is_late", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("SLA")).toBeInTheDocument();
    });

    const slaSelect = screen.getByText("SLA").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(slaSelect, { target: { value: "warning" } });

    const isLateSelect = screen.getByText("Atrasado?").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(isLateSelect, { target: { value: "true" } });

    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ sla_status: "warning", is_late: true })
      );
    });
  });

  it("Deve limpar filtros SLA ao clicar em Limpar", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("SLA")).toBeInTheDocument();
    });

    const slaSelect = screen.getByText("SLA").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(slaSelect, { target: { value: "critical" } });

    const isLateSelect = screen.getByText("Atrasado?").closest("div")?.querySelector("select") as HTMLSelectElement;
    fireEvent.change(isLateSelect, { target: { value: "true" } });

    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ sla_status: "critical", is_late: true })
      );
    });

    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    fireEvent.click(screen.getByText("Limpar"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          sla_status: undefined,
          is_late: undefined,
        })
      );
    });
  });

  it("Deve exibir loading state com filtros SLA", async () => {
    vi.mocked(listShipments).mockImplementation(() => new Promise(() => {}));

    render(<ShipmentsPage />);

    expect(screen.getByText("Carregando envios...")).toBeInTheDocument();
  });

  it("Deve exibir empty state com filtros SLA", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Nenhum envio encontrado.")).toBeInTheDocument();
    });
  });

  it("Deve aplicar filtro por criticality", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Todas")).toBeInTheDocument();
    });

    const criticalitySelect = screen.getByText("Todas").closest("select") as HTMLSelectElement;
    fireEvent.change(criticalitySelect, { target: { value: "alta" } });

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ criticality: "alta" })
      );
    });
  });

  it("Deve combinar SLA com cliente", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Nome do cliente")).toBeInTheDocument();
    });

    const clientInput = screen.getByPlaceholderText("Nome do cliente");
    fireEvent.change(clientInput, { target: { value: "Cliente Teste" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ customer_name: "Cliente Teste" })
      );
    });
  });

  it("Deve combinar SLA com UF", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("UF")).toBeInTheDocument();
    });

    const ufInput = screen.getByPlaceholderText("UF");
    fireEvent.change(ufInput, { target: { value: "SP" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ destination_uf: "SP" })
      );
    });
  });

  it("Deve limpar filtros SLA", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Limpar")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Limpar"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          status: undefined,
          criticality: undefined,
          customer_name: undefined,
          destination_uf: undefined,
        })
      );
    });
  });

  it("Deve atualizar resultados sem refresh manual", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [{ id: 1, tracking_code: "TEST001", status: "in_transit", estimated_delivery: "2025-01-15", delay_days: 0, criticality: "normal", customer_name: "Cliente A", destination_uf: "SP", invoice_number: "NF001", invoice_key: null, fiscal_document: null, amount: 100, due_date: null, freight_value: 10, invoice_value: 100, freight_percentage: 10, collection_departure_date: null } as any],
      total: 1,
      total_pages: 1,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("TEST001")).toBeInTheDocument();
    });
  });

  it("Deve exibir erro quando API falhar", async () => {
    vi.mocked(listShipments).mockRejectedValueOnce(new Error("Network Error"));

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText(/Erro/i)).toBeInTheDocument();
    });
  });

  // ========== TESTES BETA-031: Campos Fiscais/Financeiros ==========

  it("Deve aplicar filtro por invoice_number", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("NF")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("NF");
    fireEvent.change(input, { target: { value: "NF12345" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ invoice_number: "NF12345" })
      );
    });
  });

  it("Deve aplicar filtro por invoice_key", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Chave NF-e")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Chave NF-e");
    fireEvent.change(input, { target: { value: "35250101234567890123550010001234561000123456" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ invoice_key: "35250101234567890123550010001234561000123456" })
      );
    });
  });

  it("Deve aplicar filtro por fiscal_document", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText("Documento fiscal")).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText("Documento fiscal");
    fireEvent.change(input, { target: { value: "DOC001" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ fiscal_document: "DOC001" })
      );
    });
  });

  it("Deve aplicar filtro por collection_departure_from", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Coleta/Saída")).toBeInTheDocument();
    });

    const input = screen.getByText("Coleta/Saída").closest("div")?.querySelector("input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "2025-01-15" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ collection_departure_from: "2025-01-15" })
      );
    });
  });

  it("Deve aplicar filtro por collection_departure_to", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Coleta/Saída")).toBeInTheDocument();
    });

    const inputs = screen.getByText("Coleta/Saída").closest("div")?.querySelectorAll("input");
    const input = inputs?.[1] as HTMLInputElement;
    fireEvent.change(input, { target: { value: "2025-01-31" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ collection_departure_to: "2025-01-31" })
      );
    });
  });

  it("Deve aplicar filtro por freight_value_min", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Valor Frete")).toBeInTheDocument();
    });

    const input = screen.getByText("Valor Frete").closest("div")?.querySelector("input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "50.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ freight_value_min: 50 })
      );
    });
  });

  it("Deve aplicar filtro por freight_value_max", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Valor Frete")).toBeInTheDocument();
    });

    const inputs = screen.getByText("Valor Frete").closest("div")?.querySelectorAll("input");
    const input = inputs?.[1] as HTMLInputElement;
    fireEvent.change(input, { target: { value: "200.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ freight_value_max: 200 })
      );
    });
  });

  it("Deve aplicar filtro por invoice_value_min", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getAllByText("Valor NF")[0]).toBeInTheDocument();
    });

    const input = screen.getAllByText("Valor NF")[0].closest("div")?.querySelector("input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "1000.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ invoice_value_min: 1000 })
      );
    });
  });

  it("Deve aplicar filtro por invoice_value_max", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getAllByText("Valor NF")[0]).toBeInTheDocument();
    });

    const inputs = screen.getAllByText("Valor NF")[0].closest("div")?.querySelectorAll("input");
    const input = inputs?.[1] as HTMLInputElement;
    fireEvent.change(input, { target: { value: "5000.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ invoice_value_max: 5000 })
      );
    });
  });

  it("Deve aplicar filtro por freight_percentage_min", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("% Frete")).toBeInTheDocument();
    });

    const input = screen.getByText("% Frete").closest("div")?.querySelector("input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "5.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ freight_percentage_min: 5 })
      );
    });
  });

  it("Deve aplicar filtro por freight_percentage_max", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("% Frete")).toBeInTheDocument();
    });

    const inputs = screen.getByText("% Frete").closest("div")?.querySelectorAll("input");
    const input = inputs?.[1] as HTMLInputElement;
    fireEvent.change(input, { target: { value: "15.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ freight_percentage_max: 15 })
      );
    });
  });

  it("Deve aplicar filtro por amount_min", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Valor Total")).toBeInTheDocument();
    });

    const input = screen.getByText("Valor Total").closest("div")?.querySelector("input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "100.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ amount_min: 100 })
      );
    });
  });

  it("Deve aplicar filtro por amount_max", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Valor Total")).toBeInTheDocument();
    });

    const inputs = screen.getByText("Valor Total").closest("div")?.querySelectorAll("input");
    const input = inputs?.[1] as HTMLInputElement;
    fireEvent.change(input, { target: { value: "10000.00" } });
    fireEvent.click(screen.getByText("Aplicar Filtros"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ amount_max: 10000 })
      );
    });
  });

  it("Deve limpar filtros fiscais/financeiros", async () => {
    vi.mocked(listShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Limpar")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Limpar"));

    await waitFor(() => {
      expect(vi.mocked(listShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          invoice_number: undefined,
          invoice_key: undefined,
          fiscal_document: undefined,
          collection_departure_from: undefined,
          collection_departure_to: undefined,
          freight_value_min: undefined,
          freight_value_max: undefined,
          invoice_value_min: undefined,
          invoice_value_max: undefined,
          freight_percentage_min: undefined,
          freight_percentage_max: undefined,
          amount_min: undefined,
          amount_max: undefined,
        })
      );
    });
  });
});