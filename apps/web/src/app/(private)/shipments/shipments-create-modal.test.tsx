import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import { listShipments, listCarriers, createShipment } from "@/lib/api";
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
  role: "admin",
};

describe("Shipments create modal", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAuth).mockReturnValue({ session: mockSession });
    vi.mocked(listShipments).mockResolvedValue({
      items: [],
      total: 0,
      total_pages: 0,
      page: 1,
      page_size: 20,
    });
    vi.mocked(listCarriers).mockResolvedValue([
      { id: 1, name: "Transportes A", external_code: null, integration_metadata: {}, is_active: true },
    ]);
    vi.mocked(createShipment).mockResolvedValue({
      id: 1,
      tracking_code: "TRK-NEW-001",
      carrier_id: 1,
      status: "pending",
      estimated_delivery: "2026-07-10T10:00:00",
      actual_delivery: null,
      recipient_name: "João Silva",
      recipient_phone: "11999999999",
      origin_address: "Rua A",
      destination_address: "Rua B",
      meta_data: {},
      is_active: true,
      created_at: "2026-07-01T00:00:00",
      updated_at: "2026-07-01T00:00:00",
      invoice_number: null,
      invoice_key: null,
      fiscal_document: null,
      amount: null,
      due_date: null,
      delay_days: 0,
      criticality: "normal",
      freight_value: null,
      invoice_value: null,
      freight_percentage: null,
      collection_departure_date: null,
      customer_name: null,
      destination_uf: null,
    });
  });

  it("Deve exibir botão Novo envio para perfil com permissão de escrita", async () => {
    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Novo envio")).toBeInTheDocument();
    });
  });

  it("Deve abrir modal ao clicar em Novo envio", async () => {
    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Novo envio")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Novo envio"));

    await waitFor(() => {
      expect(screen.getByText(/Código de rastreio/)).toBeInTheDocument();
    });
  });

  it("Deve chamar createShipment ao submeter formulário", async () => {
    render(<ShipmentsPage />);

    await waitFor(() => {
      expect(screen.getByText("Novo envio")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Novo envio"));

    await waitFor(() => {
      expect(screen.getByText(/Código de rastreio/)).toBeInTheDocument();
    });

    fireEvent.change(screen.getByPlaceholderText("Ex: BR123456789"), { target: { value: "TRK-NEW-001" } });
    fireEvent.change(screen.getByText(/Transportadora/).closest("div")?.querySelector("select") as HTMLSelectElement, { target: { value: "1" } });
    fireEvent.change(screen.getByText(/Endereço origem/).closest("div")?.querySelector("input") as HTMLInputElement, { target: { value: "Rua A" } });
    fireEvent.change(screen.getByText(/Endereço destino/).closest("div")?.querySelector("input") as HTMLInputElement, { target: { value: "Rua B" } });
    fireEvent.change(screen.getByText(/Destinatário/).closest("div")?.querySelector("input") as HTMLInputElement, { target: { value: "João Silva" } });
    fireEvent.change(screen.getByText(/Telefone destinatário/).closest("div")?.querySelector("input") as HTMLInputElement, { target: { value: "11999999999" } });

    fireEvent.click(screen.getByText("Salvar envio"));

    await waitFor(() => {
      expect(vi.mocked(createShipment)).toHaveBeenCalledWith(
        "test-token",
        expect.objectContaining({
          tracking_code: "TRK-NEW-001",
          carrier_id: 1,
          origin_address: "Rua A",
          destination_address: "Rua B",
          recipient_name: "João Silva",
          recipient_phone: "11999999999",
        })
      );
    });
  });
});
