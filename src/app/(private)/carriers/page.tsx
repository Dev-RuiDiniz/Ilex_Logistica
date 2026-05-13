"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import { createCarrier, inactivateCarrier, listCarriers, updateCarrier } from "@/lib/api";
import { canEditCarriers } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";
import type { Carrier } from "@/lib/types";

type FormState = {
  id?: number;
  name: string;
  external_code: string;
  metadata_json: string;
};

const initialForm: FormState = { name: "", external_code: "", metadata_json: "{}" };

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

  const editable = canEditCarriers(session?.role ?? "auditoria");

  const load = async () => {
    if (!session) return;
    setLoading(true);
    setError("");
    try {
      const data = await listCarriers(session.accessToken);
      setItems(data);
    } catch {
      setError("Não foi possível carregar transportadoras.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session?.accessToken]);

  const filtered = useMemo(
    () => items.filter((item) => item.name.toLowerCase().includes(query.toLowerCase())),
    [items, query],
  );

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!session || !editable) return;
    setSaving(true);
    setError("");
    setFormError("");
    try {
      if (form.name.trim().length < 2) {
        throw new Error("Nome inválido");
      }
      const parsed = JSON.parse(form.metadata_json || "{}") as Record<string, unknown>;
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
    } catch {
      setFormError("Falha ao salvar transportadora. Verifique nome e metadados JSON.");
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
      setItems((prev) => prev.filter((x) => x.id !== item.id));
    } catch {
      setError("Falha ao inativar transportadora.");
    } finally {
      setInactivatingId(null);
    }
  };

  return (
    <section className="space-y-4">
      <header className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-semibold">Transportadoras</h2>
          <p className="text-sm text-slate-600">Listagem com filtro, cadastro, edição e inativação.</p>
        </div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Buscar por nome"
          className="w-full rounded border px-3 py-2 text-sm md:w-64"
        />
      </header>

      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      {!editable && <p className="rounded bg-amber-50 px-3 py-2 text-sm text-amber-700">Perfil com permissão somente leitura.</p>}

      <div className="overflow-hidden rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-3 py-2">Nome</th>
              <th className="px-3 py-2">Código</th>
              <th className="px-3 py-2">Status</th>
              {editable && <th className="px-3 py-2">Ações</th>}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={editable ? 4 : 3} className="px-3 py-3 text-slate-500">
                  Carregando...
                </td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={editable ? 4 : 3} className="px-3 py-3 text-slate-500">
                  Nenhuma transportadora encontrada.
                </td>
              </tr>
            ) : (
              filtered.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-3 py-2">{item.name}</td>
                  <td className="px-3 py-2">{item.external_code ?? "-"}</td>
                  <td className="px-3 py-2">{item.is_active ? "Ativo" : "Inativo"}</td>
                  {editable && (
                    <td className="px-3 py-2">
                      <div className="flex gap-2">
                        <button onClick={() => onEdit(item)} className="rounded border px-2 py-1">
                          Editar
                        </button>
                        <button
                          onClick={() => onInactivate(item)}
                          className="rounded border px-2 py-1 text-red-700"
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
        <form onSubmit={onSubmit} className="grid gap-3 rounded border p-4 md:grid-cols-2">
          <h3 className="md:col-span-2 text-base font-semibold">
            {form.id ? "Editar transportadora" : "Nova transportadora"}
          </h3>
          <input
            value={form.name}
            onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            placeholder="Nome"
            required
            minLength={2}
            className="rounded border px-3 py-2"
          />
          <input
            value={form.external_code}
            onChange={(e) => setForm((f) => ({ ...f, external_code: e.target.value }))}
            placeholder="Código externo"
            className="rounded border px-3 py-2"
          />
          <textarea
            value={form.metadata_json}
            onChange={(e) => setForm((f) => ({ ...f, metadata_json: e.target.value }))}
            className="md:col-span-2 min-h-24 rounded border px-3 py-2 font-mono text-sm"
          />
          {formError && <p className="md:col-span-2 rounded bg-red-50 px-3 py-2 text-sm text-red-700">{formError}</p>}
          <div className="md:col-span-2 flex gap-2">
            <button type="submit" disabled={saving} className="rounded bg-slate-900 px-4 py-2 text-white">
              {saving ? "Salvando..." : form.id ? "Atualizar" : "Cadastrar"}
            </button>
            <button
              type="button"
              onClick={() => setForm(initialForm)}
              className="rounded border px-4 py-2"
            >
              Limpar
            </button>
          </div>
        </form>
      )}
    </section>
  );
}
