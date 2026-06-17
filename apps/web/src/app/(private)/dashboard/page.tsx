"use client";

import { useEffect, useState } from "react";
import { getDashboardSummary, getDashboardTrend } from "@/lib/dashboard-api";
import type { DashboardFilters, DashboardSummaryResponse, DashboardTrendResponse, DashboardTrendFilters } from "@/lib/types";
import { DateRangePicker } from "@/app/(private)/shipments/analytics/carrier-efficiency/DateRangePicker";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummaryResponse | null>(null);
  const [trendData, setTrendData] = useState<DashboardTrendResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [trendLoading, setTrendLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<DashboardFilters>({});
  const [trendFilters, setTrendFilters] = useState<DashboardTrendFilters>({});
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem("accessToken") || "";
        const result = await getDashboardSummary(token, filters);
        setData(result);
      } catch (err) {
        handleApiError(err instanceof Error ? err : new Error("Erro ao carregar dados"));
        setError(err instanceof Error ? err.message : "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filters, handleApiError]);

  useEffect(() => {
    const fetchTrendData = async () => {
      setTrendLoading(true);
      try {
        const token = localStorage.getItem("accessToken") || "";
        const result = await getDashboardTrend(token, trendFilters);
        setTrendData(result);
      } catch (err) {
        handleApiError(err instanceof Error ? err : new Error("Erro ao carregar tendência"));
        console.error("Erro ao carregar tendência:", err);
      } finally {
        setTrendLoading(false);
      }
    };

    fetchTrendData();
  }, [trendFilters, handleApiError]);

  const handleFilterChange = (key: keyof DashboardFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleTrendFilterChange = (key: keyof DashboardTrendFilters, value: string | number | undefined) => {
    setTrendFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  const clearTrendFilters = () => {
    setTrendFilters({});
  };

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-gray-500">Carregando...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="text-red-500">Erro: {error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="p-6">
        <div className="text-gray-500">Sem dados</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard Beta</h1>

      {/* Filtros */}
      <div className="mb-4 p-4 bg-white rounded-lg shadow" data-testid="dashboard-filters">
        <h2 className="text-lg font-semibold mb-3">Filtros</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Mês</label>
            <input
              aria-label="Mês"
              className="w-full p-2 border rounded"
              id="filter-month"
              max="12"
              min="1"
              type="number"
              value={filters.month ?? ""}
              onChange={(e) => handleFilterChange("month", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Ano</label>
            <input
              aria-label="Ano"
              className="w-full p-2 border rounded"
              id="filter-year"
              max="2100"
              min="2020"
              type="number"
              value={filters.year ?? ""}
              onChange={(e) => handleFilterChange("year", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Cliente</label>
            <input
              aria-label="Cliente"
              className="w-full p-2 border rounded"
              id="filter-customer"
              type="text"
              value={filters.customer_name ?? ""}
              onChange={(e) => handleFilterChange("customer_name", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">UF</label>
            <input
              aria-label="UF"
              className="w-full p-2 border rounded"
              id="filter-uf"
              maxLength={2}
              type="text"
              value={filters.destination_uf ?? ""}
              onChange={(e) => handleFilterChange("destination_uf", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Status SLA</label>
            <select
              aria-label="Status SLA"
              className="w-full p-2 border rounded"
              id="filter-sla-status"
              value={filters.sla_status ?? ""}
              onChange={(e) => handleFilterChange("sla_status", e.target.value)}
            >
              <option value="">Todos</option>
              <option value="on_time">No Prazo</option>
              <option value="late">Atrasada</option>
              <option value="critical">Crítica</option>
              <option value="warning">Atenção</option>
              <option value="unknown_sla">Sem SLA</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Atrasada</label>
            <select
              aria-label="Atrasada"
              className="w-full p-2 border rounded"
              id="filter-is-late"
              value={filters.is_late === undefined ? "" : String(filters.is_late)}
              onChange={(e) => handleFilterChange("is_late", e.target.value === "true" ? true : e.target.value === "false" ? false : undefined)}
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
        </div>
        <button
          data-testid="clear-main-filters"
          className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          onClick={clearFilters}
        >
          Limpar Filtros
        </button>
      </div>

      {/* Filtros de Período para Tendência */}
      <div className="mb-4 p-4 bg-white rounded-lg shadow" data-testid="dashboard-trend-filters">
        <h2 className="text-lg font-semibold mb-3">Período da Tendência</h2>
        <DateRangePicker
          label="Período de Entrega Estimada"
          value={{ from: trendFilters.estimated_delivery_from, to: trendFilters.estimated_delivery_to }}
          onChange={(v) => setTrendFilters((prev) => ({ ...prev, ...v }))}
          placeholder={{ from: "Data inicial", to: "Data final" }}
        />
        <div className="flex items-end gap-2 mt-3">
          <label className="block text-sm font-medium mb-1">Dias</label>
          <input
            type="number"
            min="1"
            max="90"
            className="w-24 p-2 border rounded"
            value={trendFilters.days ?? ""}
            onChange={(e) => handleTrendFilterChange("days", e.target.value ? parseInt(e.target.value) : undefined)}
          />
          <button
            className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            onClick={clearTrendFilters}
          >
            Limpar Filtros
          </button>
        </div>
      </div>

      {/* Cards de KPI */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6" data-testid="dashboard-kpi-cards">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-sm text-gray-500">Total</div>
          <div className="text-2xl font-bold">{data.total_shipments}</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg shadow border border-green-200">
          <div className="text-sm text-green-600">No Prazo</div>
          <div className="text-2xl font-bold text-green-600">{data.on_time_count}</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg shadow border border-orange-200">
          <div className="text-sm text-orange-600">Atrasadas</div>
          <div className="text-2xl font-bold text-orange-600">{data.late_count}</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg shadow border border-red-200">
          <div className="text-sm text-red-600">Críticas</div>
          <div className="text-2xl font-bold text-red-600">{data.critical_count}</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg shadow border border-yellow-200">
          <div className="text-sm text-yellow-600">Atenção</div>
          <div className="text-2xl font-bold text-yellow-600">{data.warning_count}</div>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg shadow border border-gray-200">
          <div className="text-sm text-gray-600">Sem SLA</div>
          <div className="text-2xl font-bold text-gray-600">{data.unknown_sla_count}</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg shadow border border-purple-200">
          <div className="text-sm text-purple-600">Exceções</div>
          <div className="text-2xl font-bold text-purple-600">{data.exceptions_count}</div>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg shadow border border-blue-200">
          <div className="text-sm text-blue-600">Transportadoras</div>
          <div className="text-2xl font-bold text-blue-600">{data.carriers_count}</div>
        </div>
        <div className="bg-indigo-50 p-4 rounded-lg shadow border border-indigo-200">
          <div className="text-sm text-indigo-600">Alertas Ativos</div>
          <div className="text-2xl font-bold text-indigo-600">
            {data.active_alerts_count === 0 ? "Nenhum alerta ativo" : data.active_alerts_count}
          </div>
          {data.active_alerts_count > 0 && (
            <a href="/alerts" className="text-sm text-indigo-800 hover:text-indigo-600 mt-1 block">
              Ver alertas →
            </a>
          )}
        </div>
        <div className="bg-pink-50 p-4 rounded-lg shadow border border-pink-200">
          <div className="text-sm text-pink-600">Falhas Importação</div>
          <div className="text-2xl font-bold text-pink-600">{data.import_failure_count}</div>
        </div>
      </div>

      {/* Gráficos de Tendência */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-3">Tendência dos KPIs (Últimos 30 dias)</h2>
        {trendLoading ? (
          <div className="p-6 text-center text-gray-500">Carregando tendências...</div>
        ) : trendData && trendData.trend_data && trendData.trend_data.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Total Shipments / On Time / Late / Critical / Warning */}
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-3">Total de Entregas por Dia</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData.trend_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={(v) => v.slice(5)} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="total_shipments" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} name="Total" />
                    <Line type="monotone" dataKey="on_time_count" stroke="#22c55e" strokeWidth={2} dot={{ r: 4 }} name="No Prazo" />
                    <Line type="monotone" dataKey="late_count" stroke="#ef4444" strokeWidth={2} dot={{ r: 4 }} name="Atrasadas" />
                    <Line type="monotone" dataKey="critical_count" stroke="#f97316" strokeWidth={2} dot={{ r: 4 }} name="Críticas" />
                    <Line type="monotone" dataKey="warning_count" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} name="Atenção" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Exceptions / Unknown SLA */}
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-3">Exceções e Sem SLA por Dia</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData.trend_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" tickFormatter={(v) => v.slice(5)} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="exceptions_count" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} name="Exceções" />
                    <Line type="monotone" dataKey="unknown_sla_count" stroke="#6b7280" strokeWidth={2} dot={{ r: 4 }} name="Sem SLA" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
            Sem dados de tendência para o período selecionado
          </div>
        )}
      </div>

      {/* Top Transportadoras por Eficiência */}
      <div className="mb-6 p-4 bg-white rounded-lg shadow" data-testid="top-carriers">
        <h2 className="text-lg font-semibold mb-3">Top Transportadoras por Eficiência</h2>
        {data.top_carriers_by_efficiency.length === 0 ? (
          <div className="text-gray-500">Nenhuma transportadora encontrada</div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-2">Transportadora</th>
                <th className="text-right p-2">Total</th>
                <th className="text-right p-2">No Prazo</th>
                <th className="text-right p-2">Atrasadas</th>
                <th className="text-right p-2">% No Prazo</th>
              </tr>
            </thead>
            <tbody>
              {data.top_carriers_by_efficiency.map((carrier) => (
                <tr key={carrier.carrier_id} className="border-b">
                  <td className="p-2">{carrier.carrier_name || "-"}</td>
                  <td className="text-right p-2">{carrier.total_shipments}</td>
                  <td className="text-right p-2">{carrier.on_time_count}</td>
                  <td className="text-right p-2">{carrier.late_count}</td>
                  <td className="text-right p-2">{carrier.on_time_percentage.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Top Exceções Priorizadas */}
      <div className="mb-6 p-4 bg-white rounded-lg shadow" data-testid="top-exceptions">
        <h2 className="text-lg font-semibold mb-3">Top Exceções Priorizadas</h2>
        {data.top_exceptions.length === 0 ? (
          <div className="text-gray-500">Nenhuma exceção encontrada</div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-2">Prioridade</th>
                <th className="text-left p-2">Tipo</th>
                <th className="text-left p-2">Motivo</th>
                <th className="text-left p-2">Rastreio</th>
                <th className="text-left p-2">NF</th>
                <th className="text-left p-2">Transportadora</th>
                <th className="text-left p-2">Cliente</th>
                <th className="text-left p-2">UF</th>
                <th className="text-left p-2">Status SLA</th>
                <th className="text-left p-2">Criticidade</th>
                <th className="text-right p-2">Atraso (dias)</th>
              </tr>
            </thead>
            <tbody>
              {data.top_exceptions.map((exc) => (
                <tr key={exc.shipment_id} className="border-b">
                  <td className="p-2">{exc.priority}</td>
                  <td className="p-2">{exc.exception_type || "-"}</td>
                  <td className="p-2">{exc.exception_reason || "-"}</td>
                  <td className="p-2">{exc.tracking_code}</td>
                  <td className="p-2">{exc.invoice_number || "-"}</td>
                  <td className="p-2">{exc.carrier_name || "-"}</td>
                  <td className="p-2">{exc.customer_name || "-"}</td>
                  <td className="p-2">{exc.destination_uf || "-"}</td>
                  <td className="p-2">{exc.sla_status}</td>
                  <td className="p-2">{exc.criticality}</td>
                  <td className="text-right p-2">{exc.delay_days}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Data de Geração */}
      <div className="text-sm text-gray-500">
        Gerado em: {data.generated_at ? new Date(data.generated_at).toLocaleString("pt-BR") : "-"}
      </div>
    </div>
  );
}
