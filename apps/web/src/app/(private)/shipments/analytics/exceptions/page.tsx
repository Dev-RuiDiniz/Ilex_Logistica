"use client";

import { useEffect, useState } from "react";
import { getExceptionsPanel, type ExceptionsPanelResponse, type ExceptionsPanelFilters } from "@/lib/exceptions-api";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";

export default function ExceptionsPanelPage() {
  const [data, setData] = useState<ExceptionsPanelResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ExceptionsPanelFilters>({});
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem("accessToken") || "";
        const result = await getExceptionsPanel(token, filters);
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

  const handleFilterChange = (key: keyof ExceptionsPanelFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleClearFilters = () => {
    setFilters({});
  };

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (loading) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Painel de Exceções</h1>
        <div className="text-gray-500">Carregando...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Painel de Exceções</h1>
        <div className="text-red-500">Erro: {error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Painel de Exceções</h1>
        <div className="text-gray-500">Sem dados</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Painel de Exceções</h1>

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-sm text-gray-500">Total</div>
          <div className="text-2xl font-bold">{data.summary.total_exceptions}</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg shadow border border-red-200">
          <div className="text-sm text-red-600">Críticas</div>
          <div className="text-2xl font-bold text-red-600">{data.summary.critical_count}</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg shadow border border-orange-200">
          <div className="text-sm text-orange-600">Atrasadas</div>
          <div className="text-2xl font-bold text-orange-600">{data.summary.late_count}</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg shadow border border-yellow-200">
          <div className="text-sm text-yellow-600">Atenção</div>
          <div className="text-2xl font-bold text-yellow-600">{data.summary.warning_count}</div>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg shadow border border-gray-200">
          <div className="text-sm text-gray-600">Sem SLA</div>
          <div className="text-2xl font-bold text-gray-600">{data.summary.unknown_sla_count}</div>
        </div>
      </div>

      {/* Filtros */}
      <div className="mb-4 p-4 bg-white rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-3">Filtros</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-month">
              Mês
            </label>
            <input
              id="filter-month"
              aria-label="Mês"
              className="w-full p-2 border rounded"
              type="number"
              min="1"
              max="12"
              value={filters.month ?? ""}
              onChange={(e) => handleFilterChange("month", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-year">
              Ano
            </label>
            <input
              id="filter-year"
              aria-label="Ano"
              className="w-full p-2 border rounded"
              type="number"
              min="2020"
              max="2030"
              value={filters.year ?? ""}
              onChange={(e) => handleFilterChange("year", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-customer">
              Cliente
            </label>
            <input
              id="filter-customer"
              aria-label="Cliente"
              className="w-full p-2 border rounded"
              type="text"
              value={filters.customer_name ?? ""}
              onChange={(e) => handleFilterChange("customer_name", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-uf">
              UF
            </label>
            <input
              id="filter-uf"
              aria-label="UF"
              className="w-full p-2 border rounded"
              type="text"
              maxLength={2}
              value={filters.destination_uf ?? ""}
              onChange={(e) => handleFilterChange("destination_uf", e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-carrier">
              Transportadora ID
            </label>
            <input
              id="filter-carrier"
              aria-label="Transportadora ID"
              className="w-full p-2 border rounded"
              type="number"
              value={filters.carrier_id ?? ""}
              onChange={(e) => handleFilterChange("carrier_id", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-criticality">
              Criticidade
            </label>
            <select
              id="filter-criticality"
              aria-label="Criticidade"
              className="w-full p-2 border rounded"
              value={filters.criticality ?? ""}
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
            <label className="block text-sm font-medium mb-1" htmlFor="filter-sla-status">
              Status SLA
            </label>
            <select
              id="filter-sla-status"
              aria-label="Status SLA"
              className="w-full p-2 border rounded"
              value={filters.sla_status ?? ""}
              onChange={(e) => handleFilterChange("sla_status", e.target.value)}
            >
              <option value="">Todos</option>
              <option value="on_time">No prazo</option>
              <option value="warning">Atenção</option>
              <option value="late">Atrasada</option>
              <option value="critical">Crítica</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-exception-type">
              Tipo de Exceção
            </label>
            <select
              id="filter-exception-type"
              aria-label="Tipo de Exceção"
              className="w-full p-2 border rounded"
              value={filters.exception_type ?? ""}
              onChange={(e) => handleFilterChange("exception_type", e.target.value)}
            >
              <option value="">Todos</option>
              <option value="critical">Crítica</option>
              <option value="late">Atrasada</option>
              <option value="warning">Atenção</option>
              <option value="unknown_sla">Sem SLA</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="filter-is-late">
              Atrasada
            </label>
            <select
              id="filter-is-late"
              aria-label="Atrasada"
              className="w-full p-2 border rounded"
              value={filters.is_late === undefined ? "" : String(filters.is_late)}
              onChange={(e) => handleFilterChange("is_late", e.target.value === "true" ? true : e.target.value === "false" ? false : undefined)}
            >
              <option value="">Todas</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
        </div>
        <button
          className="mt-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
          onClick={handleClearFilters}
        >
          Limpar Filtros
        </button>
      </div>

      {/* Tabela de Exceções */}
      {data.items.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-medium">Prioridade</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Tipo</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Motivo</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Rastreio</th>
                <th className="px-4 py-2 text-left text-sm font-medium">NF</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Transportadora</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Cliente</th>
                <th className="px-4 py-2 text-left text-sm font-medium">UF</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Status</th>
                <th className="px-4 py-2 text-left text-sm font-medium">SLA</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Criticidade</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Atraso (dias)</th>
                <th className="px-4 py-2 text-left text-sm font-medium">Prazo SLA</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((item) => (
                <tr key={item.shipment_id} className="border-b">
                  <td className="px-4 py-2 text-sm">{item.priority}</td>
                  <td className="px-4 py-2 text-sm">
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        item.exception_type === "critical"
                          ? "bg-red-100 text-red-800"
                          : item.exception_type === "late"
                          ? "bg-orange-100 text-orange-800"
                          : item.exception_type === "warning"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {item.exception_type}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-sm">{item.exception_reason}</td>
                  <td className="px-4 py-2 text-sm">{item.tracking_code}</td>
                  <td className="px-4 py-2 text-sm">{item.invoice_number || "-"}</td>
                  <td className="px-4 py-2 text-sm">{item.carrier_name || "-"}</td>
                  <td className="px-4 py-2 text-sm">{item.customer_name || "-"}</td>
                  <td className="px-4 py-2 text-sm">{item.destination_uf || "-"}</td>
                  <td className="px-4 py-2 text-sm">{item.status}</td>
                  <td className="px-4 py-2 text-sm">{item.sla_status || "-"}</td>
                  <td className="px-4 py-2 text-sm">{item.criticality}</td>
                  <td className="px-4 py-2 text-sm">{item.delay_days}</td>
                  <td className="px-4 py-2 text-sm">{item.sla_due_date ? new Date(item.sla_due_date).toLocaleDateString() : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
