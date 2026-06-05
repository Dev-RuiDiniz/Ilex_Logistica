"use client";

import { useEffect, useState } from "react";

import { getDeliveryDetail, listCarriers, promoteDeliveryToShipment } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import type { Carrier, DeliveryDetail, PromoteDeliveryRequest } from "@/lib/types";

export default function DeliveryDetailPage({ params }: { params: { id: string } }) {
  const { session } = useAuth();
  const [item, setItem] = useState<DeliveryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Estados do formulário de promoção
  const [showPromoteForm, setShowPromoteForm] = useState(false);
  const [promoteLoading, setPromoteLoading] = useState(false);
  const [promoteError, setPromoteError] = useState("");
  const [promoteSuccess, setPromoteSuccess] = useState(false);
  const [shipmentCreated, setShipmentCreated] = useState<{ id: number; tracking_code: string; status: string } | null>(null);
  const [carriers, setCarriers] = useState<Carrier[]>([]);
  const [carriersLoading, setCarriersLoading] = useState(false);
  const [carriersError, setCarriersError] = useState("");
  
  // Campos do formulário
  const [trackingCode, setTrackingCode] = useState("");
  const [carrierId, setCarrierId] = useState("");
  const [estimatedDelivery, setEstimatedDelivery] = useState("");
  const [recipientName, setRecipientName] = useState("");
  const [recipientPhone, setRecipientPhone] = useState("");
  const [originAddress, setOriginAddress] = useState("");
  const [destinationAddress, setDestinationAddress] = useState("");
  const [shipmentStatus, setShipmentStatus] = useState("pending");

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

  // Carregar carriers quando o formulário é aberto
  useEffect(() => {
    if (!showPromoteForm || !session) return;
    const loadCarriers = async () => {
      setCarriersLoading(true);
      setCarriersError("");
      try {
        const data = await listCarriers(session.accessToken);
        setCarriers(data);
      } catch {
        setCarriersError("Não foi possível carregar transportadoras.");
      } finally {
        setCarriersLoading(false);
      }
    };
    void loadCarriers();
  }, [showPromoteForm, session]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR");
  };

  const handlePromote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session || !item) return;

    setPromoteLoading(true);
    setPromoteError("");
    setPromoteSuccess(false);
    setShipmentCreated(null);

    try {
      const payload: PromoteDeliveryRequest = {
        tracking_code: trackingCode,
        carrier_id: parseInt(carrierId, 10),
        estimated_delivery: estimatedDelivery,
        recipient_name: recipientName,
        recipient_phone: recipientPhone,
        origin_address: originAddress,
        destination_address: destinationAddress,
        shipment_status: shipmentStatus || undefined,
      };

      const response = await promoteDeliveryToShipment(session.accessToken, item.id, payload);
      setPromoteSuccess(true);
      setShipmentCreated({
        id: response.id,
        tracking_code: response.tracking_code,
        status: response.status,
      });
      // Limpar formulário
      setTrackingCode("");
      setCarrierId("");
      setEstimatedDelivery("");
      setRecipientName("");
      setRecipientPhone("");
      setOriginAddress("");
      setDestinationAddress("");
      setShipmentStatus("pending");
    } catch {
      setPromoteError("Não foi possível promover a entrega para Shipment.");
    } finally {
      setPromoteLoading(false);
    }
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

      {/* Seção de Promoção para Shipment */}
      <div className="rounded border bg-white p-4 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Promover para Shipment</h3>
          <button
            onClick={() => setShowPromoteForm(!showPromoteForm)}
            className="rounded border px-3 py-1 text-sm"
          >
            {showPromoteForm ? "Cancelar" : "Promover"}
          </button>
        </div>

        {showPromoteForm && (
          <form onSubmit={handlePromote} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium">Tracking Code *</label>
                <input
                  type="text"
                  value={trackingCode}
                  onChange={(e) => setTrackingCode(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Transportadora *</label>
                {carriersLoading ? (
                  <p className="mt-1 text-sm text-slate-500">Carregando transportadoras...</p>
                ) : carriersError ? (
                  <p className="mt-1 text-sm text-red-700">{carriersError}</p>
                ) : (
                  <select
                    value={carrierId}
                    onChange={(e) => setCarrierId(e.target.value)}
                    required
                    className="mt-1 w-full rounded border px-3 py-2 text-sm"
                    disabled={promoteLoading}
                  >
                    <option value="">Selecione uma transportadora</option>
                    {carriers.map((carrier) => (
                      <option key={carrier.id} value={carrier.id.toString()}>
                        {carrier.name}
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium">Data Estimada de Entrega *</label>
                <input
                  type="datetime-local"
                  value={estimatedDelivery}
                  onChange={(e) => setEstimatedDelivery(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Nome do Destinatário *</label>
                <input
                  type="text"
                  value={recipientName}
                  onChange={(e) => setRecipientName(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Telefone do Destinatário *</label>
                <input
                  type="text"
                  value={recipientPhone}
                  onChange={(e) => setRecipientPhone(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Endereço de Origem *</label>
                <input
                  type="text"
                  value={originAddress}
                  onChange={(e) => setOriginAddress(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Endereço de Destino *</label>
                <input
                  type="text"
                  value={destinationAddress}
                  onChange={(e) => setDestinationAddress(e.target.value)}
                  required
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Status do Shipment</label>
                <input
                  type="text"
                  value={shipmentStatus}
                  onChange={(e) => setShipmentStatus(e.target.value)}
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={promoteLoading}
                />
              </div>
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={promoteLoading}
                className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
              >
                {promoteLoading ? "Promovendo..." : "Promover"}
              </button>
              <button
                type="button"
                onClick={() => setShowPromoteForm(false)}
                disabled={promoteLoading}
                className="rounded border px-4 py-2 text-sm disabled:opacity-60"
              >
                Cancelar
              </button>
            </div>

            {promoteError && (
              <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{promoteError}</p>
            )}

            {promoteSuccess && shipmentCreated && (
              <div className="rounded bg-green-50 px-3 py-2 text-sm text-green-700">
                <p className="font-semibold">Shipment criado com sucesso!</p>
                <p>ID: {shipmentCreated.id}</p>
                <p>Tracking Code: {shipmentCreated.tracking_code}</p>
                <p>Status: {shipmentCreated.status}</p>
              </div>
            )}
          </form>
        )}
      </div>
    </section>
  );
}
