"use client";

import { useEffect, useState } from "react";

import { getDashboardSummary } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import type { DashboardSummaryResponse } from "@/lib/types";

export default function DashboardPage() {
  const { session } = useAuth();
  const { handleApiError } = useApiErrorHandler();
  const [data, setData] = useState<DashboardSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!session) return;
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const summary = await getDashboardSummary(session.accessToken);
        setData(summary);
      } catch (err) {
        handleApiError(err instanceof Error ? err : new Error("Erro ao carregar dashboard"));
        setError(err instanceof Error ? err.message : "Erro ao carregar dashboard");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [session, handleApiError]);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center rounded-2xl border border-zinc-200 bg-white">
        <div className="flex items-center gap-3 text-zinc-500">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-300 border-t-red-600" />
          <span className="text-sm font-medium">Carregando dashboard...</span>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-96 flex-col items-center justify-center rounded-2xl border border-red-200 bg-red-50 p-6">
        <p className="text-sm font-semibold text-red-600">Falha ao carregar dashboard</p>
        <p className="mt-1 text-xs text-red-500">{error || "Dados indisponíveis"}</p>
      </div>
    );
  }

  const onTimePct = data.total_shipments > 0
    ? ((data.on_time_count / data.total_shipments) * 100).toFixed(1)
    : "0.0";
  const latePct = data.total_shipments > 0
    ? ((data.late_count / data.total_shipments) * 100).toFixed(1)
    : "0.0";
  const criticalPct = data.total_shipments > 0
    ? ((data.critical_count / data.total_shipments) * 100).toFixed(1)
    : "0.0";
  const warningPct = data.total_shipments > 0
    ? ((data.warning_count / data.total_shipments) * 100).toFixed(1)
    : "0.0";

  const carriers = data.top_carriers_by_efficiency ?? [];
  const maxCarrier = carriers.length > 0
    ? Math.max(...carriers.map((c) => c.total_shipments))
    : 1;

  const translateExceptionType = (type: string | null | undefined, slaStatus: string) => {
    if (type === "late" || slaStatus === "late") return "Atraso";
    if (type === "critical" || slaStatus === "critical") return "Crítico";
    if (type === "warning" || slaStatus === "warning") return "Atenção";
    if (type === "unknown") return "SLA indefinido";
    return type ? type.charAt(0).toUpperCase() + type.slice(1) : "Exceção";
  };

  const getSeverity = (slaStatus: string, priority: number) => {
    if (slaStatus === "critical" || priority >= 80) return "critical";
    if (slaStatus === "late" || slaStatus === "warning" || priority >= 50) return "warning";
    return "info";
  };

  const recentActivity = (data.top_exceptions ?? []).slice(0, 7).map((exc) => {
    const severity = getSeverity(exc.sla_status, exc.priority);
    const typeLabel = translateExceptionType(exc.exception_type, exc.sla_status);
    const carrier = exc.carrier_name ?? "Transportadora não informada";
    const destination = exc.destination_uf ? ` → ${exc.destination_uf}` : "";
    const delayText = exc.delay_days > 0 ? `de ${exc.delay_days}d` : "";
    const event = delayText ? `${typeLabel} ${delayText}`.trim() : typeLabel;
    return {
      id: exc.shipment_id,
      event,
      tracking: `${exc.tracking_code ?? "—"} • ${carrier}${destination}`,
      time: exc.last_update_at
        ? new Date(exc.last_update_at).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })
        : "",
      severity,
    };
  });

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <KpiCard
          label="Total Envios"
          value={data.total_shipments.toLocaleString("pt-BR")}
          sublabel={`${data.carriers_count} transportadoras`}
          iconColor="blue"
          icon={<IconShipment />}
        />
        <KpiCard
          label="No Prazo"
          value={`${onTimePct}%`}
          sublabel={`${data.on_time_count.toLocaleString("pt-BR")} entregas`}
          iconColor="emerald"
          icon={<IconCheck />}
        />
        <KpiCard
          label="Atrasadas"
          value={data.late_count.toLocaleString("pt-BR")}
          sublabel={`${data.critical_count} críticas`}
          iconColor="amber"
          icon={<IconClock />}
        />
        <KpiCard
          label="Exceções"
          value={data.exceptions_count.toLocaleString("pt-BR")}
          sublabel={`${data.active_alerts_count} alertas ativos`}
          iconColor="red"
          icon={<IconAlert />}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Bar Chart - Carrier Distribution */}
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-zinc-900">Envios por Transportadora</h3>
              <p className="text-[11px] text-zinc-500">Top performance por eficiência</p>
            </div>
          </div>
          {carriers.length === 0 ? (
            <p className="py-8 text-center text-sm text-zinc-400">Nenhuma transportadora com envios no período.</p>
          ) : (
            <div className="space-y-3">
              {carriers.map((carrier, i) => {
                const colors = [
                  "bg-blue-500",
                  "bg-emerald-500",
                  "bg-amber-500",
                  "bg-purple-500",
                  "bg-red-400",
                  "bg-cyan-500",
                  "bg-orange-400",
                  "bg-zinc-400",
                ];
                const pct = carrier.total_shipments > 0
                  ? ((carrier.total_shipments / data.total_shipments) * 100).toFixed(1)
                  : "0.0";
                return (
                  <div key={carrier.carrier_id} className="flex items-center gap-3">
                    <span className="w-32 flex-shrink-0 truncate text-xs font-medium text-zinc-700">
                      {carrier.carrier_name ?? "—"}
                    </span>
                    <div className="flex-1">
                      <div className="h-6 overflow-hidden rounded-md bg-zinc-100">
                        <div
                          className={`h-full rounded-md ${colors[i % colors.length]} transition-all`}
                          style={{ width: `${(carrier.total_shipments / maxCarrier) * 100}%` }}
                        />
                      </div>
                    </div>
                    <span className="w-12 text-right text-xs font-bold tabular-nums text-zinc-700">
                      {carrier.total_shipments}
                    </span>
                    <span className="w-12 text-right text-[10px] font-medium text-zinc-400">
                      {pct}%
                    </span>
                    <span className="w-14 text-right text-[10px] font-medium text-emerald-600">
                      {carrier.on_time_percentage.toFixed(0)}%
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Donut Chart - Status Distribution */}
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="mb-5">
            <h3 className="text-sm font-bold text-zinc-900">Status das Entregas</h3>
            <p className="text-[11px] text-zinc-500">Visão geral</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="relative h-36 w-36">
              <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#e4e4e7" strokeWidth="14" />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#22c55e" strokeWidth="14"
                  strokeDasharray={`${Number(onTimePct) * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset="0"
                  strokeLinecap="round"
                />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#f59e0b" strokeWidth="14"
                  strokeDasharray={`${Number(latePct) * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-Number(onTimePct) * 2.51327}`}
                  strokeLinecap="round"
                />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#ef4444" strokeWidth="14"
                  strokeDasharray={`${Number(criticalPct) * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-(Number(onTimePct) + Number(latePct)) * 2.51327}`}
                  strokeLinecap="round"
                />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#eab308" strokeWidth="14"
                  strokeDasharray={`${Number(warningPct) * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-(Number(onTimePct) + Number(latePct) + Number(criticalPct)) * 2.51327}`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <p className="text-2xl font-extrabold text-zinc-900">{data.total_shipments.toLocaleString("pt-BR")}</p>
                <p className="text-[10px] font-medium text-zinc-500">TOTAL</p>
              </div>
            </div>
            <div className="mt-4 grid w-full grid-cols-2 gap-2">
              <LegendItem color="bg-emerald-500" label="No Prazo" value={`${onTimePct}%`} />
              <LegendItem color="bg-amber-500" label="Atrasadas" value={`${latePct}%`} />
              <LegendItem color="bg-red-500" label="Críticas" value={`${criticalPct}%`} />
              <LegendItem color="bg-yellow-500" label="Atenção" value={`${warningPct}%`} />
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <h3 className="text-sm font-bold text-zinc-900">Exceções em Destaque</h3>
          <span className="text-[11px] font-medium text-zinc-500">Top prioridade</span>
        </div>
        <div className="divide-y divide-zinc-50">
          {recentActivity.length === 0 ? (
            <p className="px-6 py-8 text-center text-sm text-zinc-400">Nenhuma exceção no momento.</p>
          ) : (
            recentActivity.map((item) => (
              <div key={item.id} className="flex items-center gap-4 px-6 py-3.5 transition-colors hover:bg-zinc-50/50">
                <div className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full ${
                  item.severity === "critical" ? "bg-red-100 text-red-600" :
                  item.severity === "warning" ? "bg-amber-100 text-amber-600" :
                  "bg-blue-100 text-blue-600"
                }`}>
                  {item.severity === "critical" ? <IconAlert /> :
                   item.severity === "warning" ? <IconClock /> : <IconInfo />}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold text-zinc-900">{item.event}</p>
                  <p className="truncate text-xs text-zinc-500">{item.tracking}</p>
                </div>
                <span className="flex-shrink-0 text-[11px] font-medium text-zinc-400" suppressHydrationWarning>{item.time}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function KpiCard({
  label,
  value,
  sublabel,
  iconColor,
  icon,
}: {
  label: string;
  value: string;
  sublabel: string;
  iconColor: "blue" | "emerald" | "amber" | "red";
  icon: React.ReactNode;
}) {
  const colorMap = {
    blue: "bg-blue-50 text-blue-600",
    emerald: "bg-emerald-50 text-emerald-600",
    amber: "bg-amber-50 text-amber-600",
    red: "bg-red-50 text-red-600",
  };
  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:shadow-md">
      <div className="flex items-center justify-between">
        <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</p>
        <div className={`flex h-8 w-8 items-center justify-center rounded-lg ${colorMap[iconColor]}`}>
          {icon}
        </div>
      </div>
      <p className="mt-3 text-3xl font-extrabold tabular-nums text-zinc-900">{value}</p>
      <p className="mt-1 text-xs font-medium text-zinc-500">{sublabel}</p>
    </div>
  );
}

function LegendItem({ color, label, value }: { color: string; label: string; value: string }) {
  return (
    <div className="flex items-center gap-2 rounded-lg bg-zinc-50 px-3 py-2">
      <div className={`h-2.5 w-2.5 rounded-full ${color}`} />
      <span className="flex-1 text-[11px] font-medium text-zinc-700">{label}</span>
      <span className="text-[11px] font-bold text-zinc-900">{value}</span>
    </div>
  );
}

function IconShipment() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  );
}

function IconCheck() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconClock() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  );
}

function IconAlert() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
    </svg>
  );
}

function IconInfo() {
  return (
    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
    </svg>
  );
}
