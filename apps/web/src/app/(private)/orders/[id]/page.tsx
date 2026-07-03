"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { AccessDenied } from "@/components/AccessDenied";
import { useAuth } from "@/features/auth/auth-provider";
import { createQuoteRound, getOrder, listQuoteRounds } from "@/lib/api";
import { canReadOrders, canWriteQuotes } from "@/lib/permissions";
import type { Order, QuoteRound } from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

export default function OrderDetailPage() {
  const params = useParams<{ id: string }>();
  const orderId = Number(params.id);
  const { session } = useAuth();
  const role = session?.role ?? "auditoria";
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();
  const [order, setOrder] = useState<Order | null>(null);
  const [rounds, setRounds] = useState<QuoteRound[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  const load = useCallback(async () => {
    if (!session || !canReadOrders(role) || !Number.isInteger(orderId)) return;
    setLoading(true);
    try {
      const [orderData, roundData] = await Promise.all([
        getOrder(session.accessToken, orderId),
        listQuoteRounds(session.accessToken, orderId),
      ]);
      setOrder(orderData);
      setRounds(roundData);
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro ao carregar pedido");
      handleApiError(apiError);
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  }, [handleApiError, orderId, role, session]);

  useEffect(() => { queueMicrotask(() => void load()); }, [load]);

  const createRound = async () => {
    if (!session) return;
    setCreating(true);
    try {
      const created = await createQuoteRound(session.accessToken, orderId);
      setRounds((current) => [created, ...current]);
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro ao criar rodada");
      handleApiError(apiError);
      setError(apiError.message);
    } finally {
      setCreating(false);
    }
  };

  if (!canReadOrders(role) || accessDenied) return <AccessDenied message={accessDeniedMessage || "Sem acesso ao pedido."} />;
  if (loading) return <p role="status" className="p-8 text-sm text-zinc-500">Carregando pedido...</p>;
  if (!order) return <div role="alert" className="rounded-xl bg-red-50 p-4 text-red-700">{error || "Pedido não encontrado."}</div>;

  return (
    <section className="space-y-5">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div><Link href="/orders" className="text-sm text-red-700 hover:underline">← Pedidos</Link><h1 className="mt-2 text-2xl font-extrabold text-zinc-900">{order.external_number}</h1><p className="text-sm text-zinc-500">{order.customer_name}</p></div>
        {canWriteQuotes(role) && <button onClick={createRound} disabled={creating} className="rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50">{creating ? "Criando..." : "Nova rodada"}</button>}
      </header>
      {error && <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      <dl className="grid gap-3 rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm sm:grid-cols-2 lg:grid-cols-4">
        <Info label="Origem" value={`${order.origin_zip} · ${order.origin_uf}`} /><Info label="Destino" value={`${order.destination_zip} · ${order.destination_uf}`} /><Info label="Peso / volumes" value={`${order.weight_kg} kg · ${order.volume_count}`} /><Info label="Valor da mercadoria" value={new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(order.goods_value))} />
      </dl>
      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm"><h2 className="border-b border-zinc-100 px-5 py-4 font-bold text-zinc-900">Histórico de rodadas</h2>{rounds.length === 0 ? <p className="p-6 text-sm text-zinc-500">Nenhuma rodada iniciada.</p> : <ul className="divide-y divide-zinc-100">{rounds.map((round) => <li key={round.id}><Link href={`/quote-rounds/${round.id}`} className="flex items-center justify-between p-5 hover:bg-zinc-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-red-500"><span><strong>Rodada {round.sequence}</strong><span className="ml-2 text-sm text-zinc-500">{round.quotes.length} transportadoras</span></span><span className="rounded-full bg-zinc-100 px-3 py-1 text-xs font-semibold text-zinc-700">{round.status}</span></Link></li>)}</ul>}</div>
    </section>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return <div><dt className="text-xs font-semibold uppercase tracking-wide text-zinc-500">{label}</dt><dd className="mt-1 font-semibold text-zinc-900">{value}</dd></div>;
}
