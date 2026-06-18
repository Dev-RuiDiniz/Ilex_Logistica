"use client";

/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable react-hooks/exhaustive-deps */

import { useEffect, useState } from "react";

import {
  getDailyReports,
  getDailyReportById,
  getDailyReportByDate,
  generateDailyReport,
  exportDailyReports,
  parseSummary,
  parseKpis,
  parseExceptions,
  parseAlerts,
  parseCarrierEfficiency,
  parseImportFailures,
} from "@/lib/daily-report-api";
import type {
  DailyReport,
  DailyReportFilters,
  DailyReportStatus,
} from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";

export default function DailyReportPage() {
  const [reports, setReports] = useState<DailyReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<DailyReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState("");
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  // Export state
  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState("");

  // Filters
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [status, setStatus] = useState<DailyReportStatus | "">("");
  const [searchDate, setSearchDate] = useState("");

  const loadReports = async (signal?: AbortSignal) => {
    setLoading(true);
    setError("");
    try {
      const filters: DailyReportFilters = {};
      if (dateFrom) filters.date_from = dateFrom;
      if (dateTo) filters.date_to = dateTo;
      if (status) filters.status = status;

      const response = await getDailyReports(filters);
      if (!signal?.aborted) {
        setReports(response.reports);
      }
    } catch (err) {
      if (!signal?.aborted) {
        handleApiError(err instanceof Error ? err : new Error("Erro ao carregar relatórios"));
        setError(err instanceof Error ? err.message : "Erro ao carregar relatórios");
        console.error(err);
      }
    } finally {
      if (!signal?.aborted) {
        setLoading(false);
      }
    }
  };

  // Load reports on mount and when filters change
  useEffect(() => {
    const controller = new AbortController();
    loadReports(controller.signal);
    return () => controller.abort();
  }, [dateFrom, dateTo, status]);

  const handleGenerateReport = async () => {
    if (!searchDate) {
      setGenerateError("Informe uma data para gerar o relatório.");
      return;
    }

    setGenerating(true);
    setGenerateError("");
    try {
      const report = await generateDailyReport({
        report_date: searchDate,
      });
      setSelectedReport(report);
      await loadReports(); // Refresh list
    } catch (err) {
      setGenerateError("Falha ao gerar relatório diário.");
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const handleExportReport = async (format: "csv" | "json") => {
    if (reports.length === 0) {
      setExportError("Nenhum relatório para exportar.");
      return;
    }

    setExporting(true);
    setExportError("");
    try {
      const response = await exportDailyReports({
        format,
        date_from: dateFrom || undefined,
        date_to: dateTo || undefined,
        status: status || undefined,
      });

      // Create download link
      const blob = new Blob([response.content], { type: response.media_type });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = response.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setExportError("Falha ao exportar relatórios.");
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  const handleSearchByDate = async () => {
    if (!searchDate) {
      setError("Informe uma data para buscar.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const report = await getDailyReportByDate(searchDate);
      setSelectedReport(report);
    } catch (err) {
      setError("Relatório não encontrado para a data informada.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (reportId: number) => {
    setLoading(true);
    setError("");
    try {
      const report = await getDailyReportById(reportId);
      setSelectedReport(report);
    } catch (err) {
      setError("Falha ao carregar detalhes do relatório.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearFilters = () => {
    setDateFrom("");
    setDateTo("");
    setStatus("");
    setSearchDate("");
    setSelectedReport(null);
  };

  const summary = selectedReport ? parseSummary(selectedReport.summary_json) : null;
  const kpis = selectedReport ? parseKpis(selectedReport.kpis_json) : null;
  const exceptions = selectedReport ? parseExceptions(selectedReport.exceptions_json) : [];
  const alerts = selectedReport ? parseAlerts(selectedReport.alerts_json) : [];
  const carrierEfficiency = selectedReport ? parseCarrierEfficiency(selectedReport.carrier_efficiency_json) : [];
  const importFailures = selectedReport ? parseImportFailures(selectedReport.import_failures_json) : null;

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  return (
    <section className="page-stack">
      <header className="page-hero">
        <p className="page-kicker">Leitura executiva</p>
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <h2 className="page-title !text-[clamp(1.65rem,1.3rem+0.8vw,2.4rem)]">Relatório Diário</h2>
            <p className="page-subtitle">Consolide operação, exceções e desempenho em um único resumo acionável.</p>
          </div>
        </div>
        <button
          className="button-secondary self-start !bg-white"
          onClick={() => setSelectedReport(null)}
          disabled={!selectedReport}
        >
          Voltar para Lista
        </button>
      </header>

      {error && (
        <div className="rounded bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {!selectedReport ? (
        <>
          {/* Filters */}
          <div className="surface-panel p-4 md:p-6">
            <h3 className="mb-3 text-base font-semibold">Filtros</h3>
            <div className="grid gap-3 md:grid-cols-4">
              <div>
                <label className="mb-1 block text-sm font-medium">Data Inicial</label>
                <input
                  type="date"
                  className="field"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Data Final</label>
                <input
                  type="date"
                  className="field"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Status</label>
                <select
                  className="field-select"
                  value={status}
                  onChange={(e) => setStatus(e.target.value as DailyReportStatus | "")}
                >
                  <option value="">Todos</option>
                  <option value="generated">Gerado</option>
                  <option value="failed">Falhou</option>
                  <option value="stale">Antigo</option>
                  <option value="archived">Arquivado</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  className="button-secondary w-full"
                  onClick={handleClearFilters}
                >
                  Limpar Filtros
                </button>
              </div>
            </div>
          </div>

          {/* Generate/Search by Date */}
          <div className="surface-panel p-4 md:p-6">
            <h3 className="mb-3 text-base font-semibold">Gerar ou Buscar Relatório</h3>
            <div className="grid gap-3 md:grid-cols-3">
              <div>
                <label className="mb-1 block text-sm font-medium">Data</label>
                <input
                  type="date"
                  className="field"
                  value={searchDate}
                  onChange={(e) => setSearchDate(e.target.value)}
                />
              </div>
              <div className="flex items-end gap-2">
                <button
                  className="button-primary flex-1"
                  onClick={handleGenerateReport}
                  disabled={generating}
                >
                  {generating ? "Gerando..." : "Gerar Relatório"}
                </button>
                <button
                  className="button-secondary flex-1"
                  onClick={handleSearchByDate}
                  disabled={loading}
                >
                  Buscar por Data
                </button>
                <div className="flex gap-2">
                  <button
                    className="button-primary !bg-[linear-gradient(135deg,#2f7a63_0%,#459277_100%)]"
                    onClick={() => handleExportReport("csv")}
                    disabled={exporting || reports.length === 0}
                  >
                    {exporting ? "Exportando..." : "Exportar CSV"}
                  </button>
                  <button
                    className="button-primary !bg-[linear-gradient(135deg,#2e6a8e_0%,#3b83ae_100%)]"
                    onClick={() => handleExportReport("json")}
                    disabled={exporting || reports.length === 0}
                  >
                    {exporting ? "Exportando..." : "Exportar JSON"}
                  </button>
                </div>
              </div>
            </div>
            {generateError && (
              <p className="mt-2 text-sm text-red-600">{generateError}</p>
            )}
            {exportError && (
              <p className="mt-2 text-sm text-red-600">{exportError}</p>
            )}
          </div>

          {/* Report List */}
          <div className="surface-panel p-4 md:p-6">
            <h3 className="mb-3 text-base font-semibold">Histórico de Relatórios</h3>
            {loading ? (
              <p className="text-sm text-slate-600">Carregando...</p>
            ) : reports.length === 0 ? (
              <p className="text-sm text-slate-600">Nenhum relatório encontrado.</p>
            ) : (
              <div className="table-shell overflow-x-auto">
                <table className="data-table">
                  <thead>
                    <tr className="border-b">
                      <th className="px-3 py-2 text-left">Data</th>
                      <th className="px-3 py-2 text-left">Status</th>
                      <th className="px-3 py-2 text-left">Gerado em</th>
                      <th className="px-3 py-2 text-left">Total</th>
                      <th className="px-3 py-2 text-left">Atrasadas</th>
                      <th className="px-3 py-2 text-left">Críticas</th>
                      <th className="px-3 py-2 text-left">Alertas</th>
                      <th className="px-3 py-2 text-left">Exceções</th>
                      <th className="px-3 py-2 text-left">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reports.map((report) => {
                      const reportSummary = parseSummary(report.summary_json);
                      const reportKpis = parseKpis(report.kpis_json);
                      return (
                        <tr key={report.id} className="border-b">
                          <td className="px-3 py-2">
                            {new Date(report.report_date).toLocaleDateString("pt-BR")}
                          </td>
                          <td className="px-3 py-2">
                            <span
                              className={`rounded px-2 py-1 text-xs ${
                                report.status === "generated"
                                  ? "bg-green-100 text-green-800"
                                  : report.status === "failed"
                                  ? "bg-red-100 text-red-800"
                                  : "bg-gray-100 text-gray-800"
                              }`}
                            >
                              {report.status}
                            </span>
                          </td>
                          <td className="px-3 py-2">
                            {new Date(report.generated_at).toLocaleString("pt-BR")}
                          </td>
                          <td className="px-3 py-2">{reportSummary?.total_shipments || 0}</td>
                          <td className="px-3 py-2">{reportSummary?.late_count || 0}</td>
                          <td className="px-3 py-2">{reportSummary?.critical_count || 0}</td>
                          <td className="px-3 py-2">{reportKpis?.active_alerts_count || 0}</td>
                          <td className="px-3 py-2">{reportSummary?.exceptions_count || 0}</td>
                          <td className="px-3 py-2">
                            <button
                              className="button-secondary !px-3 !py-2 !text-xs"
                              onClick={() => handleViewDetails(report.id)}
                            >
                              Ver Detalhes
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      ) : (
        <>
          {/* Report Detail */}
          <div className="surface-panel p-4 md:p-6">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">
                  Relatório de {new Date(selectedReport.report_date).toLocaleDateString("pt-BR")}
                </h3>
                <p className="text-sm text-slate-600">
                  Gerado em {new Date(selectedReport.generated_at).toLocaleString("pt-BR")}
                </p>
              </div>
              <span
                className={`rounded px-3 py-1 text-sm ${
                  selectedReport.status === "generated"
                    ? "bg-green-100 text-green-800"
                    : selectedReport.status === "failed"
                    ? "bg-red-100 text-red-800"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {selectedReport.status}
              </span>
            </div>

            {selectedReport.period_start && selectedReport.period_end && (
              <p className="mb-4 text-sm text-slate-600">
                Período: {new Date(selectedReport.period_start).toLocaleDateString("pt-BR")} a{" "}
                {new Date(selectedReport.period_end).toLocaleDateString("pt-BR")}
              </p>
            )}

            {selectedReport.notes && (
              <div className="mb-4 rounded bg-yellow-50 p-3 text-sm text-yellow-800">
                <strong>Nota:</strong> {selectedReport.notes}
              </div>
            )}

            {/* KPIs */}
            {summary && kpis && (
              <div className="mb-6 grid gap-3 md:grid-cols-4">
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-600">Total de Envios</div>
                  <div className="text-2xl font-semibold">{summary.total_shipments}</div>
                </div>
                <div className="metric-card" data-tone="success">
                  <div className="text-sm text-slate-600">No Prazo</div>
                  <div className="text-2xl font-semibold text-green-600">{summary.on_time_count}</div>
                </div>
                <div className="metric-card" data-tone="warning">
                  <div className="text-sm text-slate-600">Atrasadas</div>
                  <div className="text-2xl font-semibold text-orange-600">{summary.late_count}</div>
                </div>
                <div className="metric-card" data-tone="danger">
                  <div className="text-sm text-slate-600">Críticas</div>
                  <div className="text-2xl font-semibold text-red-600">{summary.critical_count}</div>
                </div>
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-600">Alertas Ativos</div>
                  <div className="text-2xl font-semibold text-purple-600">{kpis.active_alerts_count ?? 0}</div>
                </div>
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-600">Taxa de Entrega</div>
                  <div className="text-2xl font-semibold">{((kpis.delivery_rate ?? 0) * 100).toFixed(1)}%</div>
                </div>
                <div className="metric-card" data-tone="warning">
                  <div className="text-sm text-slate-600">Exceções</div>
                  <div className="text-2xl font-semibold">{summary.exceptions_count}</div>
                </div>
                <div className="metric-card" data-tone="danger">
                  <div className="text-sm text-slate-600">Falhas de Importação</div>
                  <div className="text-2xl font-semibold">{importFailures?.rejected_count || 0}</div>
                </div>
              </div>
            )}

            {/* Exceptions */}
            {exceptions.length > 0 && (
              <div className="surface-muted mb-6 p-4">
                <h4 className="mb-3 text-base font-semibold">Exceções Priorizadas</h4>
                <div className="max-h-64 overflow-y-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="px-2 py-1 text-left">Tracking</th>
                        <th className="px-2 py-1 text-left">Transportadora</th>
                        <th className="px-2 py-1 text-left">Cliente</th>
                        <th className="px-2 py-1 text-left">UF</th>
                        <th className="px-2 py-1 text-left">Atraso (dias)</th>
                        <th className="px-2 py-1 text-left">Tipo</th>
                      </tr>
                    </thead>
                    <tbody>
                      {exceptions.slice(0, 10).map((exc) => (
                        <tr key={exc.shipment_id} className="border-b">
                          <td className="px-2 py-1">{exc.tracking_code}</td>
                          <td className="px-2 py-1">{exc.carrier_name || "-"}</td>
                          <td className="px-2 py-1">{exc.customer_name || "-"}</td>
                          <td className="px-2 py-1">{exc.destination_uf || "-"}</td>
                          <td className="px-2 py-1">{exc.delay_days}</td>
                          <td className="px-2 py-1">{exc.exception_type || "-"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Alerts */}
            {alerts.length > 0 && (
              <div className="surface-muted mb-6 p-4">
                <h4 className="mb-3 text-base font-semibold">Alertas Críticos/Ativos</h4>
                <div className="max-h-64 overflow-y-auto space-y-2">
                  {alerts.slice(0, 10).map((alert) => (
                    <div
                      key={alert.id}
                      className={`rounded border p-2 text-sm ${
                        alert.severity === "critical"
                          ? "border-red-200 bg-red-50"
                          : alert.severity === "high"
                          ? "border-orange-200 bg-orange-50"
                          : "border-gray-200 bg-gray-50"
                      }`}
                    >
                      <div className="font-semibold">{alert.title}</div>
                      <div className="text-slate-600">{alert.message}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Carrier Efficiency */}
            {carrierEfficiency.length > 0 && (
              <div className="surface-muted mb-6 p-4">
                <h4 className="mb-3 text-base font-semibold">Top Transportadoras por Eficiência</h4>
                <div className="max-h-64 overflow-y-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        <th className="px-2 py-1 text-left">Transportadora</th>
                        <th className="px-2 py-1 text-left">Total</th>
                        <th className="px-2 py-1 text-left">No Prazo</th>
                        <th className="px-2 py-1 text-left">Atrasadas</th>
                        <th className="px-2 py-1 text-left">Eficiência</th>
                      </tr>
                    </thead>
                    <tbody>
                      {carrierEfficiency.slice(0, 10).map((carrier) => (
                        <tr key={carrier.carrier_id} className="border-b">
                          <td className="px-2 py-1">{carrier.carrier_name}</td>
                          <td className="px-2 py-1">{carrier.total_shipments}</td>
                          <td className="px-2 py-1">{carrier.on_time_count}</td>
                          <td className="px-2 py-1">{carrier.late_count}</td>
                          <td className="px-2 py-1">{(carrier.efficiency_rate * 100).toFixed(1)}%</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </section>
  );
}
