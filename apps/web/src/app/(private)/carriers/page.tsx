"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import { AccessDenied } from "@/components/AccessDenied";
import { useAuth } from "@/features/auth/auth-provider";
import { createCarrier, inactivateCarrier, listCarriers, updateCarrier } from "@/lib/api";
import { canEditCarriers } from "@/lib/permissions";
import type { Carrier } from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

type FormState = {
  id?: number;
  name: string;
  external_code: string;
  metadata_json: string;
};

const initialForm: FormState = { name: "", external_code: "", metadata_json: "{}" };

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
  const [formError, setFormError] = useState("");
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  const editable = canEditCarriers(session?.role ?? "auditoria");

  const load = async () => {
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
  };

  useEffect(() => {
    void load();
  }, [session?.accessToken]); // eslint-disable-line react-hooks/exhaustive-deps

  const filtered = useMemo(() => filterCarriersByQuery(items, query), [items, query]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!session || !editable) return;
    setSaving(true);
    setError("");
    setFormError("");
    try {
      if (!validateCarrierName(form.name)) {
        throw new Error("Nome invalido");
      }
      const parsed = parseIntegrationMetadata(form.metadata_json);
      if (form.id) {
        await updateCarrier(session.accessToken, form.id, {
          name: form.name,
          external_code: form.external_code,
          integration_metadata: parsed,
        });
      } else {
        await createCarrier(session.accessToken, {
          name: form.name,
          external_code: form.external_code,
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

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  return (
    <section className="page-stack">
      <header className="page-hero">
        <p className="page-kicker">Rede de transporte</p>
        <h2 className="page-title !text-[clamp(1.65rem,1.3rem+0.8vw,2.4rem)]">Transportadoras</h2>
        <p className="page-subtitle">
          Organize parceiros, códigos e metadados com uma visão clara da rede ativa e do
          que exige manutenção.
        </p>
      </header>

      <div className="surface-panel p-5 md:p-6">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="section-title">Cadastro e acompanhamento</h3>
            <p className="section-subtitle">Encontre rápido, edite com clareza e mantenha a base consistente.</p>
          </div>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar por nome"
            className="field md:w-72"
          />
        </div>
      </div>

      {error && <p className="error-state">{error}</p>}
      {!editable && (
        <p className="surface-muted px-4 py-3 text-sm text-amber-700">Perfil com permissao somente leitura.</p>
      )}

      <div className="table-shell">
        <table className="data-table">
          <thead className="text-left">
            <tr>
              <th className="px-3 py-2">Nome</th>
              <th className="px-3 py-2">Codigo</th>
              <th className="px-3 py-2">Status</th>
              {editable && <th className="px-3 py-2">Acoes</th>}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={editable ? 4 : 3} className="px-3 py-3 text-slate-700">
                  Carregando...
                </td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={editable ? 4 : 3} className="px-3 py-3 text-slate-700">
                  Nenhuma transportadora encontrada.
                </td>
              </tr>
            ) : (
              filtered.map((item) => (
                <tr key={item.id}>
                  <td className="px-3 py-2">{item.name}</td>
                  <td className="px-3 py-2">{item.external_code ?? "-"}</td>
                  <td className="px-3 py-2">{item.is_active ? "Ativo" : "Inativo"}</td>
                  {editable && (
                    <td className="px-3 py-2">
                      <div className="flex gap-2">
                        <button onClick={() => onEdit(item)} className="button-secondary !px-3 !py-2">
                          Editar
                        </button>
                        <button
                          onClick={() => onInactivate(item)}
                          className="button-danger !px-3 !py-2"
                          disabled={inactivatingId === item.id}
                        >
                          {inactivatingId === item.id ? "Inativando..." : "Inativar"}
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

      {editable && (
        <form onSubmit={onSubmit} className="surface-panel grid gap-3 p-5 md:grid-cols-2 md:p-6">
          <h3 className="section-title md:col-span-2">
            {form.id ? "Editar transportadora" : "Nova transportadora"}
          </h3>
          <input
            value={form.name}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            placeholder="Nome"
            required
            minLength={2}
            className="field"
          />
          <input
            value={form.external_code}
            onChange={(e) => setForm((f) => ({ ...f, external_code: e.target.value }))}
            placeholder="Codigo externo"
            className="field"
          />
          <textarea
            value={form.metadata_json}
            onChange={(e) => setForm((f) => ({ ...f, metadata_json: e.target.value }))}
            className="field-textarea min-h-24 font-mono text-sm md:col-span-2"
          />
          {formError && <p className="error-state md:col-span-2">{formError}</p>}
          <div className="flex gap-2 md:col-span-2">
            <button type="submit" disabled={saving} className="button-primary">
              {saving ? "Salvando..." : form.id ? "Atualizar" : "Cadastrar"}
            </button>
            <button type="button" onClick={() => setForm(initialForm)} className="button-ghost">
              Limpar
            </button>
          </div>
        </form>
      )}
    </section>
  );
}
