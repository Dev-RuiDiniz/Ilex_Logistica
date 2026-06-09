import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import CarrierEfficiencyPage from "./page";
import * as api from "@/lib/api";

vi.mock("@/lib/api");

describe("CarrierEfficiencyPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it("Deve renderizar estado loading", () => {
    vi.mocked(api.getCarrierEfficiency).mockImplementation(() => new Promise(() => {}));

    render(<CarrierEfficiencyPage />);

    expect(screen.getByText(/carregando/i)).toBeInTheDocument();
  });

  it("Deve renderizar estado vazio", async () => {
    vi.mocked(api.getCarrierEfficiency).mockResolvedValueOnce({
      carriers: [],
      generated_at: "2025-01-01T00:00:00Z",
    });

    render(<CarrierEfficiencyPage />);

    await screen.findByText(/sem dados/i);
  });

  it("Deve renderizar erro de API", async () => {
    vi.mocked(api.getCarrierEfficiency).mockRejectedValueOnce(new Error("Erro de API"));

    render(<CarrierEfficiencyPage />);

    await screen.findByText(/erro/i);
  });

  it("Deve renderizar tabela de transportadoras", async () => {
    vi.mocked(api.getCarrierEfficiency).mockResolvedValueOnce({
      carriers: [
        {
          carrier_id: 1,
          carrier_name: "Transportadora A",
          total_invoices: 10,
          total_shipments: 10,
          on_time_count: 8,
          on_time_percentage: 80,
          late_count: 2,
          late_percentage: 20,
          critical_count: 0,
          lost_count: 0,
          lost_percentage: 0,
          total_freight_value: 1000,
          total_invoice_value: 10000,
          average_freight_percentage: 10,
          average_freight_value: 100,
          ranking_by_efficiency: 1,
          ranking_by_cost: 1,
          ranking_by_volume: 1,
        },
      ],
      generated_at: "2025-01-01T00:00:00Z",
    });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");
    expect(screen.getByText(/Total NFs/i)).toBeInTheDocument();
    expect(screen.getByText(/Total Entregas/i)).toBeInTheDocument();
    expect(screen.getByText(/No Prazo/i)).toBeInTheDocument();
    expect(screen.getByText(/Atrasadas/i)).toBeInTheDocument();
    expect(screen.getByText(/Frete Total/i)).toBeInTheDocument();
    expect(screen.getByText(/Frete Médio/i)).toBeInTheDocument();
    expect(screen.getByText(/Ranking Eficiência/i)).toBeInTheDocument();
    expect(screen.getByText(/Ranking Custo/i)).toBeInTheDocument();
    expect(screen.getByText(/Ranking Volume/i)).toBeInTheDocument();
  });

  it("Deve tratar ausência de extraviadas como zero", async () => {
    vi.mocked(api.getCarrierEfficiency).mockResolvedValueOnce({
      carriers: [
        {
          carrier_id: 1,
          carrier_name: "Transportadora A",
          total_invoices: 10,
          total_shipments: 10,
          on_time_count: 8,
          on_time_percentage: 80,
          late_count: 2,
          late_percentage: 20,
          critical_count: 0,
          lost_count: 0,
          lost_percentage: 0,
          total_freight_value: 1000,
          total_invoice_value: 10000,
          average_freight_percentage: 10,
          average_freight_value: 100,
          ranking_by_efficiency: 1,
          ranking_by_cost: 1,
          ranking_by_volume: 1,
        },
      ],
      generated_at: "2025-01-01T00:00:00Z",
    });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");
  });
});
