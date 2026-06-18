"use client";

import { useState, useEffect, useCallback } from "react";
import { getAuditLogs, getAuditSummary, type AuditLog, type AuditLogFilters, type AuditLogSummaryResponse, type AuditSeverity, type AuditStatus } from "@/lib/audit-api";
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
    }
  }, [token, handleApiError]);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    const init = async () => {
      await fetchLogs();
      await fetchSummary();
    };
    init();
  }, [token]);

  const handleFilterChange = (key: keyof AuditLogFilters, value: string | number | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
      page: 1,
    }));
  };

  const clearFilters = () => {
    setFilters({ page: 1, page_size: 50 });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString("pt-BR");
  };

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (loading && logs.length === 0) {
    return (
      <div data-testid="audit-page" className="p-6">
        <h1 className="text-2xl font-bold mb-6">Auditoria Operacional</h1>
        <div className="text-slate-700">Carregando...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div data-testid="audit-page" className="p-6">
        <h1 className="text-2xl font-bold mb-6">Auditoria Operacional</h1>
        <div data-testid="audit-error-state" className="text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div data-testid="audit-page" className="p-6">
      <h1 className="text-2xl font-bold mb-6">Auditoria Operacional</h1>

      {/* Summary */}
      {summary && (
        <div data-testid="audit-summary" className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-slate-700">Total de Logs</div>
            <div className="text-2xl font-bold">{summary.total_logs}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-slate-700">Sucesso</div>
            <div className="text-2xl font-bold text-green-600">{summary.success_count}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-slate-700">Falhas</div>
            <div className="text-2xl font-bold text-red-600">{summary.failed_count}</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-sm text-slate-700">Críticos</div>
            <div className="text-2xl font-bold text-red-800">{summary.critical_count}</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div data-testid="audit-filters" className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-800">Event Type</label>
            <input
              type="text"
              value={filters.event_type || ""}
              onChange={(e) => handleFilterChange("event_type", e.target.value || undefined)}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Ex: daily_report_generated"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-800">Entity Type</label>
            <input
              type="text"
              value={filters.entity_type || ""}
              onChange={(e) => handleFilterChange("entity_type", e.target.value || undefined)}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="Ex: shipment"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-800">Severity</label>
            <select
              value={filters.severity || ""}
              onChange={(e) => handleFilterChange("severity", e.target.value as AuditSeverity | undefined)}
              className="w-full px-3 py-2 border rounded-md"
            >
              <option value="">Todos</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-800">Status</label>
            <select
              value={filters.status || ""}
              onChange={(e) => handleFilterChange("status", e.target.value as AuditStatus | undefined)}
              className="w-full px-3 py-2 border rounded-md"
            >
              <option value="">Todos</option>
              <option value="success">Success</option>
              <option value="failed">Failed</option>
              <option value="skipped">Skipped</option>
            </select>
          </div>
        </div>
        <div className="mt-4 flex gap-2">
          <button
            onClick={() => fetchLogs()}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Aplicar Filtros
          </button>
          <button
            onClick={clearFilters}
            className="rounded-md bg-gray-200 px-4 py-2 text-slate-800 hover:bg-gray-300"
          >
            Limpar Filtros
          </button>
        </div>
      </div>

      {/* Logs Table */}
      {logs.length === 0 ? (
        <div data-testid="audit-empty-state" className="py-8 text-center text-slate-700">
          Nenhum log encontrado
        </div>
      ) : (
        <div data-testid="audit-log-table" className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Data</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Event Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Action</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Entity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Severity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Actor</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-700 uppercase tracking-wider">Message</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {logs.map((log) => (
                <tr
                  key={log.id}
                  data-testid="audit-log-row"
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => setSelectedLog(log)}
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                    {formatDate(log.created_at)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {log.event_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {log.action}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {log.entity_type} {log.entity_id && `#${log.entity_id}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <AuditSeverityBadge severity={log.severity} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <AuditStatusBadge status={log.status} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {log.actor_email || log.actor_user_id || "System"}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                    {log.message}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Log Detail Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div data-testid="audit-log-detail" className="bg-white rounded-lg shadow-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto m-4">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Detalhe do Log #{selectedLog.id}</h2>
                <button
                  onClick={() => setSelectedLog(null)}
                  className="text-slate-700 hover:text-slate-900"
                >
                  Fechar
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-sm font-medium text-slate-800">Event Type:</span>
                    <div className="text-sm">{selectedLog.event_type}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Action:</span>
                    <div className="text-sm">{selectedLog.action}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Entity Type:</span>
                    <div className="text-sm">{selectedLog.entity_type}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Entity ID:</span>
                    <div className="text-sm">{selectedLog.entity_id || "N/A"}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Severity:</span>
                    <div className="text-sm"><AuditSeverityBadge severity={selectedLog.severity} /></div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Status:</span>
                    <div className="text-sm"><AuditStatusBadge status={selectedLog.status} /></div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Actor:</span>
                    <div className="text-sm">{selectedLog.actor_email || selectedLog.actor_user_id || "System"}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Source:</span>
                    <div className="text-sm">{selectedLog.source || "N/A"}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Request ID:</span>
                    <div className="text-sm">{selectedLog.request_id || "N/A"}</div>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-800">Created At:</span>
                    <div className="text-sm">{formatDate(selectedLog.created_at)}</div>
                  </div>
                </div>

                <div>
                  <span className="text-sm font-medium text-slate-800">Message:</span>
                  <div className="text-sm mt-1">{selectedLog.message}</div>
                </div>

                <AuditJsonViewer data={selectedLog.metadata_json} label="Metadata" data-testid="audit-json-metadata" />
                <AuditJsonViewer data={selectedLog.before_json} label="Before" data-testid="audit-json-before" />
                <AuditJsonViewer data={selectedLog.after_json} label="After" data-testid="audit-json-after" />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
