import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { CarrierEfficiencyCharts } from "./CarrierEfficiencyCharts";
import type { CarrierEfficiencyItem } from "@/lib/types";

const mockData: CarrierEfficiencyItem[] = [
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
  {
    carrier_id: 2,
    carrier_name: "Transportadora B",
    total_invoices: 5,
    total_shipments: 5,
    on_time_count: 3,
    on_time_percentage: 60,
    late_count: 2,
    late_percentage: 40,
    critical_count: 1,
    lost_count: 0,
    lost_percentage: 0,
    total_freight_value: 800,
    total_invoice_value: 5000,
    average_freight_percentage: 16,
    average_freight_value: 160,
    ranking_by_efficiency: 2,
    ranking_by_cost: 2,
    ranking_by_volume: 2,
  },
];

describe("CarrierEfficiencyCharts", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("Deve renderizar sem erros quando há dados", () => {
    render(<CarrierEfficiencyCharts data={mockData} />);

    expect(screen.getByText("Eficiência por Transportadora (%)")).toBeInTheDocument();
    expect(screen.getByText("Volume de Entregas vs Frete Total")).toBeInTheDocument();
    expect(screen.getByText("Rankings Comparativos")).toBeInTheDocument();
    expect(screen.getByText("Top 5 - Maior Eficiência (On-Time %)")).toBeInTheDocument();
  });

  it("Deve exibir mensagem quando não há dados", () => {
    render(<CarrierEfficiencyCharts data={[]} />);

    expect(screen.getByText("Sem dados para exibir gráficos")).toBeInTheDocument();
  });

  it("Deve exibir mensagem quando data é null", () => {
    render(<CarrierEfficiencyCharts data={null} />);

    expect(screen.getByText("Sem dados para exibir gráficos")).toBeInTheDocument();
  });

  it("Deve renderizar gráfico de eficiência com section header", () => {
    render(<CarrierEfficiencyCharts data={mockData} />);

    expect(screen.getByText("Eficiência por Transportadora (%)")).toBeInTheDocument();
  });

  it("Deve renderizar gráfico de volume com section header", () => {
    render(<CarrierEfficiencyCharts data={mockData} />);

    expect(screen.getByText("Volume de Entregas vs Frete Total")).toBeInTheDocument();
  });

  it("Deve renderizar rankings comparativos", () => {
    render(<CarrierEfficiencyCharts data={mockData} />);

    expect(screen.getByText("Rankings Comparativos")).toBeInTheDocument();
  });

  it("Deve renderizar top 5 eficiência ordenado", () => {
    render(<CarrierEfficiencyCharts data={mockData} />);

    expect(screen.getByText("Top 5 - Maior Eficiência (On-Time %)")).toBeInTheDocument();
  });

  it("Deve lidar com carrier_name null", () => {
    const dataWithNullName: CarrierEfficiencyItem[] = [
      {
        ...mockData[0],
        carrier_id: 99,
        carrier_name: null,
      },
    ];

    render(<CarrierEfficiencyCharts data={dataWithNullName} />);

    // O componente usa carrier_name || `ID ${carrier_id}` internamente
    // Verificamos se renderiza sem erro
    expect(screen.getByText("Top 5 - Maior Eficiência (On-Time %)")).toBeInTheDocument();
  });

  it("Deve lidar com múltiplas transportadoras (mais de 5) no top 5", () => {
    const manyCarriers: CarrierEfficiencyItem[] = Array.from({ length: 7 }, (_, i) => ({
      ...mockData[0],
      carrier_id: i + 10,
      carrier_name: `Transportadora ${i + 10}`,
      on_time_percentage: 90 - i * 5,
      ranking_by_efficiency: i + 1,
    }));

    render(<CarrierEfficiencyCharts data={manyCarriers} />);

    expect(screen.getByText("Top 5 - Maior Eficiência (On-Time %)")).toBeInTheDocument();
  });
});
