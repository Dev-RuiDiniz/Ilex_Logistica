"use client";

import { useState } from "react";

const MOCK = {
  total_shipments: 2847,
  on_time_count: 2134,
  late_count: 412,
  critical_count: 87,
  warning_count: 214,
  exceptions_count: 23,
  carriers_count: 12,
  active_alerts_count: 3,
  weekly_evolution: [
    { week: "S1", on_time: 82, late: 12, critical: 6 },
    { week: "S2", on_time: 85, late: 9, critical: 6 },
    { week: "S3", on_time: 78, late: 14, critical: 8 },
    { week: "S4", on_time: 89, late: 7, critical: 4 },
    { week: "S5", on_time: 86, late: 8, critical: 6 },
    { week: "S6", on_time: 91, late: 5, critical: 4 },
    { week: "S7", on_time: 88, late: 7, critical: 5 },
    { week: "S8", on_time: 92, late: 4, critical: 4 },
  ],
  carrier_distribution: [
    { name: "Transportes Rápidos", count: 534, pct: 18.8 },
    { name: "Braspress", count: 421, pct: 14.8 },
    { name: "Jadlog", count: 387, pct: 13.6 },
    { name: "Loggi", count: 298, pct: 10.5 },
    { name: "Sequoia", count: 256, pct: 9.0 },
    { name: "Azul Cargo", count: 198, pct: 7.0 },
    { name: "JSL", count: 145, pct: 5.1 },
    { name: "Outros", count: 309, pct: 10.9 },
  ],
  recent_activity: [
    { id: 1, event: "Novo envio criado", tracking: "BRP001234567", time: "2 min atrás", severity: "info" },
    { id: 2, event: "Alerta SLA crítico", tracking: "LOG009876543", time: "15 min atrás", severity: "critical" },
    { id: 3, event: "Importação concluída", tracking: "350 registros", time: "1h atrás", severity: "success" },
    { id: 4, event: "Atraso detectado", tracking: "JDL005432167", time: "2h atrás", severity: "warning" },
    { id: 5, event: "Entrega realizada", tracking: "RAP003216548", time: "3h atrás", severity: "success" },
    { id: 6, event: "Falha de integração", tracking: "API Braspress", time: "4h atrás", severity: "critical" },
    { id: 7, event: "Relatório gerado", tracking: "Diário", time: "5h atrás", severity: "info" },
  ],
};

export default function DashboardPage() {
  const data = MOCK;
  const onTimePct = ((data.on_time_count / data.total_shipments) * 100).toFixed(1);
  const maxCarrier = Math.max(...data.carrier_distribution.map((c) => c.count));

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 lg:grid-cols-4">
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total Envios</p>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
              </svg>
            </div>
          </div>
          <p className="mt-3 text-3xl font-extrabold tabular-nums text-zinc-900">{data.total_shipments.toLocaleString("pt-BR")}</p>
          <p className="mt-1 text-xs font-medium text-emerald-600">+12% vs semana anterior</p>
        </div>
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">No Prazo</p>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 text-emerald-600">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <p className="mt-3 text-3xl font-extrabold tabular-nums text-emerald-600">{onTimePct}%</p>
          <p className="mt-1 text-xs font-medium text-zinc-500">{data.on_time_count.toLocaleString("pt-BR")} entregas</p>
        </div>
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atrasadas</p>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-50 text-amber-600">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <p className="mt-3 text-3xl font-extrabold tabular-nums text-amber-600">{data.late_count}</p>
          <p className="mt-1 text-xs font-medium text-zinc-500">{data.critical_count} críticas</p>
        </div>
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm transition-all hover:shadow-md">
          <div className="flex items-center justify-between">
            <p className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Exceções</p>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-red-50 text-red-600">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
            </div>
          </div>
          <p className="mt-3 text-3xl font-extrabold tabular-nums text-red-600">{data.exceptions_count}</p>
          <p className="mt-1 text-xs font-medium text-zinc-500">{data.active_alerts_count} alertas ativos</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Bar Chart - Carrier Distribution */}
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm lg:col-span-2">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-zinc-900">Envios por Transportadora</h3>
              <p className="text-[11px] text-zinc-500">Distribuição do período</p>
            </div>
          </div>
          <div className="space-y-3">
            {data.carrier_distribution.map((carrier, i) => {
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
              return (
                <div key={i} className="flex items-center gap-3">
                  <span className="w-28 flex-shrink-0 text-xs font-medium text-zinc-700 truncate">{carrier.name}</span>
                  <div className="flex-1">
                    <div className="h-6 overflow-hidden rounded-md bg-zinc-100">
                      <div
                        className={`h-full rounded-md ${colors[i % colors.length]} transition-all`}
                        style={{ width: `${(carrier.count / maxCarrier) * 100}%` }}
                      />
                    </div>
                  </div>
                  <span className="w-12 text-right text-xs font-bold tabular-nums text-zinc-700">{carrier.count}</span>
                  <span className="w-12 text-right text-[10px] font-medium text-zinc-400">{carrier.pct}%</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Pie Chart - Status Distribution */}
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="mb-5">
            <h3 className="text-sm font-bold text-zinc-900">Status das Entregas</h3>
            <p className="text-[11px] text-zinc-500">Visão geral</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="relative h-36 w-36">
              <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
                {/* On Time - 75% */}
                <circle cx="50" cy="50" r="40" fill="none" stroke="#e4e4e7" strokeWidth="14" />
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#22c55e" strokeWidth="14"
                  strokeDasharray={`${75 * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset="0"
                  strokeLinecap="round"
                />
                {/* Late - 14.5% */}
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#f59e0b" strokeWidth="14"
                  strokeDasharray={`${14.5 * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-75 * 2.51327}`}
                  strokeLinecap="round"
                />
                {/* Critical - 3% */}
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#ef4444" strokeWidth="14"
                  strokeDasharray={`${3 * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-(75 + 14.5) * 2.51327}`}
                  strokeLinecap="round"
                />
                {/* Warning - 7.5% */}
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="#eab308" strokeWidth="14"
                  strokeDasharray={`${7.5 * 2.51327} ${100 * 2.51327}`}
                  strokeDashoffset={`${-(75 + 14.5 + 3) * 2.51327}`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <p className="text-2xl font-extrabold text-zinc-900">{data.total_shipments.toLocaleString("pt-BR")}</p>
                <p className="text-[10px] font-medium text-zinc-500">TOTAL</p>
              </div>
            </div>
            <div className="mt-4 grid w-full grid-cols-2 gap-2">
              <div className="flex items-center gap-2 rounded-lg bg-emerald-50 px-3 py-2">
                <div className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                <span className="flex-1 text-[11px] font-medium text-zinc-700">No Prazo</span>
                <span className="text-[11px] font-bold text-emerald-700">75%</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-amber-50 px-3 py-2">
                <div className="h-2.5 w-2.5 rounded-full bg-amber-500" />
                <span className="flex-1 text-[11px] font-medium text-zinc-700">Atrasadas</span>
                <span className="text-[11px] font-bold text-amber-700">14.5%</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-red-50 px-3 py-2">
                <div className="h-2.5 w-2.5 rounded-full bg-red-500" />
                <span className="flex-1 text-[11px] font-medium text-zinc-700">Críticas</span>
                <span className="text-[11px] font-bold text-red-700">3%</span>
              </div>
              <div className="flex items-center gap-2 rounded-lg bg-yellow-50 px-3 py-2">
                <div className="h-2.5 w-2.5 rounded-full bg-yellow-500" />
                <span className="flex-1 text-[11px] font-medium text-zinc-700">Atenção</span>
                <span className="text-[11px] font-bold text-yellow-700">7.5%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <h3 className="text-sm font-bold text-zinc-900">Atividade Recente</h3>
          <span className="text-[11px] font-medium text-zinc-500">Últimas 24h</span>
        </div>
        <div className="divide-y divide-zinc-50">
          {data.recent_activity.map((item) => (
            <div key={item.id} className="flex items-center gap-4 px-6 py-3.5 transition-colors hover:bg-zinc-50/50">
              <div className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full ${
                item.severity === "critical" ? "bg-red-100 text-red-600" :
                item.severity === "warning" ? "bg-amber-100 text-amber-600" :
                item.severity === "success" ? "bg-emerald-100 text-emerald-600" :
                "bg-blue-100 text-blue-600"
              }`}>
                {item.severity === "critical" ? (
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                  </svg>
                ) : item.severity === "warning" ? (
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ) : item.severity === "success" ? (
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ) : (
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                  </svg>
                )}
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-zinc-900">{item.event}</p>
                <p className="truncate text-xs text-zinc-500">{item.tracking}</p>
              </div>
              <span className="flex-shrink-0 text-[11px] font-medium text-zinc-400">{item.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
