"use client";

import { useEffect, useState } from "react";

import { getDailyReport } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import type { DailyReportResponse } from "@/lib/types";

export default function DailyReportPage() {
  const { session } = useAuth();
  const [report, setReport] = useState<DailyReportResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      if (!session) return;
      try {
        setReport(await getDailyReport(session.accessToken));
      } catch {
        setError("Falha ao carregar relatório diário.");
      }
    };
    void load();
  }, [session?.accessToken]);

  const exportCsv = () => {
    if (!report) return;
    const lines = [
      "metric,value",
      `report_date,${report.report_date}`,
      `total_shipments,${report.total_shipments}`,
      `total_exceptions,${report.total_exceptions}`,
      ...Object.entries(report.by_criticality).map(([k, v]) => `criticality_${k},${v}`),
    ];
    const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `relatorio_diario_${report.report_date}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="space-y-4">
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Relatório Diário</h2>
          <p className="text-sm text-slate-600">Visão executiva consolidada da operação.</p>
        </div>
        <button className="rounded bg-slate-900 px-4 py-2 text-sm text-white" onClick={exportCsv} disabled={!report}>
          Exportar CSV
        </button>
      </header>
      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      {report && (
        <>
          <div className="grid gap-3 md:grid-cols-3">
            <div className="rounded border p-3"><strong>Total de envios:</strong> {report.total_shipments}</div>
            <div className="rounded border p-3"><strong>Total de exceções:</strong> {report.total_exceptions}</div>
            <div className="rounded border p-3"><strong>Data:</strong> {report.report_date}</div>
          </div>
          <div className="rounded border p-4">
            <h3 className="mb-2 text-base font-semibold">Criticidade</h3>
            <ul className="space-y-1 text-sm">
              {Object.entries(report.by_criticality).map(([k, v]) => (
                <li key={k}>{k}: {v}</li>
              ))}
            </ul>
          </div>
        </>
      )}
    </section>
  );
}
