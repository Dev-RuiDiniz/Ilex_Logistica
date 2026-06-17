"use client";

import { useEffect, useState } from "react";

import { listExceptionShipments } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { Shipment } from "@/lib/types";

export default function ExceptionsPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<Shipment[]>([]);
  const [criticality, setCriticality] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      setLoading(true);
      setError("");
      try {
        const response = await listExceptionShipments(session.accessToken, {
          criticality: criticality || undefined,
          sort_by: "delay_days",
          sort_order: "desc",
        });
        if (!cancelled) setItems(response.items);
      } catch (err) {
        if (!cancelled) {
          handleApiError(err instanceof Error ? err : new Error("Não foi possível carregar exceções"));
          setError(err instanceof Error ? err.message : "Não foi possível carregar exceções");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session, criticality, handleApiError]);

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  return (
    <section className="space-y-4">
      <header className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">Painel de Exceções</h2>
          <p className="text-sm text-slate-600">Fila priorizada por atraso e criticidade.</p>
        </div>
        <select value={criticality} onChange={(e) => setCriticality(e.target.value)} className="rounded border px-3 py-2 text-sm">
          <option value="">Todas</option>
          <option value="baixa">Baixa</option>
          <option value="media">Média</option>
          <option value="alta">Alta</option>
        </select>
      </header>
      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      <div className="overflow-hidden rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-3 py-2">Tracking</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Atraso</th>
              <th className="px-3 py-2">Criticidade</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td className="px-3 py-3 text-slate-500" colSpan={4}>Carregando...</td></tr>
            ) : items.length === 0 ? (
              <tr><td className="px-3 py-3 text-slate-500" colSpan={4}>Sem exceções no momento.</td></tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-3 py-2">
                    <a className="text-blue-700 hover:underline" href={`/shipments/${item.id}`}>{item.tracking_code}</a>
                  </td>
                  <td className="px-3 py-2">{item.status}</td>
                  <td className="px-3 py-2">{item.delay_days}</td>
                  <td className="px-3 py-2">{item.criticality}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
