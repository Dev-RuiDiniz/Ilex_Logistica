"use client";

import { useEffect, useState } from "react";
<<<<<<< HEAD
import Link from "next/link";
import { getDashboardSummary } from "@/lib/dashboard-api";
import type { DashboardExceptionItem, DashboardFilters, DashboardSummaryResponse } from "@/lib/types";

// Helpers de tradução e cores para a seção Top Exceções Priorizadas
const slaStatusLabels: Record<string, string> = {
  on_time: "No Prazo",
  late: "Atrasada",
  critical: "Crítica",
  warning: "Atenção",
  unknown: "Sem SLA",
  unknown_sla: "Sem SLA",
};

const slaStatusColors: Record<string, string> = {
  on_time: "bg-emerald-100 text-emerald-700 border-emerald-200",
  late: "bg-orange-100 text-orange-700 border-orange-200",
  critical: "bg-red-100 text-red-700 border-red-200",
  warning: "bg-yellow-100 text-yellow-700 border-yellow-200",
  unknown: "bg-gray-100 text-gray-700 border-gray-200",
  unknown_sla: "bg-gray-100 text-gray-700 border-gray-200",
};

const criticalityLabels: Record<string, string> = {
  normal: "Normal",
  baixa: "Baixa",
  media: "Média",
  alta: "Alta",
};

const criticalityColors: Record<string, string> = {
  normal: "bg-blue-100 text-blue-700 border-blue-200",
  baixa: "bg-green-100 text-green-700 border-green-200",
  media: "bg-yellow-100 text-yellow-700 border-yellow-200",
  alta: "bg-red-100 text-red-700 border-red-200",
};

const statusLabels: Record<string, string> = {
  in_transit: "Em Trânsito",
  delivered: "Entregue",
  pending: "Pendente",
  failed: "Falha",
  cancelled: "Cancelado",
};

const exceptionTypeLabels: Record<string, string> = {
  critical: "Crítico",
  late: "Atraso",
  warning: "Atenção",
  unknown_sla: "Sem SLA",
};

const priorityLabels: Record<number, string> = {
  1: "Urgente",
  2: "Alta",
  3: "Média",
  4: "Baixa",
};

const priorityColors: Record<number, string> = {
  1: "bg-red-600 text-white border-red-600",
  2: "bg-orange-500 text-white border-orange-500",
  3: "bg-yellow-500 text-white border-yellow-500",
  4: "bg-blue-500 text-white border-blue-500",
};

function getPriorityLabel(priority: number) {
  return priorityLabels[priority] || `P${priority}`;
}

function getPriorityColor(priority: number) {
  return priorityColors[priority] || "bg-gray-500 text-white border-gray-500";
}

function formatWhatsAppNumber(raw?: string | null) {
  if (!raw) return null;
  const digits = raw.replace(/\D/g, "");
  if (!digits) return null;
  return digits.startsWith("55") || digits.startsWith("+") ? digits : `55${digits}`;
}

function ContactActions({ exc }: { exc: DashboardExceptionItem }) {
  const whatsapp = formatWhatsAppNumber(exc.carrier_whatsapp);
  const email = exc.carrier_email;

  if (!whatsapp && !email) {
    return <span className="text-xs text-gray-400">Sem contato cadastrado</span>;
  }

  const message = encodeURIComponent(
    `Olá, ${exc.carrier_name || "Transportadora"}!\n\nGostaria de tratar sobre o envio *${exc.tracking_code}* do cliente *${exc.customer_name || "-"}* (NF: ${exc.invoice_number || "-"}).\n\nPodemos verificar o status?`
  );

  return (
    <div className="flex flex-wrap gap-2">
      {whatsapp && (
        <a
          href={`https://wa.me/${whatsapp}?text=${message}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 rounded-lg bg-green-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-green-700 transition-colors"
        >
          <svg className="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.521.15-.174.2-.298.3-.497.099-.198.05-.371-.025-.521-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.521.074-.797.372-.275.297-1.052 1.029-1.052 2.509 0 1.48 1.078 2.91 1.227 3.112.149.198 2.12 3.236 5.137 4.536.719.31 1.28.495 1.718.634.722.23 1.377.197 1.894.12.577-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.839c3.545 0 6.421 2.876 6.421 6.421 0 3.545-2.876 6.421-6.421 6.421-3.545 0-6.421-2.876-6.421-6.421 0-3.545 2.876-6.421 6.421-6.421m0 14.186c4.286 0 7.765-3.479 7.765-7.765S16.786 2.964 12.5 2.964 4.735 6.443 4.735 10.729s3.479 7.765 7.765 7.765" />
          </svg>
          WhatsApp
        </a>
      )}
      {email && (
        <a
          href={`mailto:${email}?subject=${encodeURIComponent(`Solicitação sobre envio ${exc.tracking_code}`)}&body=${message}`}
          className="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-blue-700 transition-colors"
        >
          <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          E-mail
        </a>
      )}
    </div>
  );
}
=======
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
>>>>>>> fix/infra-setup-local

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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<DashboardFilters>({});

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const token = localStorage.getItem("accessToken") || "";
        const result = await getDashboardSummary(token, filters);
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
<<<<<<< HEAD
  }, [filters]);
=======
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
>>>>>>> fix/infra-setup-local

  const handleFilterChange = (key: keyof DashboardFilters, value: string | number | boolean | undefined) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const clearFilters = () => {
    setFilters({});
  };

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
<<<<<<< HEAD
        <button
          className="mt-4 px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          onClick={clearFilters}
          data-testid="clear-main-filters"
        >
          Limpar Filtros
        </button>
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
=======
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
>>>>>>> fix/infra-setup-local
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

<<<<<<< HEAD
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
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Top Exceções Priorizadas</h2>
          <Link
            href="/shipments/analytics/exceptions"
            className="text-sm font-medium text-red-600 hover:text-red-700 transition-colors"
          >
            Ver painel completo →
          </Link>
        </div>
        {data.top_exceptions.length === 0 ? (
          <div className="text-gray-500">Nenhuma exceção encontrada</div>
        ) : (
          <div className="grid gap-4">
            {data.top_exceptions.map((exc) => (
              <div
                key={exc.shipment_id}
                className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
              >
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  {/* Coluna principal */}
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2 mb-2">
                      <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold ${getPriorityColor(exc.priority)}`}>
                        {getPriorityLabel(exc.priority)} · Prioridade {exc.priority}
                      </span>
                      <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${slaStatusColors[exc.sla_status] || slaStatusColors.unknown}`}>
                        {slaStatusLabels[exc.sla_status] || exc.sla_status}
                      </span>
                      <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${criticalityColors[exc.criticality] || criticalityColors.normal}`}>
                        {criticalityLabels[exc.criticality] || exc.criticality}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-sm">
                      <div>
                        <span className="block text-xs text-gray-500">Rastreio</span>
                        <span className="font-semibold text-gray-900">{exc.tracking_code}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">NF</span>
                        <span className="font-medium text-gray-900">{exc.invoice_number || "-"}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Transportadora</span>
                        <span className="font-medium text-gray-900">{exc.carrier_name || "-"}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Cliente / UF</span>
                        <span className="font-medium text-gray-900">{exc.customer_name || "-"} / {exc.destination_uf || "-"}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Tipo de Exceção</span>
                        <span className="font-medium text-gray-900">{exceptionTypeLabels[exc.exception_type || ""] || exc.exception_type || "-"}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Motivo</span>
                        <span className="font-medium text-gray-900">{exc.exception_reason || "-"}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Status do Envio</span>
                        <span className="font-medium text-gray-900">{statusLabels[exc.status] || exc.status}</span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">Atraso</span>
                        <span className={`font-semibold ${exc.delay_days > 0 ? "text-red-600" : "text-gray-900"}`}>
                          {exc.delay_days > 0 ? `${exc.delay_days} dias` : "Sem atraso"}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Coluna de ações */}
                  <div className="flex flex-col gap-2 lg:items-end lg:min-w-[12rem]">
                    <span className="text-xs font-medium text-gray-500 mb-1">Contato com a transportadora</span>
                    <ContactActions exc={exc} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Data de Geração */}
      <div className="text-sm text-gray-500">
=======
      <p className="text-sm text-slate-700">
>>>>>>> fix/infra-setup-local
        Gerado em: {data.generated_at ? new Date(data.generated_at).toLocaleString("pt-BR") : "-"}
      </p>
    </div>
  );
}
