"use client";

import { useEffect, useState } from "react";
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

import { DateRangePicker } from "@/app/(private)/shipments/analytics/carrier-efficiency/DateRangePicker";
import { AccessDenied } from "@/components/AccessDenied";
import { getDashboardSummary, getDashboardTrend } from "@/lib/dashboard-api";
import type {
  DashboardFilters,
  DashboardSummaryResponse,
  DashboardTrendFilters,
  DashboardTrendResponse,
} from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

const kpiCards = [
  { key: "total_shipments", label: "Total", tone: "accent", note: "Base monitorada", render: (data: DashboardSummaryResponse) => data.total_shipments },
  { key: "on_time_count", label: "No Prazo", tone: "success", note: "Fluxo saudável", render: (data: DashboardSummaryResponse) => data.on_time_count },
  { key: "late_count", label: "Atrasadas", tone: "warning", note: "Exigem correção", render: (data: DashboardSummaryResponse) => data.late_count },
  { key: "critical_count", label: "Críticas", tone: "danger", note: "Ação imediata", render: (data: DashboardSummaryResponse) => data.critical_count },
  { key: "warning_count", label: "Atenção", tone: "warning", note: "Risco operacional", render: (data: DashboardSummaryResponse) => data.warning_count },
  { key: "unknown_sla_count", label: "Sem SLA", tone: "accent", note: "Revisar parametrização", render: (data: DashboardSummaryResponse) => data.unknown_sla_count },
  { key: "exceptions_count", label: "Exceções", tone: "danger", note: "Fila priorizada", render: (data: DashboardSummaryResponse) => data.exceptions_count },
  { key: "carriers_count", label: "Transportadoras", tone: "accent", note: "Rede ativa", render: (data: DashboardSummaryResponse) => data.carriers_count },
  {
    key: "active_alerts_count",
    label: "Alertas Ativos",
    tone: "warning",
    note: "Monitoramento vivo",
    render: (data: DashboardSummaryResponse) => data.active_alerts_count === 0 ? "Nenhum alerta ativo" : data.active_alerts_count,
  },
  { key: "import_failure_count", label: "Falhas Importação", tone: "danger", note: "Pipeline sob atenção", render: (data: DashboardSummaryResponse) => data.import_failure_count },
];

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
      <div className="loading-state surface-panel-strong">
        <p className="page-kicker !text-slate-600">Dashboard</p>
        <div className="section-title">Carregando...</div>
        <p className="section-subtitle">Montando a visão operacional do dia.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <div className="section-title">Erro: {error}</div>
        <p className="section-subtitle !text-[#8d4234]">Não foi possível consolidar os indicadores agora.</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="empty-state">
        <div className="section-title">Sem dados</div>
        <p className="section-subtitle">Ainda não há indicadores consolidados para o período selecionado.</p>
      </div>
    );
  }

  return (
    <div className="page-grid">
      <section className="page-hero">
        <p className="page-kicker">Painel diário</p>
        <h1 className="page-title">Painel de controle</h1>
        <p className="page-subtitle">
          Monitore envios, detecte gargalos e acompanhe o que merece resposta
          imediata com uma leitura executiva da operação.
        </p>
      </section>

      <section className="surface-panel p-5 md:p-6" data-testid="dashboard-filters">
        <div className="mb-5">
          <h2 className="section-title">Filtros</h2>
          <p className="section-subtitle">Refine a leitura principal por janela, cliente, UF e status de SLA.</p>
        </div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div>
            <label className="field-label">Mês</label>
            <input
              aria-label="Mês"
              className="field"
              id="filter-month"
              max="12"
              min="1"
              type="number"
              value={filters.month ?? ""}
              onChange={(e) => handleFilterChange("month", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="field-label">Ano</label>
            <input
              aria-label="Ano"
              className="field"
              id="filter-year"
              max="2100"
              min="2020"
              type="number"
              value={filters.year ?? ""}
              onChange={(e) => handleFilterChange("year", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <div>
            <label className="field-label">Cliente</label>
            <input
              aria-label="Cliente"
              className="field"
              id="filter-customer"
              type="text"
              value={filters.customer_name ?? ""}
              onChange={(e) => handleFilterChange("customer_name", e.target.value)}
            />
          </div>
          <div>
            <label className="field-label">UF</label>
            <input
              aria-label="UF"
              className="field"
              id="filter-uf"
              maxLength={2}
              type="text"
              value={filters.destination_uf ?? ""}
              onChange={(e) => handleFilterChange("destination_uf", e.target.value)}
            />
          </div>
          <div>
            <label className="field-label">Status SLA</label>
            <select
              aria-label="Status SLA"
              className="field-select"
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
            <label className="field-label">Atrasada</label>
            <select
              aria-label="Atrasada"
              className="field-select"
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
        <div className="section-actions mt-5">
          <button data-testid="clear-main-filters" className="button-secondary" onClick={clearFilters}>
            Limpar Filtros
          </button>
        </div>
      </section>

      <section className="surface-panel p-5 md:p-6" data-testid="dashboard-trend-filters">
        <div className="mb-5">
          <h2 className="section-title">Período da Tendência</h2>
          <p className="section-subtitle">Compare evolução de volume, SLA e exceções por recorte temporal.</p>
        </div>
        <DateRangePicker
          label="Período de Entrega Estimada"
          value={{ from: trendFilters.estimated_delivery_from, to: trendFilters.estimated_delivery_to }}
          onChange={(v) => setTrendFilters((prev) => ({ ...prev, ...v }))}
          placeholder={{ from: "Data inicial", to: "Data final" }}
        />
        <div className="mt-4 flex flex-wrap items-end gap-3">
          <div>
            <label className="field-label">Dias</label>
            <input
              type="number"
              min="1"
              max="90"
              className="field w-28"
              value={trendFilters.days ?? ""}
              onChange={(e) => handleTrendFilterChange("days", e.target.value ? parseInt(e.target.value) : undefined)}
            />
          </div>
          <button className="button-secondary" onClick={clearTrendFilters}>
            Limpar Filtros
          </button>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-5" data-testid="dashboard-kpi-cards">
        {kpiCards.map((card) => (
          <article key={card.key} className="metric-card" data-tone={card.tone}>
            <div className="space-y-2">
              <div className="metric-card-label">{card.label}</div>
              <strong>{card.render(data)}</strong>
            </div>
            <div className="space-y-2">
              <div className="metric-card-note">{card.note}</div>
              {card.key === "active_alerts_count" && data.active_alerts_count > 0 && (
                <a href="/alerts" className="inline-flex text-sm font-semibold text-[#15314b] hover:text-[#2e6a8e]">
                  Ver alertas →
                </a>
              )}
            </div>
          </article>
        ))}
      </section>

      <section className="grid gap-5 xl:grid-cols-[1.5fr_1fr]">
        <div className="surface-panel p-5 md:p-6">
          <div className="mb-4">
            <h2 className="section-title">Tendência dos KPIs</h2>
            <p className="section-subtitle">Acompanhe ritmo da operação e sinais de desvio nos últimos dias.</p>
          </div>
          {trendLoading ? (
            <div className="loading-state">Carregando tendências...</div>
          ) : trendData && trendData.trend_data && trendData.trend_data.length > 0 ? (
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
              <div className="surface-muted p-4">
                <h3 className="mb-3 text-base font-bold tracking-[-0.03em] text-slate-900">Total de entregas por dia</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={trendData.trend_data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(16,32,51,0.12)" />
                      <XAxis dataKey="date" tickFormatter={(v) => v.slice(5)} />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="total_shipments" stroke="#2e6a8e" strokeWidth={2.5} dot={{ r: 4 }} name="Total" />
                      <Line type="monotone" dataKey="on_time_count" stroke="#2f7a63" strokeWidth={2.5} dot={{ r: 4 }} name="No Prazo" />
                      <Line type="monotone" dataKey="late_count" stroke="#b6523d" strokeWidth={2.5} dot={{ r: 4 }} name="Atrasadas" />
                      <Line type="monotone" dataKey="critical_count" stroke="#c67d2f" strokeWidth={2.5} dot={{ r: 4 }} name="Críticas" />
                      <Line type="monotone" dataKey="warning_count" stroke="#c07a22" strokeWidth={2.5} dot={{ r: 4 }} name="Atenção" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="surface-muted p-4">
                <h3 className="mb-3 text-base font-bold tracking-[-0.03em] text-slate-900">Exceções e sem SLA</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={trendData.trend_data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(16,32,51,0.12)" />
                      <XAxis dataKey="date" tickFormatter={(v) => v.slice(5)} />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="exceptions_count" stroke="#15314b" strokeWidth={2.5} dot={{ r: 4 }} name="Exceções" />
                      <Line type="monotone" dataKey="unknown_sla_count" stroke="#64748b" strokeWidth={2.5} dot={{ r: 4 }} name="Sem SLA" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">Sem dados de tendência para o período selecionado</div>
          )}
        </div>

        <div className="page-stack">
          <div className="surface-panel p-5" data-testid="top-carriers">
            <h2 className="section-title">Top Transportadoras por Eficiência</h2>
            <p className="section-subtitle mt-1">Quem sustenta melhor o nível de serviço no período.</p>
            {data.top_carriers_by_efficiency.length === 0 ? (
              <div className="empty-state mt-4 !min-h-[11rem]">Nenhuma transportadora encontrada</div>
            ) : (
              <div className="table-shell mt-4">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th className="text-left">Transportadora</th>
                      <th className="text-right">Total</th>
                      <th className="text-right">No Prazo</th>
                      <th className="text-right">Atrasadas</th>
                      <th className="text-right">% No Prazo</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.top_carriers_by_efficiency.map((carrier) => (
                      <tr key={carrier.carrier_id}>
                        <td>{carrier.carrier_name || "-"}</td>
                        <td className="text-right">{carrier.total_shipments}</td>
                        <td className="text-right">{carrier.on_time_count}</td>
                        <td className="text-right">{carrier.late_count}</td>
                        <td className="text-right">{carrier.on_time_percentage.toFixed(1)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="surface-panel p-5" data-testid="top-exceptions">
            <h2 className="section-title">Top Exceções Priorizadas</h2>
            <p className="section-subtitle mt-1">Fila crítica para resposta rápida do time.</p>
            {data.top_exceptions.length === 0 ? (
              <div className="empty-state mt-4 !min-h-[11rem]">Nenhuma exceção encontrada</div>
            ) : (
              <div className="table-shell mt-4">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th className="text-left">Prioridade</th>
                      <th className="text-left">Tipo</th>
                      <th className="text-left">Motivo</th>
                      <th className="text-left">Rastreio</th>
                      <th className="text-left">NF</th>
                      <th className="text-left">Transportadora</th>
                      <th className="text-left">Cliente</th>
                      <th className="text-left">UF</th>
                      <th className="text-left">Status SLA</th>
                      <th className="text-left">Criticidade</th>
                      <th className="text-right">Atraso (dias)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.top_exceptions.map((exc) => (
                      <tr key={exc.shipment_id}>
                        <td>{exc.priority}</td>
                        <td>{exc.exception_type || "-"}</td>
                        <td>{exc.exception_reason || "-"}</td>
                        <td>{exc.tracking_code}</td>
                        <td>{exc.invoice_number || "-"}</td>
                        <td>{exc.carrier_name || "-"}</td>
                        <td>{exc.customer_name || "-"}</td>
                        <td>{exc.destination_uf || "-"}</td>
                        <td>{exc.sla_status}</td>
                        <td>{exc.criticality}</td>
                        <td className="text-right">{exc.delay_days}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </section>

      <p className="text-sm text-slate-700">
        Gerado em: {data.generated_at ? new Date(data.generated_at).toLocaleString("pt-BR") : "-"}
      </p>
    </div>
  );
}
