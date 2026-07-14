"use client";

import { useCallback, useEffect, useState } from "react";
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
import type { DailyReport, DailyReportFilters, DailyReportStatus } from "@/lib/types";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";

export default function DailyReportPage() {
  const [reports, setReports] = useState<DailyReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<DailyReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [generating, setGenerating] = useState(false);
  const [generateError, setGenerateError] = useState("");
  const { session } = useAuth();
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  // Export state
  const [exporting, setExporting] = useState(false);
  const [exportError, setExportError] = useState("");

  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [status, setStatus] = useState<DailyReportStatus | "">("");
  const [searchDate, setSearchDate] = useState("");

  const loadReports = useCallback(async (signal?: AbortSignal) => {
    if (!session) return;
    setLoading(true);
    setError("");
    try {
      const filters: DailyReportFilters = {};
      if (dateFrom) filters.date_from = dateFrom;
      if (dateTo) filters.date_to = dateTo;
      if (status) filters.status = status;
      const response = await getDailyReports(session.accessToken, filters);
      if (!signal?.aborted) setReports(response.reports);
    } catch (err) {
      if (!signal?.aborted) {
        const error = err instanceof Error ? err : new Error(String(err));
        handleApiError(error);
        setError(error.message);
      }
    } finally {
      if (!signal?.aborted) setLoading(false);
    }
  }, [dateFrom, dateTo, handleApiError, session, status]);

  useEffect(() => {
    if (!session) return;
    const controller = new AbortController();
    queueMicrotask(() => void loadReports(controller.signal));
    return () => controller.abort();
  }, [loadReports, session]);

  const handleGenerateReport = async () => {
    if (!session) return;
    if (!searchDate) {
      setGenerateError("Informe uma data para gerar o relatório.");
      return;
    }
    setGenerating(true);
    setGenerateError("");
    try {
      const report = await generateDailyReport(session.accessToken, { report_date: searchDate });
      setSelectedReport(report);
      await loadReports();
    } catch {
      setGenerateError("Falha ao gerar relatório diário.");
    } finally {
      setGenerating(false);
    }
  };

  const handleExportReport = async (format: "csv" | "json") => {
    if (!session) return;
    if (reports.length === 0) {
      setExportError("Nenhum relatório para exportar.");
      return;
    }

    setExporting(true);
    setExportError("");
    try {
      const response = await exportDailyReports(session.accessToken, {
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
    if (!session) return;
    if (!searchDate) {
      setError("Informe uma data para buscar.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const report = await getDailyReportByDate(session.accessToken, searchDate);
      setSelectedReport(report);
    } catch {
      setError("Relatório não encontrado para a data informada.");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (reportId: number) => {
    if (!session) return;
    setLoading(true);
    setError("");
    try {
      const report = await getDailyReportById(session.accessToken, reportId);
      setSelectedReport(report);
    } catch {
      setError("Falha ao carregar detalhes do relatório.");
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

  const inputClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800 disabled:opacity-50";
  const btnSecondary = "rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50";

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  const getStatusBadge = (reportStatus: string) => {
    const map: Record<string, string> = {
      generated: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20",
      failed: "bg-red-50 text-red-700 ring-1 ring-red-600/20",
      stale: "bg-amber-50 text-amber-700 ring-1 ring-amber-600/20",
      archived: "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20",
    };
    return map[reportStatus] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20";
  };

  return (
<<<<<<< HEAD
    <section className="space-y-6">
      {/* Header */}
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Relatório Diário</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Visão consolidada da operação diária</p>
        </div>
        {selectedReport && (
          <button
            onClick={() => setSelectedReport(null)}
            className={btnSecondary}
          >
            ← Voltar para Lista
          </button>
        )}
=======
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
>>>>>>> fix/infra-setup-local
      </header>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {!selectedReport ? (
        <>
          {/* Filters */}
<<<<<<< HEAD
          <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
            <p className="mb-4 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Filtros</p>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Data Inicial</label>
                <input type="date" className={inputClass} value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Data Final</label>
                <input type="date" className={inputClass} value={dateTo} onChange={(e) => setDateTo(e.target.value)} />
              </div>
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Status</label>
                <select className={inputClass} value={status} onChange={(e) => setStatus(e.target.value as DailyReportStatus | "")}>
=======
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
>>>>>>> fix/infra-setup-local
                  <option value="">Todos</option>
                  <option value="generated">Gerado</option>
                  <option value="failed">Falhou</option>
                  <option value="stale">Antigo</option>
                  <option value="archived">Arquivado</option>
                </select>
              </div>
              <div className="flex items-end">
<<<<<<< HEAD
                <button onClick={handleClearFilters} className={btnSecondary + " w-full"}>
=======
                <button
                  className="button-secondary w-full"
                  onClick={handleClearFilters}
                >
>>>>>>> fix/infra-setup-local
                  Limpar Filtros
                </button>
              </div>
            </div>
          </div>

<<<<<<< HEAD
          {/* Generate/Search */}
          <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
            <p className="mb-4 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Gerar ou Buscar Relatório</p>
            <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
              <div>
                <label className="block text-[11px] font-semibold text-zinc-500">Data</label>
                <input type="date" className={inputClass} value={searchDate} onChange={(e) => setSearchDate(e.target.value)} />
=======
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
>>>>>>> fix/infra-setup-local
              </div>
              <div className="flex items-end gap-2 md:col-span-2">
                <button
<<<<<<< HEAD
=======
                  className="button-primary flex-1"
>>>>>>> fix/infra-setup-local
                  onClick={handleGenerateReport}
                  disabled={generating}
                  className={btnPrimary + " flex-1"}
                >
                  {generating ? "Gerando..." : "Gerar Relatório"}
                </button>
                <button
<<<<<<< HEAD
=======
                  className="button-secondary flex-1"
>>>>>>> fix/infra-setup-local
                  onClick={handleSearchByDate}
                  disabled={loading}
                  className={btnSecondary + " flex-1"}
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
              <div className="mt-3 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
                {generateError}
              </div>
            )}
            {exportError && (
              <p className="mt-2 text-sm text-red-600">{exportError}</p>
            )}
          </div>

          {/* Report List */}
<<<<<<< HEAD
          <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
            <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
              <p className="text-sm font-semibold text-zinc-700">
                {reports.length} relatório{reports.length !== 1 ? "s" : ""} encontrado{reports.length !== 1 ? "s" : ""}
              </p>
            </div>
            {loading ? (
              <div className="flex items-center justify-center p-12">
                <div className="flex items-center gap-3">
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
                  <p className="text-sm font-medium text-zinc-500">Carregando relatórios...</p>
                </div>
              </div>
            ) : reports.length === 0 ? (
              <div className="p-12 text-center">
                <svg className="mx-auto h-12 w-12 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>
                <p className="mt-3 text-sm font-medium text-zinc-500">Nenhum relatório encontrado</p>
              </div>
=======
          <div className="surface-panel p-4 md:p-6">
            <h3 className="mb-3 text-base font-semibold">Histórico de Relatórios</h3>
            {loading ? (
              <p className="text-sm text-slate-700">Carregando...</p>
            ) : reports.length === 0 ? (
              <p className="text-sm text-slate-700">Nenhum relatório encontrado.</p>
>>>>>>> fix/infra-setup-local
            ) : (
              <div className="table-shell overflow-x-auto">
                <table className="data-table">
                  <thead>
                    <tr className="border-b border-zinc-100 bg-zinc-50/80">
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Data</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Gerado em</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atrasadas</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Críticas</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Alertas</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Exceções</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reports.map((report) => {
                      const reportSummary = parseSummary(report.summary_json);
                      const reportKpis = parseKpis(report.kpis_json);
                      return (
                        <tr key={report.id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                          <td className="px-6 py-3 font-medium text-zinc-900">
                            {new Date(report.report_date).toLocaleDateString("pt-BR")}
                          </td>
                          <td className="px-6 py-3">
                            <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold capitalize ${getStatusBadge(report.status)}`}>
                              {report.status}
                            </span>
                          </td>
                          <td className="px-6 py-3 text-xs text-zinc-500">
                            {new Date(report.generated_at).toLocaleString("pt-BR")}
                          </td>
                          <td className="px-6 py-3 text-right font-mono font-medium text-zinc-700">{reportSummary?.total_shipments || 0}</td>
                          <td className="px-6 py-3 text-right font-mono font-medium text-[#e8a84a]">{reportSummary?.late_count || 0}</td>
                          <td className="px-6 py-3 text-right font-mono font-medium text-[#ef5350]">{reportSummary?.critical_count || 0}</td>
                          <td className="px-6 py-3 text-right font-mono font-medium text-purple-600">{reportKpis?.active_alerts_count || 0}</td>
                          <td className="px-6 py-3 text-right font-mono font-medium text-zinc-600">{reportSummary?.exceptions_count || 0}</td>
                          <td className="px-6 py-3 text-right">
                            <button
<<<<<<< HEAD
=======
                              className="button-secondary !px-3 !py-2 !text-xs"
>>>>>>> fix/infra-setup-local
                              onClick={() => handleViewDetails(report.id)}
                              className="rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
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
<<<<<<< HEAD
          <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
            <div className="flex items-start justify-between">
=======
          <div className="surface-panel p-4 md:p-6">
            <div className="mb-4 flex items-center justify-between">
>>>>>>> fix/infra-setup-local
              <div>
                <h2 className="text-xl font-extrabold text-zinc-900">
                  Relatório de {new Date(selectedReport.report_date).toLocaleDateString("pt-BR")}
<<<<<<< HEAD
                </h2>
                <p className="mt-1 text-sm text-zinc-500">
=======
                </h3>
                <p className="text-sm text-slate-700">
>>>>>>> fix/infra-setup-local
                  Gerado em {new Date(selectedReport.generated_at).toLocaleString("pt-BR")}
                </p>
                {selectedReport.period_start && selectedReport.period_end && (
                  <p className="mt-1 text-xs text-zinc-400">
                    Período: {new Date(selectedReport.period_start).toLocaleDateString("pt-BR")} a {new Date(selectedReport.period_end).toLocaleDateString("pt-BR")}
                  </p>
                )}
              </div>
              <span className={`inline-flex rounded-full px-3 py-1 text-xs font-bold capitalize ${getStatusBadge(selectedReport.status)}`}>
                {selectedReport.status}
              </span>
            </div>

<<<<<<< HEAD
=======
            {selectedReport.period_start && selectedReport.period_end && (
              <p className="mb-4 text-sm text-slate-700">
                Período: {new Date(selectedReport.period_start).toLocaleDateString("pt-BR")} a{" "}
                {new Date(selectedReport.period_end).toLocaleDateString("pt-BR")}
              </p>
            )}

>>>>>>> fix/infra-setup-local
            {selectedReport.notes && (
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-700">
                <strong>Nota:</strong> {selectedReport.notes}
              </div>
            )}
<<<<<<< HEAD
=======

            {/* KPIs */}
            {summary && kpis && (
              <div className="mb-6 grid gap-3 md:grid-cols-4">
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-700">Total de Envios</div>
                  <div className="text-2xl font-semibold">{summary.total_shipments}</div>
                </div>
                <div className="metric-card" data-tone="success">
                  <div className="text-sm text-slate-700">No Prazo</div>
                  <div className="text-2xl font-semibold text-green-600">{summary.on_time_count}</div>
                </div>
                <div className="metric-card" data-tone="warning">
                  <div className="text-sm text-slate-700">Atrasadas</div>
                  <div className="text-2xl font-semibold text-orange-600">{summary.late_count}</div>
                </div>
                <div className="metric-card" data-tone="danger">
                  <div className="text-sm text-slate-700">Críticas</div>
                  <div className="text-2xl font-semibold text-red-600">{summary.critical_count}</div>
                </div>
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-700">Alertas Ativos</div>
                  <div className="text-2xl font-semibold text-purple-600">{kpis.active_alerts_count ?? 0}</div>
                </div>
                <div className="metric-card" data-tone="accent">
                  <div className="text-sm text-slate-700">Taxa de Entrega</div>
                  <div className="text-2xl font-semibold">{((kpis.delivery_rate ?? 0) * 100).toFixed(1)}%</div>
                </div>
                <div className="metric-card" data-tone="warning">
                  <div className="text-sm text-slate-700">Exceções</div>
                  <div className="text-2xl font-semibold">{summary.exceptions_count}</div>
                </div>
                <div className="metric-card" data-tone="danger">
                  <div className="text-sm text-slate-700">Falhas de Importação</div>
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
                      <div className="text-slate-700">{alert.message}</div>
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
>>>>>>> fix/infra-setup-local
          </div>

          {/* KPIs */}
          {summary && kpis && (
            <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
              <div className="rounded-2xl border border-zinc-200 bg-white p-5 text-center shadow-sm">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total de Envios</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-zinc-900">{summary.total_shipments}</p>
              </div>
              <div className="rounded-2xl border border-emerald-100 bg-emerald-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70">No Prazo</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-emerald-600">{summary.on_time_count}</p>
              </div>
              <div className="rounded-2xl border border-amber-100 bg-amber-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Atrasadas</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-amber-600">{summary.late_count}</p>
              </div>
              <div className="rounded-2xl border border-red-100 bg-red-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Críticas</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-red-600">{summary.critical_count}</p>
              </div>
              <div className="rounded-2xl border border-purple-100 bg-purple-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-purple-600/70">Alertas Ativos</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-purple-600">{kpis.active_alerts_count ?? 0}</p>
              </div>
              <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-blue-600/70">Taxa de Entrega</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-blue-600">{((kpis.delivery_rate ?? 0) * 100).toFixed(1)}%</p>
              </div>
              <div className="rounded-2xl border border-zinc-200 bg-white p-5 text-center shadow-sm">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Exceções</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-zinc-900">{summary.exceptions_count}</p>
              </div>
              <div className="rounded-2xl border border-orange-100 bg-orange-50 p-5 text-center">
                <p className="text-[11px] font-semibold uppercase tracking-wide text-orange-600/70">Falhas Importação</p>
                <p className="mt-2 text-3xl font-extrabold tabular-nums text-orange-600">{importFailures?.rejected_count || 0}</p>
              </div>
            </div>
          )}

          {/* Exceptions */}
          {exceptions.length > 0 && (
            <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="border-b border-zinc-100 px-6 py-4">
                <h3 className="text-sm font-bold text-zinc-900">Exceções Priorizadas</h3>
              </div>
              <div className="max-h-64 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 border-b border-zinc-100 bg-zinc-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Tracking</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Transportadora</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Cliente</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">UF</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atraso</th>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Tipo</th>
                    </tr>
                  </thead>
                  <tbody>
                    {exceptions.slice(0, 10).map((exc) => (
                      <tr key={exc.shipment_id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                        <td className="px-6 py-2.5 font-mono text-xs text-zinc-600">{exc.tracking_code}</td>
                        <td className="px-6 py-2.5 font-medium text-zinc-700">{exc.carrier_name || "-"}</td>
                        <td className="px-6 py-2.5 text-zinc-600">{exc.customer_name || "-"}</td>
                        <td className="px-6 py-2.5 font-mono text-xs font-semibold text-zinc-600">{exc.destination_uf || "-"}</td>
                        <td className="px-6 py-2.5 text-right font-mono text-xs font-bold text-red-600">{exc.delay_days}d</td>
                        <td className="px-6 py-2.5 text-zinc-600">{exc.exception_type || "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Alerts */}
          {alerts.length > 0 && (
            <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="border-b border-zinc-100 px-6 py-4">
                <h3 className="text-sm font-bold text-zinc-900">Alertas Críticos/Ativos</h3>
              </div>
              <div className="max-h-64 divide-y divide-zinc-50 overflow-auto">
                {alerts.slice(0, 10).map((alert) => (
                  <div
                    key={alert.id}
                    className={`px-6 py-3 ${
                      alert.severity === "critical" ? "bg-red-50/50" : alert.severity === "high" ? "bg-orange-50/50" : ""
                    }`}
                  >
                    <p className="text-sm font-semibold text-zinc-900">{alert.title}</p>
                    <p className="mt-0.5 text-xs text-zinc-600">{alert.message}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Carrier Efficiency */}
          {carrierEfficiency.length > 0 && (
            <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="border-b border-zinc-100 px-6 py-4">
                <h3 className="text-sm font-bold text-zinc-900">Top Transportadoras por Eficiência</h3>
              </div>
              <div className="max-h-64 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 border-b border-zinc-100 bg-zinc-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Transportadora</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">No Prazo</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atrasadas</th>
                      <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Eficiência</th>
                    </tr>
                  </thead>
                  <tbody>
                    {carrierEfficiency.slice(0, 10).map((carrier) => (
                      <tr key={carrier.carrier_id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                        <td className="px-6 py-2.5 font-semibold text-zinc-900">{carrier.carrier_name}</td>
                        <td className="px-6 py-2.5 text-right font-mono text-xs text-zinc-600">{carrier.total_shipments}</td>
                        <td className="px-6 py-2.5 text-right font-mono text-xs text-[#66bb6a]">{carrier.on_time_count}</td>
                        <td className="px-6 py-2.5 text-right font-mono text-xs text-[#ef5350]">{carrier.late_count}</td>
                        <td className="px-6 py-2.5 text-right">
                          <span className={`font-mono text-xs font-bold tabular-nums ${
                            carrier.efficiency_rate >= 0.85 ? "text-[#66bb6a]" : carrier.efficiency_rate >= 0.75 ? "text-[#e8a84a]" : "text-[#ef5350]"
                          }`}>
                            {(carrier.efficiency_rate * 100).toFixed(1)}%
                          </span>
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
