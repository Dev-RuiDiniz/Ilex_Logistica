"use client";

import Link from "next/link";
import { ChangeEvent, FormEvent, useCallback, useEffect, useState } from "react";

import { AccessDenied } from "@/components/AccessDenied";
import { useAuth } from "@/features/auth/auth-provider";
import { confirmOrderImport, listOrders, previewOrderImport } from "@/lib/api";
import { canReadOrders, canWriteOrders } from "@/lib/permissions";
import type { Order, OrderImportPreview } from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

const money = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

export default function OrdersPage() {
  const { session } = useAuth();
  const role = session?.role ?? "auditoria";
  const readable = canReadOrders(role);
  const writable = canWriteOrders(role);
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();
  const [items, setItems] = useState<Order[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<OrderImportPreview | null>(null);
  const [importing, setImporting] = useState(false);
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    if (!session || !readable) return;
    setLoading(true);
    setError("");
    try {
      const data = await listOrders(session.accessToken, {
        page,
        page_size: 20,
        status: status || undefined,
        external_number: query || undefined,
      });
      setItems(data.items);
      setTotal(data.total);
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro ao carregar pedidos");
      handleApiError(apiError);
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  }, [handleApiError, page, query, readable, session, status]);

  useEffect(() => {
    queueMicrotask(() => void load());
  }, [load]);

  const onFilter = (event: FormEvent) => {
    event.preventDefault();
    setPage(1);
    void load();
  };

  const onFile = (event: ChangeEvent<HTMLInputElement>) => {
    setFile(event.target.files?.[0] ?? null);
    setPreview(null);
    setNotice("");
  };

  const onPreview = async () => {
    if (!session || !file || !writable) return;
    setImporting(true);
    setError("");
    try {
      setPreview(await previewOrderImport(session.accessToken, file));
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro no preview");
      handleApiError(apiError);
      setError(apiError.message);
    } finally {
      setImporting(false);
    }
  };

  const onConfirm = async () => {
    if (!session || !preview || !writable) return;
    setImporting(true);
    try {
      const result = await confirmOrderImport(session.accessToken, preview.import_id);
      setNotice(`${result.imported_count} pedido(s) processado(s); ${result.rejected_count} rejeitado(s).`);
      setPreview(null);
      setFile(null);
      await load();
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro ao confirmar importação");
      handleApiError(apiError);
      setError(apiError.message);
    } finally {
      setImporting(false);
    }
  };

  if (!readable || accessDenied) return <AccessDenied message={accessDeniedMessage || "Sem acesso a pedidos."} />;

  return (
    <section className="space-y-5">
      <header>
        <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Pedidos e cotações</h1>
        <p className="mt-1 text-sm text-zinc-500">Importe pedidos ERP e acompanhe rodadas de frete.</p>
      </header>

      {writable && (
        <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm" aria-labelledby="import-title">
          <h2 id="import-title" className="font-bold text-zinc-900">Importar pedidos ERP</h2>
          <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-end">
            <label className="flex-1 text-sm font-medium text-zinc-700">
              Arquivo CSV ou XLSX
              <input className="mt-1 block w-full rounded-lg border border-zinc-200 p-2 text-sm" type="file" accept=".csv,.xlsx" onChange={onFile} />
            </label>
            <button className="rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50" disabled={!file || importing} onClick={onPreview}>
              {importing ? "Validando..." : "Gerar preview"}
            </button>
          </div>
          {preview && (
            <div className="mt-4 rounded-xl bg-zinc-50 p-4" aria-live="polite">
              <p className="text-sm text-zinc-700">{preview.valid_rows} válidos · {preview.invalid_rows} inválidos · {preview.duplicate_rows} duplicados</p>
              {preview.errors.length > 0 && <p className="mt-1 text-sm text-red-700">Primeiro erro: linha {preview.errors[0].row_number} — {preview.errors[0].message}</p>}
              <button className="mt-3 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50" disabled={preview.valid_rows === 0 || importing} onClick={onConfirm}>Confirmar importação</button>
            </div>
          )}
        </div>
      )}

      {(error || notice) && <div role="status" aria-live="polite" className={`rounded-xl border px-4 py-3 text-sm ${error ? "border-red-200 bg-red-50 text-red-700" : "border-emerald-200 bg-emerald-50 text-emerald-700"}`}>{error || notice}</div>}

      <form onSubmit={onFilter} className="grid gap-3 rounded-2xl border border-zinc-200 bg-white p-4 sm:grid-cols-[1fr_180px_auto]">
        <label className="text-sm font-medium text-zinc-700">Número externo<input value={query} onChange={(event) => setQuery(event.target.value)} className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2" /></label>
        <label className="text-sm font-medium text-zinc-700">Status<select value={status} onChange={(event) => setStatus(event.target.value)} className="mt-1 w-full rounded-lg border border-zinc-200 px-3 py-2"><option value="">Todos</option><option value="active">Ativos</option><option value="cancelled">Cancelados</option></select></label>
        <button className="self-end rounded-lg border border-zinc-300 px-4 py-2 text-sm font-semibold">Filtrar</button>
      </form>

      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="border-b border-zinc-100 px-5 py-3 text-sm font-semibold text-zinc-700">{total} pedido(s)</div>
        {loading ? <p className="p-8 text-center text-sm text-zinc-500" role="status">Carregando pedidos...</p> : items.length === 0 ? <p className="p-8 text-center text-sm text-zinc-500">Nenhum pedido encontrado.</p> : (
          <>
            <div className="hidden overflow-x-auto md:block"><table className="w-full text-sm"><thead className="bg-zinc-50 text-left text-xs uppercase text-zinc-500"><tr><th className="px-5 py-3">Pedido</th><th className="px-5 py-3">Cliente</th><th className="px-5 py-3">Rota</th><th className="px-5 py-3">Valor</th><th className="px-5 py-3">Status</th></tr></thead><tbody>{items.map((order) => <tr key={order.id} className="border-t border-zinc-100"><td className="px-5 py-3 font-semibold"><Link className="text-red-700 hover:underline" href={`/orders/${order.id}`}>{order.external_number}</Link><span className="block text-xs font-normal text-zinc-400">{order.source}</span></td><td className="px-5 py-3">{order.customer_name}</td><td className="px-5 py-3">{order.origin_uf} → {order.destination_uf}</td><td className="px-5 py-3">{money.format(Number(order.goods_value))}</td><td className="px-5 py-3">{order.status === "active" ? "Ativo" : "Cancelado"}</td></tr>)}</tbody></table></div>
            <div className="divide-y divide-zinc-100 md:hidden">{items.map((order) => <Link key={order.id} href={`/orders/${order.id}`} className="block p-4 focus:outline-none focus:ring-2 focus:ring-red-500"><strong>{order.external_number}</strong><span className="mt-1 block text-sm text-zinc-600">{order.customer_name}</span><span className="mt-2 block text-xs text-zinc-500">{order.origin_uf} → {order.destination_uf} · {money.format(Number(order.goods_value))}</span></Link>)}</div>
          </>
        )}
        <div className="flex justify-end gap-2 border-t border-zinc-100 p-3"><button className="rounded border px-3 py-1.5 text-sm disabled:opacity-40" disabled={page === 1} onClick={() => setPage((value) => value - 1)}>Anterior</button><button className="rounded border px-3 py-1.5 text-sm disabled:opacity-40" disabled={page * 20 >= total} onClick={() => setPage((value) => value + 1)}>Próxima</button></div>
      </div>
    </section>
  );
}
