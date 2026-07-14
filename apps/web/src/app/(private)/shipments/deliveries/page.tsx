"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { listDeliveries } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import type { DeliveryListItem, DeliveryListParams } from "@/lib/types";

export default function DeliveriesPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<DeliveryListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [total, setTotal] = useState(0);
  
  // Filtros
  const [nfFilter, setNfFilter] = useState("");
  const [transportadoraFilter, setTransportadoraFilter] = useState("");
  const [dataColetaFilter, setDataColetaFilter] = useState("");

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      setLoading(true);
      setError("");
      try {
        const params: DeliveryListParams = {
          page,
          page_size: pageSize,
          nf: nfFilter || undefined,
          transportadora: transportadoraFilter || undefined,
          data_coleta: dataColetaFilter || undefined,
        };
        const response = await listDeliveries(session.accessToken, params);
        if (!cancelled) {
          setItems(response.items);
          setTotal(response.total);
        }
      } catch {
        if (!cancelled) setError("Não foi possível carregar entregas.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session, page, pageSize, nfFilter, transportadoraFilter, dataColetaFilter]);

  const onApplyFilters = () => {
    setPage(1);
  };

  const onClearFilters = () => {
    setNfFilter("");
    setTransportadoraFilter("");
    setDataColetaFilter("");
    setPage(1);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR");
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Entregas Importadas</h2>
        <p className="text-sm text-slate-700">Listagem de entregas importadas via CSV/Excel.</p>
      </header>

      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {/* Filtros */}
      <div className="rounded border bg-white p-4 space-y-4">
        <div className="grid gap-4 md:grid-cols-3">
          <div>
            <label className="block text-sm font-medium">Nota Fiscal (NF)</label>
            <input
              value={nfFilter}
              onChange={(e) => setNfFilter(e.target.value)}
              placeholder="Buscar por NF"
              className="mt-1 w-full rounded border px-3 py-2 text-sm"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Transportadora</label>
            <input
              value={transportadoraFilter}
              onChange={(e) => setTransportadoraFilter(e.target.value)}
              placeholder="Buscar por transportadora"
              className="mt-1 w-full rounded border px-3 py-2 text-sm"
              disabled={loading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Data de Coleta</label>
            <input
              type="date"
              value={dataColetaFilter}
              onChange={(e) => setDataColetaFilter(e.target.value)}
              className="mt-1 w-full rounded border px-3 py-2 text-sm"
              disabled={loading}
            />
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={onApplyFilters}
            disabled={loading}
            className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
          >
            Aplicar Filtros
          </button>
          <button
            onClick={onClearFilters}
            disabled={loading}
            className="rounded border px-4 py-2 text-sm disabled:opacity-60"
          >
            Limpar Filtros
          </button>
        </div>
      </div>

      {/* Tabela */}
      <div className="overflow-hidden rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-3 py-2">NF</th>
              <th className="px-3 py-2">Transportadora</th>
              <th className="px-3 py-2">Data Coleta</th>
              <th className="px-3 py-2">Valor Frete</th>
              <th className="px-3 py-2">% Frete</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td className="px-3 py-3 text-slate-700" colSpan={5}>Carregando...</td></tr>
            ) : items.length === 0 ? (
              <tr><td className="px-3 py-3 text-slate-700" colSpan={5}>Nenhuma entrega encontrada.</td></tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-3 py-2">
                    <Link href={`/shipments/deliveries/${item.id}`} className="text-blue-600 hover:underline">
                      {item.nf}
                    </Link>
                  </td>
                  <td className="px-3 py-2">{item.transportadora}</td>
                  <td className="px-3 py-2">{formatDate(item.data_coleta)}</td>
                  <td className="px-3 py-2">{formatCurrency(item.valor_frete)}</td>
                  <td className="px-3 py-2">{item.percentual_frete.toFixed(2)}%</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginação */}
      {total > 0 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-700">
            Total: {total} | Página {page} de {totalPages}
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1 || loading}
              className="rounded border px-3 py-1 text-sm disabled:opacity-60"
            >
              Anterior
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages || loading}
              className="rounded border px-3 py-1 text-sm disabled:opacity-60"
            >
              Próxima
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
