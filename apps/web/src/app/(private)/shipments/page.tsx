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

  // Filtros fiscais/financeiros (BETA-031) e SLA (BETA-1.2)
  const [invoiceNumberFilter, setInvoiceNumberFilter] = useState("");
  const [invoiceKeyFilter, setInvoiceKeyFilter] = useState("");
  const [fiscalDocumentFilter, setFiscalDocumentFilter] = useState("");
  const [freightValueMin, setFreightValueMin] = useState("");
  const [freightValueMax, setFreightValueMax] = useState("");
  const [invoiceValueMin, setInvoiceValueMin] = useState("");
  const [invoiceValueMax, setInvoiceValueMax] = useState("");
  const [freightPercentageMin, setFreightPercentageMin] = useState("");
  const [freightPercentageMax, setFreightPercentageMax] = useState("");
  const [amountMin, setAmountMin] = useState("");
  const [amountMax, setAmountMax] = useState("");
  const [slaStatusFilter, setSlaStatusFilter] = useState("");
  const [isLateFilter, setIsLateFilter] = useState("");

  const [useMonthYearFilter, setUseMonthYearFilter] = useState(false);
  const [monthYearTarget, setMonthYearTarget] = useState<"estimated_delivery" | "due_date">("estimated_delivery");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [selectedYear, setSelectedYear] = useState("");

  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const canView = canViewShipments(session?.role ?? "auditoria");

  const load = useCallback(async () => {
    if (!session || !canView) return;
    setLoading(true);
    setError("");
    try {
      const searchParams = buildGlobalSearchParams(search);
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
    canView, carrierIdFilter, criticalityFilter, dueDateFrom, dueDateTo,
    estimatedDeliveryFrom, estimatedDeliveryTo, page, pageSize, search,
    selectedMonth, selectedYear, session, sortBy, sortOrder, statusFilter,
    useMonthYearFilter, monthYearTarget, customerNameFilter, destinationUfFilter,
    invoiceNumberFilter, invoiceKeyFilter, fiscalDocumentFilter,
    freightValueMin, freightValueMax, invoiceValueMin, invoiceValueMax,
    freightPercentageMin, freightPercentageMax, amountMin, amountMax,
    slaStatusFilter, isLateFilter,
  ]);

  useEffect(() => {
    const timer = setTimeout(() => { void load(); }, 0);
    return () => clearTimeout(timer);
  }, [load]);

  const formatCurrencyBRL = (value: number | null) => {
    if (value === null || value === undefined) return "-";
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
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
      normal: { color: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20", label: "Normal" },
      baixa: { color: "bg-yellow-50 text-yellow-700 ring-1 ring-yellow-600/20", label: "Baixa" },
      media: { color: "bg-orange-50 text-orange-700 ring-1 ring-orange-600/20", label: "Média" },
      alta: { color: "bg-red-50 text-red-700 ring-1 ring-red-600/20", label: "Alta" },
    };
    const badge = badges[criticality] || { color: "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20", label: criticality };
    return (
      <span className={`inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold ${badge.color}`}>
        {badge.label}
      </span>
    );
  };

  const getStatusBadge = (status: string) => {
    const map: Record<string, string> = {
      pending: "bg-zinc-100 text-zinc-700 ring-1 ring-zinc-500/20",
      in_transit: "bg-blue-50 text-blue-700 ring-1 ring-blue-600/20",
      delivered: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20",
      failed: "bg-red-50 text-red-700 ring-1 ring-red-600/20",
    };
    const cls = map[status] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20";
    return (
      <span className={`inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold capitalize ${cls}`}>
        {status.replace("_", " ")}
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

  const inputClass = "mt-1.5 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const selectClass = "mt-1.5 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800 disabled:opacity-50";
  const btnSecondary = "rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50 disabled:opacity-50";

  return (
    <section className="space-y-5">
      {/* Header */}
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Envios</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Listagem com filtros avançados e ordenação</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-zinc-500">
          <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
          {total} registros encontrados
        </div>
      </header>

      {!canView && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-700">
          Perfil sem permissão para visualizar envios.
        </div>
      )}

      {/* Filters Card */}
      <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
        {/* Search + Month/Year */}
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Buscar</label>
            <div className="mt-1.5 flex gap-2">
              <input
                value={search}
                onChange={onSearch}
                placeholder="Tracking, NF, cliente..."
                className="flex-1 rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-zinc-900 placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50"
                disabled={loading}
                onKeyDown={(e) => e.key === "Enter" && onSearchSubmit()}
              />
              <button onClick={onSearchSubmit} disabled={loading} className={btnPrimary}>
                Buscar
              </button>
            </div>
          </div>

          {/* Month/Year Filter */}
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Filtro por Mês/Ano</label>
            <div className="mt-1.5 flex items-center gap-2">
              <input
                type="checkbox"
                id="useMonthYearFilter"
                checked={useMonthYearFilter}
                onChange={(e) => setUseMonthYearFilter(e.target.checked)}
                disabled={loading}
                className="h-4 w-4 rounded border-zinc-300 text-red-600 focus:ring-red-500"
              />
              <label htmlFor="useMonthYearFilter" className="text-sm font-medium text-zinc-700">Ativar filtro temporal</label>
            </div>
            {useMonthYearFilter && (
              <div className="mt-3 grid grid-cols-3 gap-2">
                <select value={monthYearTarget} onChange={(e) => setMonthYearTarget(e.target.value as "estimated_delivery" | "due_date")} className={selectClass} disabled={loading}>
                  <option value="estimated_delivery">Entrega estimada</option>
                  <option value="due_date">Vencimento</option>
                </select>
                <select value={selectedMonth} onChange={(e) => setSelectedMonth(e.target.value)} className={selectClass} disabled={loading}>
                  <option value="">Mês</option>
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
                <select value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)} className={selectClass} disabled={loading}>
                  <option value="">Ano</option>
                  <option value="2024">2024</option>
                  <option value="2025">2025</option>
                  <option value="2026">2026</option>
                  <option value="2027">2027</option>
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Advanced Filters */}
        <div className="mt-5 border-t border-zinc-100 pt-5">
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Filtros Avançados</p>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Status</label>
              <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className={selectClass} disabled={loading}>
                <option value="">Todos</option>
                <option value="pending">Pendente</option>
                <option value="in_transit">Em trânsito</option>
                <option value="delivered">Entregue</option>
                <option value="failed">Falhou</option>
              </select>
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Carrier ID</label>
              <input type="number" value={carrierIdFilter} onChange={(e) => setCarrierIdFilter(e.target.value)} placeholder="ID" className={inputClass} disabled={loading} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Criticidade</label>
              <select value={criticalityFilter} onChange={(e) => setCriticalityFilter(e.target.value)} className={selectClass} disabled={loading}>
                <option value="">Todas</option>
                <option value="normal">Normal</option>
                <option value="baixa">Baixa</option>
                <option value="media">Média</option>
                <option value="alta">Alta</option>
              </select>
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">UF Destino</label>
              <input type="text" value={destinationUfFilter} onChange={(e) => setDestinationUfFilter(e.target.value)} placeholder="UF" maxLength={2} className={`${inputClass} uppercase`} disabled={loading} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Cliente</label>
              <input type="text" value={customerNameFilter} onChange={(e) => setCustomerNameFilter(e.target.value)} placeholder="Nome do cliente" className={inputClass} disabled={loading} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Entrega (de)</label>
              <input type="date" value={estimatedDeliveryFrom} onChange={(e) => setEstimatedDeliveryFrom(e.target.value)} className={inputClass} disabled={loading || useMonthYearFilter} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Entrega (até)</label>
              <input type="date" value={estimatedDeliveryTo} onChange={(e) => setEstimatedDeliveryTo(e.target.value)} className={inputClass} disabled={loading || useMonthYearFilter} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Vencimento (de)</label>
              <input type="date" value={dueDateFrom} onChange={(e) => setDueDateFrom(e.target.value)} className={inputClass} disabled={loading || useMonthYearFilter} />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-zinc-500">Vencimento (até)</label>
              <input type="date" value={dueDateTo} onChange={(e) => setDueDateTo(e.target.value)} className={inputClass} disabled={loading || useMonthYearFilter} />
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

        {/* Sort + Actions */}
        <div className="mt-5 flex flex-col gap-3 border-t border-zinc-100 pt-5 sm:flex-row sm:items-end">
          <div className="flex-1">
            <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ordenar por</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className={selectClass} disabled={loading}>
              <option value="created_at">Data de criação</option>
              <option value="estimated_delivery">Entrega estimada</option>
              <option value="due_date">Vencimento</option>
              <option value="amount">Valor</option>
              <option value="criticality">Criticidade</option>
            </select>
          </div>
          <button onClick={toggleSortOrder} disabled={loading} className={btnSecondary}>
            {sortOrder === "asc" ? "↑ Ascendente" : "↓ Descendente"}
          </button>
          <button onClick={onApplyFilters} disabled={loading} className={btnPrimary}>
            Aplicar Filtros
          </button>
          <button onClick={onClearFilters} disabled={loading} className={btnSecondary}>
            Limpar
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-100 bg-zinc-50/80">
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Tracking</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">NF</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Cliente</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">UF</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Coleta</th>
              <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Valor NF</th>
              <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Frete</th>
              <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">% Frete</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Entrega</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Vencimento</th>
              <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atraso</th>
              <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Criticidade</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={13} className="px-4 py-8 text-center text-sm text-zinc-400">
                  <div className="flex items-center justify-center gap-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
                    Carregando...
                  </div>
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={13} className="px-4 py-8 text-center text-sm text-zinc-400">
                  Nenhum envio encontrado.
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                  <td className="px-4 py-3">
                    <a href={`/shipments/${item.id}`} className="font-medium text-zinc-900 transition-colors hover:text-red-600">
                      {item.tracking_code}
                    </a>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs text-zinc-600">{formatUnavailable(item.invoice_number)}</td>
                  <td className="px-4 py-3 font-medium text-zinc-700">{formatUnavailable(item.customer_name)}</td>
                  <td className="px-4 py-3 font-mono text-xs font-semibold text-zinc-600">{formatUnavailable(item.destination_uf)}</td>
                  <td className="px-4 py-3 text-xs text-zinc-500">{formatDateBR(item.collection_departure_date)}</td>
                  <td className="px-4 py-3 text-right font-mono text-xs font-medium text-zinc-700">{formatCurrencyBRL(item.invoice_value)}</td>
                  <td className="px-4 py-3 text-right font-mono text-xs font-medium text-zinc-700">{formatCurrencyBRL(item.freight_value)}</td>
                  <td className="px-4 py-3 text-right font-mono text-xs text-zinc-500">{formatPercentage(item.freight_percentage)}</td>
                  <td className="px-4 py-3">{getStatusBadge(item.status)}</td>
                  <td className="px-4 py-3 text-xs text-zinc-500">{formatDateBR(item.estimated_delivery)}</td>
                  <td className="px-4 py-3 text-xs text-zinc-500">{formatDateBR(item.due_date)}</td>
                  <td className="px-4 py-3 text-right">
                    <span className={`font-mono text-xs font-bold tabular-nums ${item.delay_days > 0 ? "text-red-600" : "text-zinc-400"}`}>
                      {item.delay_days > 0 ? `${item.delay_days}d` : "-"}
                    </span>
                  </td>
                  <td className="px-4 py-3">{getCriticalityBadge(item.criticality)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {!loading && totalPages > 1 && (
        <div className="flex items-center justify-between rounded-xl border border-zinc-200 bg-white px-4 py-3 shadow-sm">
          <p className="text-sm text-zinc-500">
            Página <span className="font-semibold text-zinc-700">{page}</span> de <span className="font-semibold text-zinc-700">{totalPages}</span> ({total} registros)
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="rounded-lg border border-zinc-200 bg-white px-4 py-2 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              ← Anterior
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="rounded-lg border border-zinc-200 bg-white px-4 py-2 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Próxima →
            </button>
          </div>
        </div>
      )}

      <p className="text-[11px] text-zinc-400">
        Listagem limitada a 20 registros por página. Use os filtros para refinar resultados.
      </p>
    </section>
  );
}
