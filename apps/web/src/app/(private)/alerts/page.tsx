'use client';

import { useState, useEffect } from 'react';
import { getAlerts, getAlertsSummary, generateAlerts, markAlertAsRead, resolveAlert, type AlertsFilters, type AlertItem, type AlertsSummary } from '@/lib/alerts-api';
import { useApiErrorHandler } from '@/lib/useApiErrorHandler';
import { AccessDenied } from '@/components/AccessDenied';

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
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar alertas"));
      setError(err instanceof Error ? err.message : "Erro ao carregar alertas");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAlerts = async () => {
    try {
      await generateAlerts();
      await fetchAlerts();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao gerar alertas"));
      setError(err instanceof Error ? err.message : "Erro ao gerar alertas");
      console.error(err);
    }
  };

  const handleMarkAsRead = async (alertId: number) => {
    try {
      await markAlertAsRead(alertId);
      await fetchAlerts();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao marcar alerta como lido"));
      setError(err instanceof Error ? err.message : "Erro ao marcar alerta como lido");
      console.error(err);
    }
  };

  const handleResolve = async (alertId: number) => {
    try {
      await resolveAlert(alertId);
      await fetchAlerts();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao resolver alerta"));
      setError(err instanceof Error ? err.message : "Erro ao resolver alerta");
      console.error(err);
    }
  };

  const handleFilterChange = (key: keyof AlertsFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleClearFilters = () => {
    setFilters({});
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchAlerts();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (loading) {
    return <div className="p-6">Carregando...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">Erro: {error}</div>;
  }

  if (!summary) {
    return <div className="p-6">Carregando resumo...</div>;
  }

  return (
    <div className="page-stack">
      <section className="page-hero">
        <p className="page-kicker">Monitoramento ativo</p>
        <h1 className="page-title !text-[clamp(1.65rem,1.3rem+0.8vw,2.4rem)]">Alertas</h1>
        <p className="page-subtitle">Priorize ocorrências, acompanhe leitura e resolva desvios com contexto operacional.</p>
      </section>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-6">
        <div className="metric-card" data-tone="accent">
          <div className="text-sm text-slate-700">Total</div>
          <div className="text-2xl font-bold">{summary.total_alerts}</div>
        </div>
        <div className="metric-card" data-tone="accent">
          <div className="text-sm text-slate-700">Ativos</div>
          <div className="text-2xl font-bold text-blue-600">{summary.active_count}</div>
        </div>
        <div className="metric-card" data-tone="warning">
          <div className="text-sm text-slate-700">Não Lidos</div>
          <div className="text-2xl font-bold text-yellow-600">{summary.total_alerts - summary.read_count}</div>
        </div>
        <div className="metric-card" data-tone="success">
          <div className="text-sm text-slate-700">Resolvidos</div>
          <div className="text-2xl font-bold text-green-600">{summary.resolved_count}</div>
        </div>
        <div className="metric-card" data-tone="danger">
          <div className="text-sm text-slate-700">Críticos</div>
          <div className="text-2xl font-bold text-red-600">{summary.critical_count}</div>
        </div>
        <div className="metric-card" data-tone="warning">
          <div className="text-sm text-slate-700">Warnings</div>
          <div className="text-2xl font-bold text-orange-600">{summary.warning_count}</div>
        </div>
      </div>

      {/* Filters */}
      <div className="surface-panel p-4 md:p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div>
            <label htmlFor="status-filter" className="block text-sm font-medium mb-1">Status</label>
            <select
              id="status-filter"
              className="field-select"
              value={filters.status || ''}
              onChange={(e) => handleFilterChange('status', e.target.value || undefined)}
            >
              <option value="">Todos</option>
              <option value="active">Ativo</option>
              <option value="read">Lido</option>
              <option value="resolved">Resolvido</option>
            </select>
          </div>
          <div>
            <label htmlFor="severity-filter" className="block text-sm font-medium mb-1">Severidade</label>
            <select
              id="severity-filter"
              className="field-select"
              value={filters.severity || ''}
              onChange={(e) => handleFilterChange('severity', e.target.value || undefined)}
            >
              <option value="">Todas</option>
              <option value="critical">Crítico</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
            </select>
          </div>
          <div>
            <label htmlFor="type-filter" className="block text-sm font-medium mb-1">Tipo</label>
            <select
              id="type-filter"
              className="field-select"
              value={filters.alert_type || ''}
              onChange={(e) => handleFilterChange('alert_type', e.target.value || undefined)}
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
            <label htmlFor="read-filter" className="block text-sm font-medium mb-1">Lido</label>
            <select
              id="read-filter"
              className="field-select"
              value={filters.is_read === undefined ? '' : String(filters.is_read)}
              onChange={(e) => handleFilterChange('is_read', e.target.value === '' ? undefined : e.target.value === 'true')}
            >
              <option value="">Todos</option>
              <option value="true">Sim</option>
              <option value="false">Não</option>
            </select>
          </div>
          <div>
            <label htmlFor="resolved-filter" className="block text-sm font-medium mb-1">Resolvido</label>
            <select
              id="resolved-filter"
              className="field-select"
              value={filters.is_resolved === undefined ? '' : String(filters.is_resolved)}
              onChange={(e) => handleFilterChange('is_resolved', e.target.value === '' ? undefined : e.target.value === 'true')}
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
              className="button-secondary w-full"
            >
              Limpar Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div>
        <button
          data-testid="generate-alerts-button"
          onClick={handleGenerateAlerts}
          className="button-primary"
        >
          Gerar Alertas
        </button>
      </div>

      {/* Alerts List */}
      {alerts.length === 0 ? (
        <div className="empty-state surface-panel-strong text-slate-700">
          Nenhum alerta encontrado
        </div>
      ) : (
        <div className="table-shell overflow-hidden">
          <table className="data-table w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Severidade</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Tipo</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Status</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Título</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Mensagem</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Origem</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Gerado em</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-slate-800">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {alerts.map((alert) => (
                <tr key={alert.id} className={alert.is_resolved ? 'bg-gray-50' : ''}>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        alert.severity === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : alert.severity === 'warning'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {alert.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm">{alert.alert_type}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        alert.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : alert.status === 'resolved'
                          ? 'bg-gray-100 text-gray-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {alert.status}
                      {!alert.is_read && <span className="ml-1 text-yellow-600">• Não lido</span>}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm font-medium">{alert.title}</td>
                  <td className="px-4 py-3 text-sm text-slate-700">{alert.message}</td>
                  <td className="px-4 py-3 text-sm">
                    {alert.source_type} {alert.source_id}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-700">
                    {new Date(alert.generated_at).toLocaleString('pt-BR')}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      {!alert.is_read && (
                        <button
                          data-testid={`mark-read-button-${alert.id}`}
                          onClick={() => handleMarkAsRead(alert.id)}
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          Marcar como lido
                        </button>
                      )}
                      {!alert.is_resolved && (
                        <button
                          data-testid={`resolve-button-${alert.id}`}
                          onClick={() => handleResolve(alert.id)}
                          className="text-green-600 hover:text-green-800 text-sm"
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
      )}
    </div>
  );
}
