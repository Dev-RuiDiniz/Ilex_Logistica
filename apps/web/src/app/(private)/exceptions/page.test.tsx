import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { listExceptionShipments } from "@/lib/api";
import ExceptionsPage from "./page";
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

describe("ExceptionsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession });
  });

  it("Deve renderizar loading", async () => {
    vi.mocked(listExceptionShipments).mockImplementation(() => new Promise(() => {}));

    render(<ExceptionsPage />);

    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("Deve renderizar erro de API", async () => {
    vi.mocked(listExceptionShipments).mockRejectedValueOnce(new Error("API Error"));

    render(<ExceptionsPage />);

    await waitFor(() => {
      expect(screen.getByText("API Error")).toBeInTheDocument();
    });
  });

  it("Deve renderizar estado vazio", async () => {
    vi.mocked(listExceptionShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ExceptionsPage />);

    await waitFor(() => {
      expect(screen.getByText("Sem exceções no momento.")).toBeInTheDocument();
    });
  });

  it("Deve aplicar filtro por criticality", async () => {
    vi.mocked(listExceptionShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ExceptionsPage />);

    await waitFor(() => {
      expect(screen.getByText("Todas")).toBeInTheDocument();
    });

    const criticalitySelect = screen.getByText("Todas").closest("select") as HTMLSelectElement;
    fireEvent.change(criticalitySelect, { target: { value: "alta" } });

    await waitFor(() => {
      expect(vi.mocked(listExceptionShipments)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({ criticality: "alta" })
      );
    });
  });

  it("Deve listar exceções com dados corretos", async () => {
    vi.mocked(listExceptionShipments).mockResolvedValueOnce({
      items: [
        {
          id: 1,
          tracking_code: "TRACK001",
          status: "in_transit",
          delay_days: 5,
          criticality: "alta",
          customer_name: "Cliente A",
          destination_uf: "SP",
          invoice_number: "NF001",
          invoice_key: null,
          fiscal_document: null,
          amount: 100,
          due_date: null,
          freight_value: 10,
          invoice_value: 100,
          freight_percentage: 10,
          collection_departure_date: null,
          estimated_delivery: "2025-01-15",
        },
        {
          id: 2,
          tracking_code: "TRACK002",
          status: "in_transit",
          delay_days: 2,
          criticality: "media",
          customer_name: "Cliente B",
          destination_uf: "RJ",
          invoice_number: "NF002",
          invoice_key: null,
          fiscal_document: null,
          amount: 200,
          due_date: null,
          freight_value: 20,
          invoice_value: 200,
          freight_percentage: 10,
          collection_departure_date: null,
          estimated_delivery: "2025-01-20",
        },
      ],
      total: 2,
      total_pages: 1,
      page: 1,
      page_size: 20,
    });

    render(<ExceptionsPage />);

    await waitFor(() => {
      expect(screen.getByText("TRACK001")).toBeInTheDocument();
      expect(screen.getByText("TRACK002")).toBeInTheDocument();
      expect(screen.getByText("5")).toBeInTheDocument(); // delay_days
      expect(screen.getByText("alta")).toBeInTheDocument();
      expect(screen.getByText("media")).toBeInTheDocument();
    });
  });

  it("Deve atualizar resultados quando criticality muda", async () => {
    vi.mocked(listExceptionShipments).mockResolvedValueOnce({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });

    render(<ExceptionsPage />);

    await waitFor(() => {
      expect(screen.getByText("Todas")).toBeInTheDocument();
    });

    const criticalitySelect = screen.getByText("Todas").closest("select") as HTMLSelectElement;
    fireEvent.change(criticalitySelect, { target: { value: "baixa" } });

    await waitFor(() => {
      expect(vi.mocked(listExceptionShipments)).toHaveBeenCalledTimes(2);
      expect(vi.mocked(listExceptionShipments)).toHaveBeenLastCalledWith(
        "test-token",
        expect.objectContaining({ criticality: "baixa" })
      );
    });
  });
});