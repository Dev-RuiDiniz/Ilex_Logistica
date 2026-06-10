"use client";

import { FormEvent, useEffect, useState } from "react";

import { createSlaRule, listSlaRules, recalculateSla, updateSlaRule } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import { handleApiError } from "@/lib/error-handler";
import type { SlaRule, SlaRuleCreate } from "@/lib/types";

export default function SlaRulesPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<SlaRule[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [isRecalculating, setIsRecalculating] = useState(false);
  const [recalcResult, setRecalcResult] = useState<{ processed_count: number; updated_count: number; skipped_count: number; error_count: number } | null>(null);

  // Form state
  const [transitDays, setTransitDays] = useState("");
  const [warningThresholdDays, setWarningThresholdDays] = useState("");
  const [criticalDelayDays, setCriticalDelayDays] = useState("");
  const [carrierId, setCarrierId] = useState("");
  const [destinationUf, setDestinationUf] = useState("");
  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      setLoading(true);
      try {
        const rules = await listSlaRules(session.accessToken);
        if (!cancelled) setItems(rules);
      } catch (err) {
        if (!cancelled) setError(handleApiError(err));
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session]);

  const reloadRules = async () => {
    if (!session) return;
    try {
      setItems(await listSlaRules(session.accessToken));
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const onCreate = async (event: FormEvent) => {
    event.preventDefault();
    if (!session) return;
    setIsCreating(true);
    try {
      const payload: SlaRuleCreate = {
        transit_days: parseInt(transitDays, 10),
        warning_threshold_days: parseInt(warningThresholdDays, 10),
        critical_delay_days: parseInt(criticalDelayDays, 10),
        carrier_id: carrierId ? parseInt(carrierId, 10) : null,
        destination_uf: destinationUf || null,
        is_active: isActive,
      };
      await createSlaRule(session.accessToken, payload);
      setTransitDays("");
      setWarningThresholdDays("");
      setCriticalDelayDays("");
      setCarrierId("");
      setDestinationUf("");
      setIsActive(true);
      await reloadRules();
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsCreating(false);
    }
  };

  const onToggleActive = async (rule: SlaRule) => {
    if (!session) return;
    try {
      await updateSlaRule(session.accessToken, rule.id, { is_active: !rule.is_active });
      await reloadRules();
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const onRecalculate = async () => {
    if (!session) return;
    setIsRecalculating(true);
    setRecalcResult(null);
    try {
      const result = await recalculateSla(session.accessToken);
      setRecalcResult(result);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setIsRecalculating(false);
    }
  };

  const getRuleDescription = (rule: SlaRule) => {
    if (rule.carrier_id && rule.destination_uf) {
      return `Transportadora ${rule.carrier_id} - UF ${rule.destination_uf}`;
    }
    if (rule.carrier_id) {
      return `Transportadora ${rule.carrier_id}`;
    }
    return "Global";
  };

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Regras SLA</h2>
        <p className="text-sm text-slate-600">Configuração de prazos e alertas de SLA.</p>
      </header>

      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {/* Reprocessamento */}
      <div className="rounded border bg-white p-4">
        <h3 className="text-sm font-semibold mb-2">Reprocessamento SLA</h3>
        <button
          onClick={onRecalculate}
          disabled={isRecalculating}
          className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
        >
          {isRecalculating ? "Reprocessando..." : "Reprocessar SLA"}
        </button>
        {recalcResult && (
          <div className="mt-2 text-sm">
            <p>Processados: {recalcResult.processed_count}</p>
            <p>Atualizados: {recalcResult.updated_count}</p>
            <p>Pulados: {recalcResult.skipped_count}</p>
            <p>Erros: {recalcResult.error_count}</p>
          </div>
        )}
      </div>

      {/* Criar regra */}
      <form onSubmit={onCreate} className="grid gap-2 rounded border p-4 md:grid-cols-6">
        <input
          value={transitDays}
          onChange={(e) => setTransitDays(e.target.value)}
          className="rounded border px-3 py-2 text-sm"
          placeholder="Prazo (dias)"
          type="number"
          min="1"
          required
        />
        <input
          value={warningThresholdDays}
          onChange={(e) => setWarningThresholdDays(e.target.value)}
          className="rounded border px-3 py-2 text-sm"
          placeholder="Aviso (dias)"
          type="number"
          min="1"
          required
        />
        <input
          value={criticalDelayDays}
          onChange={(e) => setCriticalDelayDays(e.target.value)}
          className="rounded border px-3 py-2 text-sm"
          placeholder="Crítico (dias)"
          type="number"
          min="1"
          required
        />
        <input
          value={carrierId}
          onChange={(e) => setCarrierId(e.target.value)}
          className="rounded border px-3 py-2 text-sm"
          placeholder="ID Transportadora (opcional)"
          type="number"
        />
        <input
          value={destinationUf}
          onChange={(e) => setDestinationUf(e.target.value.toUpperCase())}
          className="rounded border px-3 py-2 text-sm uppercase"
          placeholder="UF (opcional)"
          maxLength={2}
        />
        <button
          className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
          type="submit"
          disabled={isCreating}
        >
          {isCreating ? "Criando..." : "Criar"}
        </button>
      </form>

      {/* Lista de regras */}
      <div className="overflow-hidden rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-3 py-2">Descrição</th>
              <th className="px-3 py-2">Prazo (dias)</th>
              <th className="px-3 py-2">Aviso (dias)</th>
              <th className="px-3 py-2">Crítico (dias)</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Ações</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-3 py-3 text-slate-500">
                  Carregando...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-3 py-3 text-slate-500">
                  Nenhuma regra SLA encontrada.
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-3 py-2">{getRuleDescription(item)}</td>
                  <td className="px-3 py-2">{item.transit_days}</td>
                  <td className="px-3 py-2">{item.warning_threshold_days}</td>
                  <td className="px-3 py-2">{item.critical_delay_days}</td>
                  <td className="px-3 py-2">
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${item.is_active ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-800"}`}>
                      {item.is_active ? "Ativa" : "Inativa"}
                    </span>
                  </td>
                  <td className="px-3 py-2">
                    <button
                      onClick={() => onToggleActive(item)}
                      className="rounded border px-2 py-1 text-xs disabled:opacity-60"
                      disabled={isCreating}
                    >
                      {item.is_active ? "Inativar" : "Ativar"}
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
