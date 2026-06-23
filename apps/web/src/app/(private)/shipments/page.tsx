"use client";

import { ChangeEvent, useCallback, useEffect, useState } from "react";

import { listShipments } from "@/lib/api";
import { canViewShipments } from "@/lib/permissions";
import { buildGlobalSearchParams, monthYearToDateRange } from "@/lib/shipment-utils";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { Shipment, ShipmentListParams } from "@/lib/types";

export default function ShipmentsPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<Shipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [search, setSearch] = useState("");
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();
  
  // Filtros avançados
  const [statusFilter, setStatusFilter] = useState("");
  const [carrierIdFilter, setCarrierIdFilter] = useState("");
  const [criticalityFilter, setCriticalityFilter] = useState("");
  const [estimatedDeliveryFrom, setEstimatedDeliveryFrom] = useState("");
  const [estimatedDeliveryTo, setEstimatedDeliveryTo] = useState("");
  const [dueDateFrom, setDueDateFrom] = useState("");
  const [dueDateTo, setDueDateTo] = useState("");
  const [collectionDepartureFrom, setCollectionDepartureFrom] = useState("");
  const [collectionDepartureTo, setCollectionDepartureTo] = useState("");
  const [customerNameFilter, setCustomerNameFilter] = useState("");
  const [destinationUfFilter, setDestinationUfFilter] = useState("");
  const [invoiceNumberFilter, setInvoiceNumberFilter] = useState("");
  const [invoiceKeyFilter, setInvoiceKeyFilter] = useState("");
  const [fiscalDocumentFilter, setFiscalDocumentFilter] = useState("");

  // Filtros fiscais/financeiros (BETA-031)
  const [freightValueMin, setFreightValueMin] = useState("");
  const [freightValueMax, setFreightValueMax] = useState("");
  const [invoiceValueMin, setInvoiceValueMin] = useState("");
  const [invoiceValueMax, setInvoiceValueMax] = useState("");
  const [freightPercentageMin, setFreightPercentageMin] = useState("");
  const [freightPercentageMax, setFreightPercentageMax] = useState("");
  const [amountMin, setAmountMin] = useState("");
  const [amountMax, setAmountMax] = useState("");

  // Filtros SLA (BETA-1.2)
  const [slaStatusFilter, setSlaStatusFilter] = useState("");
  const [isLateFilter, setIsLateFilter] = useState("");

  // Filtro temporal por mês/ano
  const [useMonthYearFilter, setUseMonthYearFilter] = useState(false);
  const [monthYearTarget, setMonthYearTarget] = useState<"estimated_delivery" | "due_date">("estimated_delivery");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [selectedYear, setSelectedYear] = useState("");
  
  // Ordenação
  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const canView = canViewShipments(session?.role ?? "auditoria");

  const load = useCallback(async () => {
    if (!session || !canView) return;
    setLoading(true);
    setError("");
    try {
      // Use global search parameter for broader search capability
      const searchParams = buildGlobalSearchParams(search);
      
      // Aplicar filtro temporal por mês/ano se ativado
      let temporalFilter: { estimated_delivery_from?: string; estimated_delivery_to?: string; due_date_from?: string; due_date_to?: string } = {};
      if (useMonthYearFilter && selectedMonth && selectedYear) {
        const month = parseInt(selectedMonth, 10);
        const year = parseInt(selectedYear, 10);
        const dateRange = monthYearToDateRange(month, year);
        if (monthYearTarget === "estimated_delivery") {
          temporalFilter = {
            estimated_delivery_from: dateRange.from,
            estimated_delivery_to: dateRange.to,
          };
        } else {
          temporalFilter = {
            due_date_from: dateRange.from,
            due_date_to: dateRange.to,
          };
        }
      }
      
      const params: ShipmentListParams = {
        page,
        page_size: pageSize,
        ...searchParams,
        status: statusFilter || undefined,
        carrier_id: carrierIdFilter ? parseInt(carrierIdFilter, 10) : undefined,
        criticality: criticalityFilter || undefined,
        estimated_delivery_from: estimatedDeliveryFrom || temporalFilter.estimated_delivery_from || undefined,
        estimated_delivery_to: estimatedDeliveryTo || temporalFilter.estimated_delivery_to || undefined,
        due_date_from: dueDateFrom || temporalFilter.due_date_from || undefined,
        due_date_to: dueDateTo || temporalFilter.due_date_to || undefined,
        collection_departure_from: collectionDepartureFrom || undefined,
        collection_departure_to: collectionDepartureTo || undefined,
        customer_name: customerNameFilter || undefined,
        destination_uf: destinationUfFilter || undefined,
        invoice_number: invoiceNumberFilter || undefined,
        invoice_key: invoiceKeyFilter || undefined,
        fiscal_document: fiscalDocumentFilter || undefined,
        // Filtros fiscais/financeiros (BETA-031)
        freight_value_min: freightValueMin ? parseFloat(freightValueMin) : undefined,
        freight_value_max: freightValueMax ? parseFloat(freightValueMax) : undefined,
        invoice_value_min: invoiceValueMin ? parseFloat(invoiceValueMin) : undefined,
        invoice_value_max: invoiceValueMax ? parseFloat(invoiceValueMax) : undefined,
        freight_percentage_min: freightPercentageMin ? parseFloat(freightPercentageMin) : undefined,
        freight_percentage_max: freightPercentageMax ? parseFloat(freightPercentageMax) : undefined,
        amount_min: amountMin ? parseFloat(amountMin) : undefined,
        amount_max: amountMax ? parseFloat(amountMax) : undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
        // Filtros SLA (BETA-1.2)
        sla_status: slaStatusFilter || undefined,
        is_late: isLateFilter === "" ? undefined : isLateFilter === "true",
      };
      const response = await listShipments(session.accessToken, params);
      setItems(response.items);
      setTotal(response.total);
      setTotalPages(response.total_pages);
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar envios"));
      setError(err instanceof Error ? err.message : "Erro ao carregar envios");
    } finally {
      setLoading(false);
    }
  }, [
    canView,
    carrierIdFilter,
    criticalityFilter,
    dueDateFrom,
    dueDateTo,
    estimatedDeliveryFrom,
    estimatedDeliveryTo,
    collectionDepartureFrom,
    collectionDepartureTo,
    page,
    pageSize,
    search,
    selectedMonth,
    selectedYear,
    session,
    sortBy,
    sortOrder,
    statusFilter,
    useMonthYearFilter,
    monthYearTarget,
    customerNameFilter,
    destinationUfFilter,
    invoiceNumberFilter,
    invoiceKeyFilter,
    fiscalDocumentFilter,
    freightValueMin,
    freightValueMax,
    invoiceValueMin,
    invoiceValueMax,
    freightPercentageMin,
    freightPercentageMax,
    amountMin,
    amountMax,
    slaStatusFilter,
    isLateFilter,
  ]);

  useEffect(() => {
    const timer = setTimeout(() => {
      void load();
    }, 0);
    return () => clearTimeout(timer);
  }, [load]);

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

  const getCriticalityBadge = (criticality: string) => {
    const badges: Record<string, { color: string; label: string }> = {
      normal: { color: "bg-green-100 text-green-800", label: "Normal" },
      baixa: { color: "bg-yellow-100 text-yellow-800", label: "Baixa" },
      media: { color: "bg-orange-100 text-orange-800", label: "Média" },
      alta: { color: "bg-red-100 text-red-800", label: "Alta" },
    };
    const badge = badges[criticality] || { color: "bg-gray-100 text-gray-800", label: criticality };
    return (
      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${badge.color}`}>
        {badge.label}
      </span>
    );
  };

  const onSearch = (event: ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  const onSearchSubmit = () => {
    setPage(1);
    void load();
  };

  const onApplyFilters = () => {
    setPage(1);
    void load();
  };

  const onClearFilters = () => {
    setSearch("");
    setStatusFilter("");
    setCarrierIdFilter("");
    setCriticalityFilter("");
    setEstimatedDeliveryFrom("");
    setEstimatedDeliveryTo("");
    setDueDateFrom("");
    setDueDateTo("");
    setCollectionDepartureFrom("");
    setCollectionDepartureTo("");
    setCustomerNameFilter("");
    setDestinationUfFilter("");
    setInvoiceNumberFilter("");
    setInvoiceKeyFilter("");
    setFiscalDocumentFilter("");
    setFreightValueMin("");
    setFreightValueMax("");
    setInvoiceValueMin("");
    setInvoiceValueMax("");
    setFreightPercentageMin("");
    setFreightPercentageMax("");
    setAmountMin("");
    setAmountMax("");
    setSlaStatusFilter("");
    setIsLateFilter("");
    setUseMonthYearFilter(false);
    setMonthYearTarget("estimated_delivery");
    setSelectedMonth("");
    setSelectedYear("");
    setSortBy("created_at");
    setSortOrder("desc");
    setPage(1);
    void load();
  };

  const toggleSortOrder = () => {
    setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));
  };

  return (
    <section className="space-y-4">
      <header className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-semibold">Envios</h2>
          <p className="text-sm text-slate-600">Listagem de envios com filtros, busca e ordenação.</p>
        </div>
      </header>

      {!canView && <p className="rounded bg-amber-50 px-3 py-2 text-sm text-amber-700">Perfil sem permissão para visualizar envios.</p>}

      {/* Filtros e busca */}
      <div className="rounded border bg-white p-4 space-y-4">
        <div className="flex flex-col gap-2 md:flex-row md:items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium">Buscar</label>
            <input
              value={search}
              onChange={onSearch}
              placeholder="Buscar por tracking, NF, cliente, etc."
              className="mt-1 w-full rounded border px-3 py-2 text-sm"
              disabled={loading}
            />
          </div>
          <button
            onClick={onSearchSubmit}
            disabled={loading}
            className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
          >
            Buscar
          </button>
        </div>

        {/* Filtro temporal por mês/ano */}
        <div className="border-t pt-4">
          <div className="flex items-center gap-2 mb-2">
            <input
              type="checkbox"
              id="useMonthYearFilter"
              checked={useMonthYearFilter}
              onChange={(e) => setUseMonthYearFilter(e.target.checked)}
              disabled={loading}
              className="rounded"
            />
            <label htmlFor="useMonthYearFilter" className="text-sm font-medium">Filtro por mês/ano</label>
          </div>
          {useMonthYearFilter && (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div>
                <label className="block text-sm font-medium">Aplicar em</label>
                <select
                  value={monthYearTarget}
                  onChange={(e) => setMonthYearTarget(e.target.value as "estimated_delivery" | "due_date")}
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={loading}
                >
                  <option value="estimated_delivery">Entrega estimada</option>
                  <option value="due_date">Vencimento</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium">Mês</label>
                <select
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={loading}
                >
                  <option value="">Selecione</option>
                  <option value="1">Janeiro</option>
                  <option value="2">Fevereiro</option>
                  <option value="3">Março</option>
                  <option value="4">Abril</option>
                  <option value="5">Maio</option>
                  <option value="6">Junho</option>
                  <option value="7">Julho</option>
                  <option value="8">Agosto</option>
                  <option value="9">Setembro</option>
                  <option value="10">Outubro</option>
                  <option value="11">Novembro</option>
                  <option value="12">Dezembro</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium">Ano</label>
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(e.target.value)}
                  className="mt-1 w-full rounded border px-3 py-2 text-sm"
                  disabled={loading}
                >
                  <option value="">Selecione</option>
                  <option value="2024">2024</option>
                  <option value="2025">2025</option>
                  <option value="2026">2026</option>
                  <option value="2027">2027</option>
                  <option value="2028">2028</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Filtros avançados manuais */}
        <div className="border-t pt-4">
          <h4 className="text-sm font-semibold mb-2">Filtros manuais</h4>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div>
              <label className="block text-sm font-medium">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              >
                <option value="">Todos</option>
                <option value="pending">Pendente</option>
                <option value="in_transit">Em trânsito</option>
                <option value="delivered">Entregue</option>
                <option value="failed">Falhou</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium">Carrier ID</label>
              <input
                type="number"
                value={carrierIdFilter}
                onChange={(e) => setCarrierIdFilter(e.target.value)}
                placeholder="ID da transportadora"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Criticidade</label>
              <select
                value={criticalityFilter}
                onChange={(e) => setCriticalityFilter(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              >
                <option value="">Todas</option>
                <option value="normal">Normal</option>
                <option value="baixa">Baixa</option>
                <option value="media">Média</option>
                <option value="alta">Alta</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium">SLA Status</label>
              <select
                value={slaStatusFilter}
                onChange={(e) => setSlaStatusFilter(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              >
                <option value="">Todos</option>
                <option value="critical">Crítico</option>
                <option value="warning">Warning</option>
                <option value="normal">Normal</option>
                <option value="unknown">Desconhecido</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium">Atrasado?</label>
              <select
                value={isLateFilter}
                onChange={(e) => setIsLateFilter(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              >
                <option value="">Todos</option>
                <option value="true">Sim</option>
                <option value="false">Não</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium">Cliente</label>
              <input
                type="text"
                value={customerNameFilter}
                onChange={(e) => setCustomerNameFilter(e.target.value)}
                placeholder="Nome do cliente"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">UF Destino</label>
              <input
                type="text"
                value={destinationUfFilter}
                onChange={(e) => setDestinationUfFilter(e.target.value)}
                placeholder="UF (ex: SP)"
                maxLength={2}
                className="mt-1 w-full rounded border px-3 py-2 text-sm uppercase"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Entrega estimada (de)</label>
              <input
                type="date"
                value={estimatedDeliveryFrom}
                onChange={(e) => setEstimatedDeliveryFrom(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Entrega estimada (até)</label>
              <input
                type="date"
                value={estimatedDeliveryTo}
                onChange={(e) => setEstimatedDeliveryTo(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Vencimento (de)</label>
              <input
                type="date"
                value={dueDateFrom}
                onChange={(e) => setDueDateFrom(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Vencimento (até)</label>
              <input
                type="date"
                value={dueDateTo}
                onChange={(e) => setDueDateTo(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Coleta/Saída (de)</label>
              <input
                type="date"
                value={collectionDepartureFrom}
                onChange={(e) => setCollectionDepartureFrom(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Coleta/Saída (até)</label>
              <input
                type="date"
                value={collectionDepartureTo}
                onChange={(e) => setCollectionDepartureTo(e.target.value)}
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Número NF</label>
              <input
                type="text"
                value={invoiceNumberFilter}
                onChange={(e) => setInvoiceNumberFilter(e.target.value)}
                placeholder="Número da NF"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Chave NF-e</label>
              <input
                type="text"
                value={invoiceKeyFilter}
                onChange={(e) => setInvoiceKeyFilter(e.target.value)}
                placeholder="Chave de acesso NF-e"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Documento Fiscal</label>
              <input
                type="text"
                value={fiscalDocumentFilter}
                onChange={(e) => setFiscalDocumentFilter(e.target.value)}
                placeholder="Documento fiscal"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor Frete Mín.</label>
              <input
                type="number"
                step="0.01"
                value={freightValueMin}
                onChange={(e) => setFreightValueMin(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor Frete Máx.</label>
              <input
                type="number"
                step="0.01"
                value={freightValueMax}
                onChange={(e) => setFreightValueMax(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor NF Mín.</label>
              <input
                type="number"
                step="0.01"
                value={invoiceValueMin}
                onChange={(e) => setInvoiceValueMin(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor NF Máx.</label>
              <input
                type="number"
                step="0.01"
                value={invoiceValueMax}
                onChange={(e) => setInvoiceValueMax(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">% Frete Mín.</label>
              <input
                type="number"
                step="0.01"
                value={freightPercentageMin}
                onChange={(e) => setFreightPercentageMin(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">% Frete Máx.</label>
              <input
                type="number"
                step="0.01"
                value={freightPercentageMax}
                onChange={(e) => setFreightPercentageMax(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor Total Mín.</label>
              <input
                type="number"
                step="0.01"
                value={amountMin}
                onChange={(e) => setAmountMin(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Valor Total Máx.</label>
              <input
                type="number"
                step="0.01"
                value={amountMax}
                onChange={(e) => setAmountMax(e.target.value)}
                placeholder="0.00"
                className="mt-1 w-full rounded border px-3 py-2 text-sm"
                disabled={loading}
              />
            </div>
          </div>
        </div>

        {/* Ordenação */}
        <div className="flex flex-col gap-2 md:flex-row md:items-center border-t pt-4">
          <div className="flex-1">
            <label className="block text-sm font-medium">Ordenar por</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="mt-1 w-full rounded border px-3 py-2 text-sm"
              disabled={loading}
            >
              <option value="created_at">Data de criação</option>
              <option value="estimated_delivery">Entrega estimada</option>
              <option value="due_date">Vencimento</option>
              <option value="amount">Valor</option>
              <option value="criticality">Criticidade</option>
            </select>
          </div>
          <button
            onClick={toggleSortOrder}
            disabled={loading}
            className="rounded border px-4 py-2 text-sm disabled:opacity-60"
          >
            {sortOrder === "asc" ? "Ascendente" : "Descendente"}
          </button>
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

      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {/* Tabela */}
      <div className="overflow-x-auto rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
            <tr>
              <th className="px-3 py-2">Tracking</th>
              <th className="px-3 py-2">NF</th>
              <th className="px-3 py-2">Cliente</th>
              <th className="px-3 py-2">UF</th>
              <th className="px-3 py-2">Data Coleta/Saída</th>
              <th className="px-3 py-2">Valor NF</th>
              <th className="px-3 py-2">Valor Frete</th>
              <th className="px-3 py-2">% Frete</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Entrega Estimada</th>
              <th className="px-3 py-2">Vencimento</th>
              <th className="px-3 py-2">Atraso (dias)</th>
              <th className="px-3 py-2">Criticidade</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={13} className="px-3 py-3 text-slate-500">
                  Carregando...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={13} className="px-3 py-3 text-slate-500">
                  Nenhum envio encontrado.
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-t">
                  <td className="px-3 py-2">
                    <a href={`/shipments/${item.id}`} className="text-blue-700 hover:underline">
                      {item.tracking_code}
                    </a>
                  </td>
                  <td className="px-3 py-2">{formatUnavailable(item.invoice_number)}</td>
                  <td className="px-3 py-2">{formatUnavailable(item.customer_name)}</td>
                  <td className="px-3 py-2">{formatUnavailable(item.destination_uf)}</td>
                  <td className="px-3 py-2">{formatDateBR(item.collection_departure_date)}</td>
                  <td className="px-3 py-2">{formatCurrencyBRL(item.invoice_value)}</td>
                  <td className="px-3 py-2">{formatCurrencyBRL(item.freight_value)}</td>
                  <td className="px-3 py-2">{formatPercentage(item.freight_percentage)}</td>
                  <td className="px-3 py-2">{item.status}</td>
                  <td className="px-3 py-2">{formatDateBR(item.estimated_delivery)}</td>
                  <td className="px-3 py-2">{formatDateBR(item.due_date)}</td>
                  <td className="px-3 py-2">{item.delay_days}</td>
                  <td className="px-3 py-2">{getCriticalityBadge(item.criticality)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Paginação */}
      {!loading && totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-600">
            Página {page} de {totalPages} ({total} registros)
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="rounded border px-3 py-1 text-sm disabled:opacity-60"
            >
              Anterior
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="rounded border px-3 py-1 text-sm disabled:opacity-60"
            >
              Próxima
            </button>
          </div>
        </div>
      )}

      {/* Limitação documentada */}
      <p className="text-xs text-slate-500">
        Esta listagem é limitada a 20 registros por página. Use os filtros para refinar sua busca.
      </p>
    </section>
  );
}
