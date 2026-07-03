"use client";

import { useEffect, useState } from "react";
import { getCarrierEfficiency } from "@/lib/api";
import type { CarrierEfficiencyResponse, CarrierEfficiencyFilters } from "@/lib/types";
import { CarrierEfficiencyCharts } from "./CarrierEfficiencyCharts";
import { DateRangePicker } from "./DateRangePicker";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";

export default function CarrierEfficiencyPage() {
  const [data, setData] = useState<CarrierEfficiencyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<CarrierEfficiencyFilters & {
    estimated_delivery_from?: string;
    estimated_delivery_to?: string;
  }>({});
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem("accessToken") || "";
        const result = await getCarrierEfficiency(token, filters);
        setData(result);
        setError(null);
      } catch (err) {
        handleApiError(err instanceof Error ? err : new Error("Erro ao carregar dados"));
        setError(err instanceof Error ? err.message : "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filters, handleApiError]);

  const handleFilterChange = (key: keyof CarrierEfficiencyFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value === "" ? undefined : value,
    }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>Erro: {error}</div>;
  }

  if (!data || data.carriers.length === 0) {
    return <div>Sem dados</div>;
  }

  return (
    <div>
      <h1>Eficiência por Transportadora</h1>
      <p className="mt-1 text-sm text-zinc-600">
        Ranking: maior percentual no prazo; desempate por menor extravio, menor percentual médio de frete e nome.
        O percentual médio usa somente notas fiscais positivas com frete informado.
      </p>
      
      <div className="mb-4 p-4 bg-white rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-3">Filtros</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="filter-month" className="block text-sm font-medium mb-1">Mês</label>
            <input
              id="filter-month"
              type="number"
              min="1"
              max="12"
              className="w-full p-2 border rounded"
              value={filters.month || ""}
              onChange={(e) => handleFilterChange("month", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label htmlFor="filter-year" className="block text-sm font-medium mb-1">Ano</label>
            <input
              id="filter-year"
              type="number"
              min="2020"
              max="2030"
              className="w-full p-2 border rounded"
              value={filters.year || ""}
              onChange={(e) => handleFilterChange("year", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label htmlFor="filter-customer" className="block text-sm font-medium mb-1">Cliente</label>
            <input
              id="filter-customer"
              type="text"
              className="w-full p-2 border rounded"
              value={filters.customer_name || ""}
              onChange={(e) => handleFilterChange("customer_name", e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="filter-uf" className="block text-sm font-medium mb-1">UF</label>
            <input
              id="filter-uf"
              type="text"
              maxLength={2}
              className="w-full p-2 border rounded"
              value={filters.destination_uf || ""}
              onChange={(e) => handleFilterChange("destination_uf", e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="filter-carrier" className="block text-sm font-medium mb-1">Transportadora ID</label>
            <input
              id="filter-carrier"
              type="number"
              className="w-full p-2 border rounded"
              value={filters.carrier_id || ""}
              onChange={(e) => handleFilterChange("carrier_id", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label htmlFor="filter-status" className="block text-sm font-medium mb-1">Status</label>
            <input
              id="filter-status"
              type="text"
              className="w-full p-2 border rounded"
              value={filters.status || ""}
              onChange={(e) => handleFilterChange("status", e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="filter-criticality" className="block text-sm font-medium mb-1">Criticidade</label>
            <select
              id="filter-criticality"
              className="w-full p-2 border rounded"
              value={filters.criticality || ""}
              onChange={(e) => handleFilterChange("criticality", e.target.value)}
            >
              <option value="">Todas</option>
              <option value="normal">Normal</option>
              <option value="baixa">Baixa</option>
              <option value="media">Média</option>
              <option value="alta">Alta</option>
            </select>
          </div>
          <div>
            <label htmlFor="filter-sla-status" className="block text-sm font-medium mb-1">Status SLA</label>
            <select
              id="filter-sla-status"
              className="w-full p-2 border rounded"
              value={filters.sla_status || ""}
              onChange={(e) => handleFilterChange("sla_status", e.target.value)}
            >
              <option value="">Todos</option>
              <option value="on_time">No prazo</option>
              <option value="warning">Atenção</option>
              <option value="late">Atrasada</option>
              <option value="critical">Crítica</option>
              <option value="unknown">Sem SLA</option>
            </select>
          </div>
          <div>
            <label htmlFor="filter-is-late" className="block text-sm font-medium mb-1">Atrasada</label>
            <select
              id="filter-is-late"
              className="w-full p-2 border rounded"
              value={filters.is_late === undefined ? "" : filters.is_late.toString()}
              onChange={(e) => handleFilterChange("is_late", e.target.value === "" ? undefined : e.target.value === "true")}
            >
              <option value="">Todas</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <DateRangePicker
            label="Período de Entrega Estimada"
            value={{ from: filters.estimated_delivery_from, to: filters.estimated_delivery_to }}
            onChange={(v) => setFilters((prev) => ({ ...prev, ...v }))}
            placeholder={{ from: "Data inicial", to: "Data final" }}
          />
        </div>
        <button
          onClick={clearFilters}
          className="mt-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
        >
          Limpar Filtros
        </button>
      </div>

      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className="border p-2">Transportadora</th>
            <th className="border p-2">Total NFs</th>
            <th className="border p-2">Total Entregas</th>
            <th className="border p-2">No Prazo</th>
            <th className="border p-2">Atrasadas</th>
            <th className="border p-2">Frete Total</th>
            <th className="border p-2">Frete Médio</th>
            <th className="border p-2">Ranking Eficiência</th>
            <th className="border p-2">Ranking Custo</th>
            <th className="border p-2">Ranking Volume</th>
          </tr>
        </thead>
        <tbody>
          {data.carriers.map((carrier) => (
            <tr key={carrier.carrier_id}>
              <td className="border p-2">{carrier.carrier_name || "-"}</td>
              <td className="border p-2">{carrier.total_invoices}</td>
              <td className="border p-2">{carrier.total_shipments}</td>
              <td className="border p-2">{carrier.on_time_percentage}%</td>
              <td className="border p-2">{carrier.late_percentage}%</td>
              <td className="border p-2">R$ {carrier.total_freight_value.toFixed(2)}</td>
              <td className="border p-2">{carrier.average_freight_percentage}%</td>
              <td className="border p-2">{carrier.ranking_by_efficiency}</td>
              <td className="border p-2">{carrier.ranking_by_cost}</td>
              <td className="border p-2">{carrier.ranking_by_volume}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <CarrierEfficiencyCharts data={data?.carriers || []} />
    </div>
  );
}
