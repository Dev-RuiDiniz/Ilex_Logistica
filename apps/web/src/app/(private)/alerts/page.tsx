"use client";

import { useState, useEffect } from "react";
import {
  getAlerts,
  getAlertsSummary,
  generateAlerts,
  markAlertAsRead,
  resolveAlert,
  type AlertsFilters,
  type AlertItem,
  type AlertsSummary,
} from "@/lib/alerts-api";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [summary, setSummary] = useState<AlertsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<AlertsFilters>({});
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      setError(null);
      const [alertsData, summaryData] = await Promise.all([
        getAlerts(filters),
        getAlertsSummary(),
      ]);
      setAlerts(alertsData.alerts);
      setSummary(summaryData);
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      handleApiError(error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAlerts = async () => {
    try {
      await generateAlerts();
      await fetchAlerts();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      handleApiError(error);
      setError(error.message);
    }
  };

  const handleMarkAsRead = async (alertId: number) => {
    try {
      await markAlertAsRead(alertId);
      await fetchAlerts();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      handleApiError(error);
      setError(error.message);
    }
  };

  const handleResolve = async (alertId: number) => {
    try {
      await resolveAlert(alertId);
      await fetchAlerts();
    } catch (err) {
      const error = err instanceof Error ? err : new Error(String(err));
      handleApiError(error);
      setError(error.message);
    }
  };

  const handleFilterChange = (key: keyof AlertsFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleClearFilters = () => {
    setFilters({});
  };

  useEffect(() => {
    fetchAlerts();
  }, [filters]);

  const getSeverityBadge = (severity: string) => {
    const map: Record<string, string> = {
      critical: "bg-red-50 text-red-700 ring-1 ring-red-600/20",
      warning: "bg-orange-50 text-orange-700 ring-1 ring-orange-600/20",
      info: "bg-blue-50 text-blue-700 ring-1 ring-blue-600/20",
    };
    return map[severity] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20";
  };

  const getStatusBadge = (status: string, isRead: boolean) => {
    const map: Record<string, string> = {
      active: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20",
      resolved: "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20",
      read: "bg-blue-50 text-blue-700 ring-1 ring-blue-600/20",
    };
    return map[status] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20";
  };

  const selectClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20";

  return (
    <section className="space-y-6">
      {/* Header */}
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Alertas</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Monitoramento de alertas operacionais</p>
        </div>
        <button
          data-testid="generate-alerts-button"
          onClick={handleGenerateAlerts}
          className="rounded-lg bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800"
        >
          Gerar Alertas
        </button>
      </header>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
          <div className="rounded-2xl border border-zinc-200 bg-white p-4 text-center shadow-sm">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-zinc-900">{summary.total_alerts}</p>
          </div>
          <div className="rounded-2xl border border-blue-100 bg-blue-50 p-4 text-center">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-blue-600/70">Ativos</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-blue-600">{summary.active_count}</p>
          </div>
          <div className="rounded-2xl border border-amber-100 bg-amber-50 p-4 text-center">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Não Lidos</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-amber-600">{summary.total_alerts - summary.read_count}</p>
          </div>
          <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-4 text-center">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70">Resolvidos</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-emerald-600">{summary.resolved_count}</p>
          </div>
          <div className="rounded-2xl border border-red-100 bg-red-50 p-4 text-center">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Críticos</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-red-600">{summary.critical_count}</p>
          </div>
          <div className="rounded-2xl border border-orange-100 bg-orange-50 p-4 text-center">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-orange-600/70">Warnings</p>
            <p className="mt-1 text-2xl font-extrabold tabular-nums text-orange-600">{summary.warning_count}</p>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
        <p className="mb-3 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Filtros</p>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
          <div>
            <label className="block text-[11px] font-semibold text-zinc-500">Status</label>
            <select
              className={selectClass}
              value={filters.status || ""}
              onChange={(e) => handleFilterChange("status", e.target.value || undefined)}
            >
              <option value="">Todos</option>
              <option value="active">Ativo</option>
              <option value="read">Lido</option>
              <option value="resolved">Resolvido</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-zinc-500">Severidade</label>
            <select
              className={selectClass}
              value={filters.severity || ""}
              onChange={(e) => handleFilterChange("severity", e.target.value || undefined)}
            >
              <option value="">Todas</option>
              <option value="critical">Crítico</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-zinc-500">Tipo</label>
            <select
              className={selectClass}
              value={filters.alert_type || ""}
              onChange={(e) => handleFilterChange("alert_type", e.target.value || undefined)}
            >
              <option value="">Todos</option>
              <option value="sla_critical">SLA Crítico</option>
              <option value="sla_late">SLA Atrasado</option>
              <option value="sla_warning">SLA Warning</option>
              <option value="unknown_sla">SLA Desconhecido</option>
              <option value="import_failure">Falha de Importação</option>
              <option value="no_update">Sem Atualização</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-zinc-500">Lido</label>
            <select
              className={selectClass}
              value={filters.is_read === undefined ? "" : String(filters.is_read)}
              onChange={(e) => handleFilterChange("is_read", e.target.value === "" ? undefined : e.target.value === "true")}
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-zinc-500">Resolvido</label>
            <select
              className={selectClass}
              value={filters.is_resolved === undefined ? "" : String(filters.is_resolved)}
              onChange={(e) => handleFilterChange("is_resolved", e.target.value === "" ? undefined : e.target.value === "true")}
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <div className="flex items-end">
            <button
              data-testid="clear-filters-button"
              onClick={handleClearFilters}
              className="w-full rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
            >
              Limpar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center rounded-2xl border border-zinc-200 bg-white p-12 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
            <p className="text-sm font-medium text-zinc-500">Carregando alertas...</p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          Erro: {error}
        </div>
      )}

      {/* Alerts Table */}
      {!loading && !error && summary && (
        <>
          {alerts.length === 0 ? (
            <div className="rounded-2xl border border-zinc-200 bg-white p-12 text-center shadow-sm">
              <svg className="mx-auto h-12 w-12 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              <p className="mt-3 text-sm font-medium text-zinc-500">Nenhum alerta encontrado</p>
            </div>
          ) : (
            <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-zinc-100 bg-zinc-50/80">
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Severidade</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Tipo</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Título</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Mensagem</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Origem</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Gerado em</th>
                      <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {alerts.map((alert) => (
                      <tr
                        key={alert.id}
                        className={`border-b border-zinc-50 transition-colors hover:bg-zinc-50/50 ${
                          alert.is_resolved ? "bg-zinc-50/30" : ""
                        }`}
                      >
                        <td className="px-4 py-3">
                          <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold capitalize ${getSeverityBadge(alert.severity)}`}>
                            {alert.severity}
                          </span>
                        </td>
                        <td className="px-4 py-3 font-mono text-xs text-zinc-600">{alert.alert_type}</td>
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-1.5">
                            <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold capitalize ${getStatusBadge(alert.status, alert.is_read)}`}>
                              {alert.status}
                            </span>
                            {!alert.is_read && (
                              <span className="inline-block h-1.5 w-1.5 rounded-full bg-amber-500" title="Não lido" />
                            )}
                          </div>
                        </td>
                        <td className="px-4 py-3 font-semibold text-zinc-900">{alert.title}</td>
                        <td className="px-4 py-3 text-zinc-600">{alert.message}</td>
                        <td className="px-4 py-3 text-xs text-zinc-500">
                          {alert.source_type} {alert.source_id}
                        </td>
                        <td className="px-4 py-3 text-xs text-zinc-500">
                          {new Date(alert.generated_at).toLocaleString("pt-BR")}
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex justify-end gap-2">
                            {!alert.is_read && (
                              <button
                                data-testid={`mark-read-button-${alert.id}`}
                                onClick={() => handleMarkAsRead(alert.id)}
                                className="rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
                              >
                                Marcar lido
                              </button>
                            )}
                            {!alert.is_resolved && (
                              <button
                                data-testid={`resolve-button-${alert.id}`}
                                onClick={() => handleResolve(alert.id)}
                                className="rounded-lg bg-emerald-600 px-3 py-1.5 text-xs font-semibold text-white transition-all hover:bg-emerald-700"
                              >
                                Resolver
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </section>
  );
}
