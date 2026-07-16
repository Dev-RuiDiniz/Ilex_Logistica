"use client";

import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";

import { AccessDenied } from "@/components/AccessDenied";
import { useAuth } from "@/features/auth/auth-provider";
import { createCarrier, inactivateCarrier, listCarriers, updateCarrier } from "@/lib/api";
import { canEditCarriers } from "@/lib/permissions";
import type { Carrier } from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import ChargeDispatchModal from "../shipments/ChargeDispatchModal";

type FormState = {
  id?: number;
  name: string;
  external_code: string;
  whatsapp: string;
  email: string;
  metadata_json: string;
};

const initialForm: FormState = { name: "", external_code: "", whatsapp: "", email: "", metadata_json: "{}" };

export function filterCarriersByQuery(items: Carrier[], query: string): Carrier[] {
  return items.filter((item) => item.name.toLowerCase().includes(query.toLowerCase()));
}

export function validateCarrierName(name: string): boolean {
  return name.trim().length >= 2;
}

export function parseIntegrationMetadata(metadataJson: string): Record<string, unknown> {
  return JSON.parse(metadataJson || "{}") as Record<string, unknown>;
}

export function removeCarrierById(items: Carrier[], id: number): Carrier[] {
  return items.filter((item) => item.id !== id);
}

export default function CarriersPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<Carrier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const [form, setForm] = useState<FormState>(initialForm);
  const [saving, setSaving] = useState(false);
  const [inactivatingId, setInactivatingId] = useState<number | null>(null);
  const [showChargeModal, setShowChargeModal] = useState(false);
  const [chargeCarrierId, setChargeCarrierId] = useState<number | null>(null);
  const [formError, setFormError] = useState("");
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  const editable = canEditCarriers(session?.role ?? "auditoria");

  const load = useCallback(async () => {
    if (!session) return;
    setLoading(true);
    setError("");
    try {
      const data = await listCarriers(session.accessToken);
      setItems(data);
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar transportadoras"));
      setError(err instanceof Error ? err.message : "Erro ao carregar transportadoras");
    } finally {
      setLoading(false);
    }
  }, [handleApiError, session]);

  useEffect(() => {
    queueMicrotask(() => void load());
  }, [load]);

  const filtered = useMemo(() => filterCarriersByQuery(items, query), [items, query]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!session || !editable) return;
    setSaving(true);
    setError("");
    setFormError("");
    try {
      if (!validateCarrierName(form.name)) {
        throw new Error("Nome inválido");
      }
      const parsed = parseIntegrationMetadata(form.metadata_json);
      if (form.id) {
        await updateCarrier(session.accessToken, form.id, {
          name: form.name,
          external_code: form.external_code,
          whatsapp: form.whatsapp || null,
          email: form.email || null,
          integration_metadata: parsed,
        });
      } else {
        await createCarrier(session.accessToken, {
          name: form.name,
          external_code: form.external_code,
          whatsapp: form.whatsapp || null,
          email: form.email || null,
          integration_metadata: parsed,
        });
      }
      setForm(initialForm);
      await load();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao salvar transportadora"));
      setFormError(err instanceof Error ? err.message : "Erro ao salvar transportadora");
    } finally {
      setSaving(false);
    }
  };

  const onEdit = (item: Carrier) => {
    setForm({
      id: item.id,
      name: item.name,
      external_code: item.external_code ?? "",
      whatsapp: item.whatsapp ?? "",
      email: item.email ?? "",
      metadata_json: JSON.stringify(item.integration_metadata ?? {}, null, 0),
    });
  };

  const onInactivate = async (item: Carrier) => {
    if (!session || !editable) return;
    if (!window.confirm(`Deseja inativar a transportadora ${item.name}?`)) return;
    setInactivatingId(item.id);
    try {
      await inactivateCarrier(session.accessToken, item.id);
      setItems((prev) => removeCarrierById(prev, item.id));
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao inativar transportadora"));
      setError(err instanceof Error ? err.message : "Erro ao inativar transportadora");
    } finally {
      setInactivatingId(null);
    }
  };

  const inputClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800 disabled:opacity-50";
  const btnSecondary = "rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50 disabled:opacity-50";

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  return (
    <section className="space-y-5">
      {/* Header */}
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Transportadoras</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Cadastro, edição e gestão de transportadoras</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <svg className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Buscar por nome..."
              className="w-full rounded-lg border border-zinc-200 bg-white py-2.5 pl-10 pr-4 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 md:w-64"
            />
          </div>
        </div>
      </header>

      {/* Alerts */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}
      {!editable && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-700">
          Perfil com permissão somente leitura.
        </div>
      )}

      {/* Table */}
      <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <p className="text-sm font-semibold text-zinc-700">
            {filtered.length} transportadora{filtered.length !== 1 ? "s" : ""} encontrada{filtered.length !== 1 ? "s" : ""}
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-100 bg-zinc-50/80">
                <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Nome</th>
                <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Código</th>
                <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">WhatsApp</th>
                <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Email</th>
                <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                {editable && <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ações</th>}
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={editable ? 6 : 5} className="px-6 py-8 text-center text-sm text-zinc-400">
                    <div className="flex items-center justify-center gap-2">
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
                      Carregando...
                    </div>
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan={editable ? 6 : 5} className="px-6 py-8 text-center text-sm text-zinc-400">
                    Nenhuma transportadora encontrada.
                  </td>
                </tr>
              ) : (
                filtered.map((item) => (
                  <tr key={item.id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                    <td className="px-6 py-3.5 font-semibold text-zinc-900">{item.name}</td>
                    <td className="px-6 py-3.5 font-mono text-xs text-zinc-600">{item.external_code ?? "-"}</td>
                    <td className="px-6 py-3.5 text-xs text-zinc-600">{item.whatsapp ?? "-"}</td>
                    <td className="px-6 py-3.5 text-xs text-zinc-600">{item.email ?? "-"}</td>
                    <td className="px-6 py-3.5">
                      <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold ${
                        item.is_active
                          ? "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20"
                          : "bg-zinc-100 text-zinc-500 ring-1 ring-zinc-300"
                      }`}>
                        {item.is_active ? "Ativo" : "Inativo"}
                      </span>
                    </td>
                    {editable && (
                      <td className="px-6 py-3.5">
                        <div className="flex justify-end gap-2">
                          <button
                            onClick={() => onEdit(item)}
                            className="rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => onInactivate(item)}
                            disabled={inactivatingId === item.id}
                            className="rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-semibold text-red-600 transition-all hover:border-red-300 hover:bg-red-50 disabled:opacity-50"
                          >
                            {inactivatingId === item.id ? "Inativando..." : "Inativar"}
                          </button>
                          <button
                            onClick={() => { setChargeCarrierId(item.id); setShowChargeModal(true); }}
                            className="rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
                          >
                            Cobrar
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Form */}
      {editable && (
        <form onSubmit={onSubmit} className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-base font-bold text-zinc-900">
            {form.id ? "Editar Transportadora" : "Nova Transportadora"}
          </h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Nome</label>
              <input
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                placeholder="Nome da transportadora"
                required
                minLength={2}
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Código externo</label>
              <input
                value={form.external_code}
                onChange={(e) => setForm((f) => ({ ...f, external_code: e.target.value }))}
                placeholder="Código (opcional)"
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">WhatsApp</label>
              <input
                value={form.whatsapp}
                onChange={(e) => setForm((f) => ({ ...f, whatsapp: e.target.value }))}
                placeholder="+55 11 99999-9999"
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Email</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                placeholder="contato@transportadora.com"
                className={inputClass}
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Metadados de integração (JSON)</label>
              <textarea
                value={form.metadata_json}
                onChange={(e) => setForm((f) => ({ ...f, metadata_json: e.target.value }))}
                placeholder='{"key": "value"}'
                className={`${inputClass} min-h-24 font-mono`}
              />
            </div>
          </div>

          {formError && (
            <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {formError}
            </div>
          )}

          <div className="mt-5 flex gap-2">
            <button type="submit" disabled={saving} className={btnPrimary}>
              {saving ? "Salvando..." : form.id ? "Atualizar" : "Cadastrar"}
            </button>
            <button type="button" onClick={() => setForm(initialForm)} className={btnSecondary}>
              Limpar
            </button>
          </div>
        </form>
      )}

      {showChargeModal && (
        <ChargeDispatchModal
          carriers={items}
          defaultCarrierId={chargeCarrierId}
          onClose={() => { setShowChargeModal(false); setChargeCarrierId(null); }}
        />
      )}
    </section>
  );
}
