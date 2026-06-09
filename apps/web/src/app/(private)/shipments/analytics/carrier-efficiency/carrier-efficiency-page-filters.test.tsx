import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import CarrierEfficiencyPage from "./page";
import * as api from "@/lib/api";

vi.mock("@/lib/api");

describe("CarrierEfficiencyPage - Interacao de Filtros", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it("Deve chamar a API inicial sem filtros vazios", async () => {
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

    expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledWith(
      expect.any(String),
      {}
    );
  });

  it("Deve alterar filtro de mês e refazer a consulta", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const monthInput = screen.getByLabelText(/Mês/i);
    fireEvent.change(monthInput, { target: { value: "1" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ month: 1 });
  });

  it("Deve alterar filtro de UF e refazer a consulta", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const ufInput = screen.getByLabelText(/UF/i);
    fireEvent.change(ufInput, { target: { value: "SP" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ destination_uf: "SP" });
  });

  it("Deve alterar filtro de transportadora e refazer a consulta", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const carrierInput = screen.getByLabelText(/Transportadora ID/i);
    fireEvent.change(carrierInput, { target: { value: "1" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ carrier_id: 1 });
  });

  it("Deve alterar filtro de criticality e refazer a consulta", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const criticalitySelect = screen.getByLabelText(/Criticidade/i);
    fireEvent.change(criticalitySelect, { target: { value: "alta" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ criticality: "alta" });
  });

  it("Deve alterar filtro de sla_status e refazer a consulta", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
        generated_at: "2025-01-01T00:00:00:00Z",
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const slaStatusSelect = screen.getByLabelText(/Status SLA/i);
    fireEvent.change(slaStatusSelect, { target: { value: "late" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ sla_status: "late" });
  });

  it("Deve alterar filtro de is_late e refazer a consulta serializando boolean corretamente", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
        generated_at: "2025-01-01T00:00:00:00Z",
      })
      .mockResolvedValueOnce({
        carriers: [],
        generated_at: "2025-01-01T00:00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const isLateSelect = screen.getByLabelText(/Atrasada/i);
    fireEvent.change(isLateSelect, { target: { value: "true" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const lastCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(lastCall[1]).toEqual({ is_late: true });
  });

  it("Deve limpar filtros e refazer a consulta sem query params", async () => {
    vi.mocked(api.getCarrierEfficiency)
      .mockResolvedValueOnce({
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
      })
      .mockResolvedValueOnce({
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
        generated_at: "2025-01-01T00:00:00:00Z",
      });

    render(<CarrierEfficiencyPage />);

    await screen.findByText("Transportadora A");

    const monthInput = screen.getByLabelText(/Mês/i);
    fireEvent.change(monthInput, { target: { value: "1" } });

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(2);
    });

    const secondCall = vi.mocked(api.getCarrierEfficiency).mock.calls[1];
    expect(secondCall[1]).toEqual({ month: 1 });

    const clearButtons = screen.getAllByText(/Limpar Filtros/i);
    fireEvent.click(clearButtons[0]);

    await waitFor(() => {
      expect(vi.mocked(api.getCarrierEfficiency)).toHaveBeenCalledTimes(3);
    });

    const thirdCall = vi.mocked(api.getCarrierEfficiency).mock.calls[2];
    expect(thirdCall[1]).toEqual({});
  });
});
