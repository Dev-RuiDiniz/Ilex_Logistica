"use client";

import { useState, useEffect, useCallback } from "react";
import {
  getAuditLogs,
  getAuditSummary,
  type AuditLog,
  type AuditLogFilters,
  type AuditLogSummaryResponse,
  type AuditSeverity,
  type AuditStatus,
} from "@/lib/audit-api";
import { AuditSeverityBadge } from "@/components/AuditSeverityBadge";
import { AuditStatusBadge } from "@/components/AuditStatusBadge";
import { AuditJsonViewer } from "@/components/AuditJsonViewer";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";

export default function AuditPage() {
  const { session } = useAuth();
  const token = session?.accessToken;
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [summary, setSummary] = useState<AuditLogSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);
  const [filters, setFilters] = useState<AuditLogFilters>({ page: 1, page_size: 50 });
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  const fetchLogs = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError(null);
    try {
      const response = await getAuditLogs(token, filters);
      setLogs(response.logs);
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar logs"));
      setError(err instanceof Error ? err.message : "Erro ao carregar logs");
    } finally {
      setLoading(false);
    }
  }, [token, filters, handleApiError]);

  const fetchSummary = useCallback(async () => {
    if (!token) return;
    try {
      const data = await getAuditSummary(token);
      setSummary(data);
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar resumo"));
      console.error("Erro ao carregar summary:", err);
      const errorMessage = handleApiError(err);
      if (errorMessage.includes("Sessão expirada")) return;
    }
  }, [token, handleApiError]);

  useEffect(() => {
    const init = async () => {
      await fetchLogs();
      await fetchSummary();
    };
    init();
  }, [token]);

  const handleFilterChange = (key: keyof AuditLogFilters, value: string | number | undefined) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
  };

  const clearFilters = () => {
    setFilters({ page: 1, page_size: 50 });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString("pt-BR");
  };

  const selectClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20";
  const inputClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800";
  const btnSecondary = "rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50";

  return (
    <section className="space-y-6">
      {/* Header */}
      <header>
        <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Auditoria Operacional</h1>
        <p className="mt-1 text-sm font-medium text-zinc-500">Logs de eventos e ações do sistema</p>
      </header>

      {/* Loading */}
      {loading && logs.length === 0 && (
        <div data-testid="audit-page" className="flex items-center justify-center rounded-2xl border border-zinc-200 bg-white p-12 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
            <p className="text-sm font-medium text-zinc-500">Carregando logs...</p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div data-testid="audit-error-state" className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Summary Cards */}
          {summary && (
            <div data-testid="audit-summary" className="grid grid-cols-2 gap-4 lg:grid-cols-4">
              <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total de Logs</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-zinc-900">{summary.total_logs}</p>
              </div>
              <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-5">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70">Sucesso</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-emerald-600">{summary.success_count}</p>
              </div>
              <div className="rounded-2xl border border-red-100 bg-red-50 p-5">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Falhas</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-red-600">{summary.failed_count}</p>
              </div>
              <div className="rounded-2xl border border-red-200 bg-red-100 p-5">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-red-700/70">Críticos</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-red-700">{summary.critical_count}</p>
              </div>
            </div>
          )}

          {/* Filters */}
          <div data-testid="audit-filters" className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
            <p className="mb-4 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Filtros</p>
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Event Type</label>
                <input
                  type="text"
                  value={filters.event_type || ""}
                  onChange={(e) => handleFilterChange("event_type", e.target.value || undefined)}
                  placeholder="Ex: daily_report_generated"
                  className={inputClass}
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Entity Type</label>
                <input
                  type="text"
                  value={filters.entity_type || ""}
                  onChange={(e) => handleFilterChange("entity_type", e.target.value || undefined)}
                  placeholder="Ex: shipment"
                  className={inputClass}
                />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Severidade</label>
                <select
                  value={filters.severity || ""}
                  onChange={(e) => handleFilterChange("severity", e.target.value as AuditSeverity | undefined)}
                  className={selectClass}
                >
                  <option value="">Todos</option>
                  <option value="info">Info</option>
                  <option value="warning">Warning</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Status</label>
                <select
                  value={filters.status || ""}
                  onChange={(e) => handleFilterChange("status", e.target.value as AuditStatus | undefined)}
                  className={selectClass}
                >
                  <option value="">Todos</option>
                  <option value="success">Success</option>
                  <option value="failed">Failed</option>
                  <option value="skipped">Skipped</option>
                </select>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <button onClick={() => fetchLogs()} className={btnPrimary}>
                Aplicar Filtros
              </button>
              <button onClick={clearFilters} className={btnSecondary}>
                Limpar Filtros
              </button>
            </div>
          </div>

          {/* Logs Table */}
          {logs.length === 0 ? (
            <div data-testid="audit-empty-state" className="flex flex-col items-center justify-center rounded-2xl border border-zinc-200 bg-white p-12 shadow-sm">
              <svg className="h-12 w-12 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
              </svg>
              <p className="mt-3 text-sm font-medium text-zinc-500">Nenhum log encontrado</p>
            </div>
          ) : (
            <div data-testid="audit-log-table" className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-zinc-100 bg-zinc-50/80">
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Data</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Event Type</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Action</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Entity</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Severidade</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Actor</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Message</th>
                    </tr>
                  </thead>
                  <tbody>
                    {logs.map((log) => (
                      <tr
                        key={log.id}
                        data-testid="audit-log-row"
                        className="cursor-pointer border-b border-zinc-50 transition-colors hover:bg-zinc-50/50"
                        onClick={() => setSelectedLog(log)}
                      >
                        <td className="whitespace-nowrap px-6 py-3.5 text-xs text-zinc-500">
                          {formatDate(log.created_at)}
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5 font-medium text-zinc-800">
                          {log.event_type}
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5 text-zinc-700">
                          {log.action}
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5 text-xs text-zinc-600">
                          {log.entity_type}{log.entity_id ? `#${log.entity_id}` : ""}
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5">
                          <AuditSeverityBadge severity={log.severity} />
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5">
                          <AuditStatusBadge status={log.status} />
                        </td>
                        <td className="whitespace-nowrap px-6 py-3.5 text-zinc-700">
                          {log.actor_email || log.actor_user_id || "System"}
                        </td>
                        <td className="max-w-xs truncate px-6 py-3.5 text-zinc-600">
                          {log.message}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Log Detail Modal */}
          {selectedLog && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
              <div data-testid="audit-log-detail" className="mx-4 max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-2xl bg-white shadow-2xl">
                <div className="sticky top-0 flex items-center justify-between border-b border-zinc-100 bg-white px-6 py-4">
                  <h2 className="text-lg font-extrabold text-zinc-900">
                    Detalhe do Log #{selectedLog.id}
                  </h2>
                  <button
                    onClick={() => setSelectedLog(null)}
                    className="rounded-lg p-2 text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-600"
                  >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <div className="space-y-4 p-6">
                  <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Event Type</p>
                      <p className="mt-1 text-sm font-medium text-zinc-900">{selectedLog.event_type}</p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Action</p>
                      <p className="mt-1 text-sm font-medium text-zinc-900">{selectedLog.action}</p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Entity</p>
                      <p className="mt-1 text-sm font-medium text-zinc-900">
                        {selectedLog.entity_type}{selectedLog.entity_id ? `#${selectedLog.entity_id}` : ""}
                      </p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Severidade</p>
                      <div className="mt-1"><AuditSeverityBadge severity={selectedLog.severity} /></div>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Status</p>
                      <div className="mt-1"><AuditStatusBadge status={selectedLog.status} /></div>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Source</p>
                      <p className="mt-1 text-sm font-medium text-zinc-900">{selectedLog.source || "N/A"}</p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Actor</p>
                      <p className="mt-1 text-sm font-medium text-zinc-900">{selectedLog.actor_email || selectedLog.actor_user_id || "System"}</p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Request ID</p>
                      <p className="mt-1 font-mono text-sm text-zinc-900">{selectedLog.request_id || "N/A"}</p>
                    </div>
                    <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-3">
                      <p className="text-[10px] font-semibold uppercase tracking-wide text-zinc-500">Data</p>
                      <p className="mt-1 text-sm text-zinc-900">{formatDate(selectedLog.created_at)}</p>
                    </div>
                  </div>

                  <div>
                    <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Message</p>
                    <p className="mt-1 text-sm text-zinc-700">{selectedLog.message}</p>
                  </div>

                  <AuditJsonViewer data={selectedLog.metadata_json} label="Metadata" data-testid="audit-json-metadata" />
                  <AuditJsonViewer data={selectedLog.before_json} label="Before" data-testid="audit-json-before" />
                  <AuditJsonViewer data={selectedLog.after_json} label="After" data-testid="audit-json-after" />
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </section>
  );
}
