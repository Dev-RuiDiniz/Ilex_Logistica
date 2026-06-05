"use client";

import { useEffect, useState } from "react";

import { getDeliveryDetail } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import type { DeliveryDetail } from "@/lib/types";

export default function DeliveryDetailPage({ params }: { params: { id: string } }) {
  const { session } = useAuth();
  const [item, setItem] = useState<DeliveryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      setLoading(true);
      setError("");
      try {
        const response = await getDeliveryDetail(session.accessToken, parseInt(params.id, 10));
        if (!cancelled) {
          setItem(response);
        }
      } catch {
        if (!cancelled) setError("Não foi possível carregar os detalhes da entrega.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session, params.id]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR");
  };

  if (loading) {
    return <p className="text-sm text-slate-500">Carregando...</p>;
  }

  if (error) {
    return <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>;
  }

  if (!item) {
    return <p className="text-sm text-slate-500">Entrega não encontrada.</p>;
  }

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Detalhe da Entrega</h2>
        <p className="text-sm text-slate-600">Informações detalhadas da entrega.</p>
      </header>

      <div className="rounded border bg-white p-4 space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="block text-sm font-medium">Nota Fiscal (NF)</label>
            <p className="mt-1 text-sm">{item.nf}</p>
          </div>
          <div>
            <label className="block text-sm font-medium">Transportadora</label>
            <p className="mt-1 text-sm">{item.transportadora}</p>
          </div>
          <div>
            <label className="block text-sm font-medium">Data de Coleta</label>
            <p className="mt-1 text-sm">{formatDate(item.data_coleta)}</p>
          </div>
          <div>
            <label className="block text-sm font-medium">Valor Frete</label>
            <p className="mt-1 text-sm">{formatCurrency(item.valor_frete)}</p>
          </div>
          <div>
            <label className="block text-sm font-medium">Percentual Frete</label>
            <p className="mt-1 text-sm">{item.percentual_frete.toFixed(2)}%</p>
          </div>
          <div>
            <label className="block text-sm font-medium">Criado em</label>
            <p className="mt-1 text-sm">{formatDate(item.created_at)}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
