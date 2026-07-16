"use client";

import { useState } from "react";

import { dispatchCharge } from "@/lib/api";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { useAuth } from "@/features/auth/auth-provider";
import type { Carrier, ChargeDispatchRequest, ChargeDispatchResponse } from "@/lib/types";

function IconX({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

export default function ChargeDispatchModal({
  carriers,
  defaultCarrierId,
  onClose,
}: {
  carriers: Carrier[];
  defaultCarrierId?: number | null;
  onClose: () => void;
}) {
  const [carrierId, setCarrierId] = useState<string>(defaultCarrierId ? String(defaultCarrierId) : "0");
  const [destinationUf, setDestinationUf] = useState("");
  const [diasMin, setDiasMin] = useState("1");
  const [diasMax, setDiasMax] = useState("999");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ChargeDispatchResponse | null>(null);
  const { session } = useAuth();
  const { handleApiError } = useApiErrorHandler();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    const payload: ChargeDispatchRequest = {
      carrier_id: carrierId && carrierId !== "0" ? Number(carrierId) : null,
      destination_uf: destinationUf.trim().toUpperCase() || null,
      dias_min: Number(diasMin) || 1,
      dias_max: Number(diasMax) || 999,
    };
    try {
      const response = await dispatchCharge(session?.accessToken ?? "", payload);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao disparar cobrança");
      handleApiError(err instanceof Error ? err : new Error("Erro ao disparar cobrança"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div className="w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl border border-zinc-200 bg-white shadow-2xl">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <div>
            <h2 className="text-lg font-bold text-zinc-900">Disparar cobrança</h2>
            <p className="text-xs text-zinc-500">Envia lembretes WhatsApp para transportadoras com remessas atrasadas</p>
          </div>
          <button onClick={onClose} className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600">
            <IconX className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={onSubmit} className="space-y-5 p-6">
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}

          {result && (
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700">
              <p>Disparo concluído:</p>
              <ul className="mt-1 list-disc pl-5">
                <li>Enviadas: {result.enviadas}</li>
                <li>Puladas (sem WhatsApp): {result.puladas_sem_whatsapp}</li>
                <li>Falhas: {result.falhas}</li>
                <li>Críticas escalonadas: {result.critico_escalonado}</li>
              </ul>
            </div>
          )}

          <div>
            <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Transportadora</label>
            <select value={carrierId} onChange={(e) => setCarrierId(e.target.value)} className="input">
              <option value="0">Todas</option>
              {carriers.map((carrier) => (
                <option key={carrier.id} value={carrier.id}>{carrier.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">UF destino</label>
            <input
              value={destinationUf}
              onChange={(e) => setDestinationUf(e.target.value.toUpperCase())}
              placeholder="SP"
              maxLength={2}
              className="input"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atraso mín. (dias)</label>
              <input type="number" min="1" value={diasMin} onChange={(e) => setDiasMin(e.target.value)} className="input" />
            </div>
            <div>
              <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atraso máx. (dias)</label>
              <input type="number" min="1" value={diasMax} onChange={(e) => setDiasMax(e.target.value)} className="input" />
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 border-t border-zinc-100 pt-5">
            <button type="button" onClick={onClose} className="btn-secondary" disabled={loading}>
              Fechar
            </button>
            <button type="submit" className="btn-primary flex items-center gap-2" disabled={loading}>
              {loading && <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-red-600" />}
              Disparar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
