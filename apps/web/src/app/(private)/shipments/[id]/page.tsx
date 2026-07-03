"use client";

import { FormEvent, use, useEffect, useState } from "react";

import { createShipmentTreatment, getShipmentDetail, listShipmentTreatments } from "@/lib/api";
import { canEditShipments } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";
import type { ShipmentDetail, ShipmentTreatment } from "@/lib/types";

export default function ShipmentDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { session } = useAuth();
  const [detail, setDetail] = useState<ShipmentDetail | null>(null);
  const [treatments, setTreatments] = useState<ShipmentTreatment[]>([]);
  const [status, setStatus] = useState("em_tratativa");
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(true);
  const { id } = use(params);
  const shipmentId = Number(id);
  const editable = canEditShipments(session?.role ?? "auditoria");

  // Formatting helpers
  const formatCurrencyBRL = (value: number | null) => {
    if (value === null || value === undefined) return "-";
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const formatPercentage = (value: number | null) => {
    if (value === null || value === undefined) return "-";
    return `${value.toFixed(2)}%`;
  };

  const formatDateBR = (dateString: string | null) => {
    if (!dateString) return "-";
    return new Date(dateString).toLocaleDateString("pt-BR");
  };

  const formatUnavailable = (value: string | number | null) => {
    if (value === null || value === undefined || value === "") return "-";
    return value;
  };

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session || Number.isNaN(shipmentId)) return;
      setLoading(true);
      setError("");
      try {
        const [shipment, timeline] = await Promise.all([
          getShipmentDetail(session.accessToken, shipmentId),
          listShipmentTreatments(session.accessToken, shipmentId),
        ]);
        if (!cancelled) {
          setDetail(shipment);
          setTreatments(timeline);
        }
      } catch {
        if (!cancelled) setError("Falha ao carregar detalhe da entrega.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session, shipmentId]);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!session || !editable) return;
    if (!comment.trim()) {
      setError("Comentário obrigatório.");
      return;
    }
    try {
      setError("");
      setSuccess("");
      await createShipmentTreatment(session.accessToken, shipmentId, { status, comment });
      setComment("");
      // Reload data after creating treatment
      if (session) {
        const [shipment, timeline] = await Promise.all([
          getShipmentDetail(session.accessToken, shipmentId),
          listShipmentTreatments(session.accessToken, shipmentId),
        ]);
        setDetail(shipment);
        setTreatments(timeline);
        setSuccess("Tratativa registrada com sucesso.");
      }
    } catch {
      setError("Falha ao registrar tratativa.");
    }
  };

  if (loading) return <p>Carregando...</p>;
  if (!detail) return <p>Entrega não encontrada.</p>;

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Detalhe da Entrega</h2>
        <p className="text-sm text-slate-600">{detail.tracking_code}</p>
      </header>
      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      {success && <p className="rounded bg-emerald-50 px-3 py-2 text-sm text-emerald-700">{success}</p>}
      
      {/* Informações Básicas */}
      <div className="grid gap-3 rounded border p-4 md:grid-cols-2">
        <div><strong>Status:</strong> {detail.status}</div>
        <div><strong>Criticidade:</strong> {detail.criticality}</div>
        <div><strong>Atraso:</strong> {detail.delay_days} dias</div>
        <div><strong>Carrier ID:</strong> {detail.carrier_id}</div>
        <div className="md:col-span-2"><strong>Origem:</strong> {detail.origin_address}</div>
        <div className="md:col-span-2"><strong>Destino:</strong> {detail.destination_address}</div>
      </div>

      {/* Informações Fiscais/Financeiras */}
      <div className="grid gap-3 rounded border p-4 md:grid-cols-2">
        <div><strong>NF:</strong> {formatUnavailable(detail.invoice_number)}</div>
        <div><strong>Documento Fiscal:</strong> {formatUnavailable(detail.fiscal_document)}</div>
        <div><strong>Cliente:</strong> {formatUnavailable(detail.customer_name)}</div>
        <div><strong>Destinatário:</strong> {formatUnavailable(detail.recipient_name)}</div>
        <div><strong>UF Destino:</strong> {formatUnavailable(detail.destination_uf)}</div>
        <div><strong>Data Coleta/Saída:</strong> {formatDateBR(detail.collection_departure_date)}</div>
        <div><strong>Valor NF:</strong> {formatCurrencyBRL(detail.invoice_value)}</div>
        <div><strong>Valor Frete:</strong> {formatCurrencyBRL(detail.freight_value)}</div>
        <div><strong>% Frete:</strong> {formatPercentage(detail.freight_percentage)}</div>
        <div><strong>Valor (Legado):</strong> {formatCurrencyBRL(detail.amount)}</div>
        <div><strong>Entrega Estimada:</strong> {formatDateBR(detail.estimated_delivery)}</div>
        <div><strong>Entrega Real:</strong> {formatDateBR(detail.actual_delivery)}</div>
        <div><strong>Vencimento:</strong> {formatDateBR(detail.due_date)}</div>
      </div>

      <section className="space-y-3 rounded border p-4">
        <h3 className="text-base font-semibold">Tratativas</h3>
        {editable && (
          <form onSubmit={onSubmit} className="grid gap-2 md:grid-cols-[180px_1fr_auto]">
            <label htmlFor="treatment-status" className="sr-only">Status</label>
            <select id="treatment-status" value={status} onChange={(e) => setStatus(e.target.value)} className="rounded border px-3 py-2 text-sm">
              <option value="em_tratativa">Em tratativa</option>
              <option value="resolvido">Resolvido</option>
              <option value="escalado">Escalado</option>
            </select>
            <label htmlFor="treatment-comment" className="sr-only">Comentário</label>
            <input id="treatment-comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Descreva a ação realizada"
              className="rounded border px-3 py-2 text-sm"
            />
            <button className="rounded bg-slate-900 px-4 py-2 text-sm text-white" type="submit">Registrar</button>
          </form>
        )}
        <ul className="space-y-2">
          {treatments.length === 0 && <li className="text-sm text-slate-500">Sem tratativas registradas.</li>}
          {treatments.map((item) => (
            <li key={item.id} data-testid="treatment-item" className="rounded border px-3 py-2 text-sm">
              <div className="font-medium">{item.status}</div>
              <div>{item.comment}</div>
            </li>
          ))}
        </ul>
      </section>
    </section>
  );
}
