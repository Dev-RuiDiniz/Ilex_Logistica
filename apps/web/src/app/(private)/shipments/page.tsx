"use client";

import { ChangeEvent, Suspense, useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useSearchParams, useRouter, usePathname } from "next/navigation";

import { createShipment, listCarriers, listShipments } from "@/lib/api";
import { canViewShipments, canWriteShipments } from "@/lib/permissions";
import { buildGlobalSearchParams, monthYearToDateRange } from "@/lib/shipment-utils";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { Carrier, CreateShipmentRequest, Shipment, ShipmentListParams } from "@/lib/types";

const STATUS_OPTIONS = [
  { value: "pending", label: "Pendente" },
  { value: "in_transit", label: "Em trânsito" },
  { value: "delivered", label: "Entregue" },
  { value: "failed", label: "Falhou" },
];

const CRITICALITY_OPTIONS = [
  { value: "normal", label: "Normal" },
  { value: "baixa", label: "Baixa" },
  { value: "media", label: "Média" },
  { value: "alta", label: "Alta" },
];

const SLA_OPTIONS = [
  { value: "on_time", label: "No prazo" },
  { value: "warning", label: "Atenção" },
  { value: "late", label: "Atrasado" },
  { value: "critical", label: "Crítico" },
  { value: "unknown", label: "Indefinido" },
];

const SORT_OPTIONS = [
  { value: "created_at", label: "Data de criação" },
  { value: "estimated_delivery", label: "Entrega estimada" },
  { value: "due_date", label: "Vencimento" },
  { value: "amount", label: "Valor" },
  { value: "criticality", label: "Criticidade" },
];

function ShipmentsPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const { session } = useAuth();
  const [items, setItems] = useState<Shipment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [showFilters, setShowFilters] = useState(true);
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

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [carriers, setCarriers] = useState<Carrier[]>([]);
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState("");
  const [form, setForm] = useState<CreateShipmentRequest>({
    tracking_code: "",
    carrier_id: 0,
    estimated_delivery: "",
    recipient_name: "",
    recipient_phone: "",
    origin_address: "",
    destination_address: "",
  });

  const [useMonthYearFilter, setUseMonthYearFilter] = useState(false);
  const [monthYearTarget, setMonthYearTarget] = useState<"estimated_delivery" | "due_date">("estimated_delivery");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [selectedYear, setSelectedYear] = useState("");

  const [sortBy, setSortBy] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  const canView = canViewShipments(session?.role ?? "auditoria");
  const canCreate = canWriteShipments(session?.role ?? "auditoria");
  const { handleApiError } = useApiErrorHandler();

  const loadCarriers = useCallback(async () => {
    if (!session) return;
    try {
      const response = await listCarriers(session.accessToken);
      setCarriers(response);
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao carregar transportadoras"));
    }
  }, [session, handleApiError]);

  const resetForm = () => {
    setForm({
      tracking_code: "",
      carrier_id: 0,
      estimated_delivery: "",
      recipient_name: "",
      recipient_phone: "",
      origin_address: "",
      destination_address: "",
    });
    setCreateError("");
  };

  const openCreateModal = () => {
    void loadCarriers();
    resetForm();
    setShowCreateModal(true);
  };

  const closeCreateModal = () => {
    setShowCreateModal(false);
    resetForm();
  };

  const updateForm = <K extends keyof CreateShipmentRequest>(field: K, value: CreateShipmentRequest[K]) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const onSubmitCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) return;
    setCreateLoading(true);
    setCreateError("");
    try {
      const payload = {
        ...form,
        carrier_id: Number(form.carrier_id),
      };
      await createShipment(session.accessToken, payload);
      setShowCreateModal(false);
      resetForm();
      setPage(1);
      void load();
    } catch (err) {
      setCreateError(err instanceof Error ? err.message : "Erro ao criar envio");
      handleApiError(err instanceof Error ? err : new Error("Erro ao criar envio"));
    } finally {
      setCreateLoading(false);
    }
  };

  const activeFiltersCount = [
    statusFilter, carrierIdFilter, criticalityFilter, estimatedDeliveryFrom, estimatedDeliveryTo,
    dueDateFrom, dueDateTo, collectionDepartureFrom, collectionDepartureTo, customerNameFilter,
    destinationUfFilter, invoiceNumberFilter, invoiceKeyFilter, fiscalDocumentFilter,
    freightValueMin, freightValueMax, invoiceValueMin, invoiceValueMax, freightPercentageMin,
    freightPercentageMax, amountMin, amountMax, slaStatusFilter, isLateFilter,
    useMonthYearFilter ? "monthYear" : "",
  ].filter(Boolean).length;

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
          temporalFilter = { estimated_delivery_from: dateRange.from, estimated_delivery_to: dateRange.to };
        } else {
          temporalFilter = { due_date_from: dateRange.from, due_date_to: dateRange.to };
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
    slaStatusFilter, isLateFilter, collectionDepartureFrom, collectionDepartureTo,
    handleApiError,
  ]);

  useEffect(() => {
    const timer = setTimeout(() => { void load(); }, 0);
    return () => clearTimeout(timer);
  }, [load]);

  useEffect(() => {
    const urlSearch = searchParams.get("search");
    const urlStatus = searchParams.get("status");
    const urlCarrierId = searchParams.get("carrier_id");
    const urlCriticality = searchParams.get("criticality");
    const urlCustomerName = searchParams.get("customer_name");
    const urlDestinationUf = searchParams.get("destination_uf");
    const urlInvoiceNumber = searchParams.get("invoice_number");
    const urlSlaStatus = searchParams.get("sla_status");
    const urlIsLate = searchParams.get("is_late");
    const urlSortBy = searchParams.get("sort_by");
    const urlSortOrder = searchParams.get("sort_order");
    const urlPage = searchParams.get("page");

    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (urlSearch) setSearch(urlSearch);

    if (urlStatus) setStatusFilter(urlStatus);
    if (urlCarrierId) setCarrierIdFilter(urlCarrierId);
    if (urlCriticality) setCriticalityFilter(urlCriticality);
    if (urlCustomerName) setCustomerNameFilter(urlCustomerName);
    if (urlDestinationUf) setDestinationUfFilter(urlDestinationUf);
    if (urlInvoiceNumber) setInvoiceNumberFilter(urlInvoiceNumber);
    if (urlSlaStatus) setSlaStatusFilter(urlSlaStatus);
    if (urlIsLate) setIsLateFilter(urlIsLate);
    if (urlSortBy) setSortBy(urlSortBy);
    if (urlSortOrder === "asc" || urlSortOrder === "desc") setSortOrder(urlSortOrder);
    if (urlPage) {
      const p = parseInt(urlPage, 10);
      if (p > 0) setPage(p);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const syncUrl = useCallback(() => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (statusFilter) params.set("status", statusFilter);
    if (carrierIdFilter) params.set("carrier_id", carrierIdFilter);
    if (criticalityFilter) params.set("criticality", criticalityFilter);
    if (estimatedDeliveryFrom) params.set("estimated_delivery_from", estimatedDeliveryFrom);
    if (estimatedDeliveryTo) params.set("estimated_delivery_to", estimatedDeliveryTo);
    if (dueDateFrom) params.set("due_date_from", dueDateFrom);
    if (dueDateTo) params.set("due_date_to", dueDateTo);
    if (collectionDepartureFrom) params.set("collection_departure_from", collectionDepartureFrom);
    if (collectionDepartureTo) params.set("collection_departure_to", collectionDepartureTo);
    if (customerNameFilter) params.set("customer_name", customerNameFilter);
    if (destinationUfFilter) params.set("destination_uf", destinationUfFilter);
    if (invoiceNumberFilter) params.set("invoice_number", invoiceNumberFilter);
    if (invoiceKeyFilter) params.set("invoice_key", invoiceKeyFilter);
    if (fiscalDocumentFilter) params.set("fiscal_document", fiscalDocumentFilter);
    if (freightValueMin) params.set("freight_value_min", freightValueMin);
    if (freightValueMax) params.set("freight_value_max", freightValueMax);
    if (invoiceValueMin) params.set("invoice_value_min", invoiceValueMin);
    if (invoiceValueMax) params.set("invoice_value_max", invoiceValueMax);
    if (freightPercentageMin) params.set("freight_percentage_min", freightPercentageMin);
    if (freightPercentageMax) params.set("freight_percentage_max", freightPercentageMax);
    if (amountMin) params.set("amount_min", amountMin);
    if (amountMax) params.set("amount_max", amountMax);
    if (slaStatusFilter) params.set("sla_status", slaStatusFilter);
    if (isLateFilter) params.set("is_late", isLateFilter);
    if (sortBy !== "created_at") params.set("sort_by", sortBy);
    if (sortOrder !== "desc") params.set("sort_order", sortOrder);
    if (page > 1) params.set("page", String(page));
    const queryString = params.toString();
    router.replace(queryString ? `${pathname}?${queryString}` : pathname, { scroll: false });
  }, [
    router, pathname, search, statusFilter, carrierIdFilter, criticalityFilter,
    estimatedDeliveryFrom, estimatedDeliveryTo, dueDateFrom, dueDateTo,
    collectionDepartureFrom, collectionDepartureTo, customerNameFilter, destinationUfFilter,
    invoiceNumberFilter, invoiceKeyFilter, fiscalDocumentFilter,
    freightValueMin, freightValueMax, invoiceValueMin, invoiceValueMax,
    freightPercentageMin, freightPercentageMax, amountMin, amountMax,
    slaStatusFilter, isLateFilter, sortBy, sortOrder, page,
  ]);

  const urlSynced = useRef(false);
  useEffect(() => {
    if (!urlSynced.current) {
      urlSynced.current = true;
      return;
    }
    syncUrl();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, sortBy, sortOrder]);

  const onSearch = (event: ChangeEvent<HTMLInputElement>) => setSearch(event.target.value);
  const onSearchSubmit = () => { setPage(1); void load(); syncUrl(); };
  const onApplyFilters = () => { setPage(1); void load(); syncUrl(); };
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
    router.replace(pathname, { scroll: false });
  };
  const toggleSortOrder = () => { setSortOrder((prev) => (prev === "asc" ? "desc" : "asc")); };

  const formatCurrencyBRL = (value: number | null) => {
    if (value === null || value === undefined) return "—";
    return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
  };
  const formatDateBR = (dateString: string | null) => {
    if (!dateString) return "—";
    return new Date(dateString).toLocaleDateString("pt-BR");
  };
  const formatUnavailable = (value: string | number | null) => {
    if (value === null || value === undefined || value === "") return "—";
    return value;
  };

  const getStatusBadge = (status: string) => {
    const map: Record<string, { color: string; label: string }> = {
      pending: { color: "bg-zinc-100 text-zinc-700 ring-1 ring-zinc-500/20", label: "Pendente" },
      in_transit: { color: "bg-blue-50 text-blue-700 ring-1 ring-blue-600/20", label: "Em trânsito" },
      delivered: { color: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20", label: "Entregue" },
      failed: { color: "bg-red-50 text-red-700 ring-1 ring-red-600/20", label: "Falhou" },
    };
    const badge = map[status] || { color: "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20", label: status };
    return (
      <span className={`inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold ${badge.color}`}>
        {badge.label}
      </span>
    );
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
      <span className={`inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold ${badge.color}`}>
        {badge.label}
      </span>
    );
  };

  if (!canView) {
    return (
      <div className="space-y-5">
        <Header total={total} />
        <AccessDenied message="Seu perfil não tem permissão para visualizar envios." />
      </div>
    );
  }

  return (
<<<<<<< HEAD
    <div className="space-y-5">
      <Header total={total}>
        {canCreate && (
          <button onClick={openCreateModal} className="btn-primary flex items-center gap-2">
            <IconPlus className="h-4 w-4" />
            Novo envio
=======
    <section className="page-stack">
      <header className="page-hero">
        <p className="page-kicker">Operação de envios</p>
        <h2 className="page-title !text-[clamp(1.65rem,1.3rem+0.8vw,2.4rem)]">Envios</h2>
        <p className="page-subtitle">
          Filtre por janela, criticidade e contexto fiscal para encontrar rapidamente o que
          precisa de acompanhamento ou tratativa.
        </p>
      </header>

      {!canView && <p className="error-state">Perfil sem permissão para visualizar envios.</p>}

      <div className="surface-panel p-5 md:p-6 space-y-5">
        <div>
          <h3 className="section-title">Busca e filtros</h3>
          <p className="section-subtitle">Separe rapidamente o operacional do crítico com filtros combinados.</p>
        </div>
        <div className="flex flex-col gap-2 md:flex-row md:items-end">
          <div className="flex-1">
            <label className="field-label">Buscar</label>
            <input
              value={search}
              onChange={onSearch}
              placeholder="Buscar por tracking, NF, cliente, etc."
              className="field"
              disabled={loading}
            />
          </div>
          <button
            onClick={onSearchSubmit}
            disabled={loading}
            className="button-primary"
          >
            Buscar
>>>>>>> fix/infra-setup-local
          </button>
        )}
      </Header>

<<<<<<< HEAD
      {/* Search bar */}
      <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start">
          <div className="flex-1">
            <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Buscar envios</label>
            <div className="mt-1.5 flex gap-2">
              <div className="relative flex-1">
                <input
                  value={search}
                  onChange={onSearch}
                  placeholder="Tracking, NF, cliente, transportadora..."
                  className="w-full rounded-lg border border-zinc-200 bg-white py-2.5 pl-10 pr-4 text-sm text-zinc-900 placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50"
                  disabled={loading}
                  onKeyDown={(e) => e.key === "Enter" && onSearchSubmit()}
                />
                <IconSearch className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
              </div>
              <button onClick={onSearchSubmit} disabled={loading} className="btn-primary">
                Buscar
              </button>
            </div>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
            <button
              onClick={() => setShowFilters((s) => !s)}
              className="btn-secondary flex items-center gap-2"
=======
        {/* Filtro temporal por mês/ano */}
        <div className="surface-muted p-4">
          <div className="flex items-center gap-2 mb-2">
            <input
              type="checkbox"
              id="useMonthYearFilter"
              checked={useMonthYearFilter}
              onChange={(e) => setUseMonthYearFilter(e.target.checked)}
              disabled={loading}
              className="rounded"
            />
            <label htmlFor="useMonthYearFilter" className="text-sm font-semibold text-slate-800">Filtro por mês/ano</label>
          </div>
          {useMonthYearFilter && (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div>
                <label className="field-label">Aplicar em</label>
                <select
                  value={monthYearTarget}
                  onChange={(e) => setMonthYearTarget(e.target.value as "estimated_delivery" | "due_date")}
                  className="field-select"
                  disabled={loading}
                >
                  <option value="estimated_delivery">Entrega estimada</option>
                  <option value="due_date">Vencimento</option>
                </select>
              </div>
              <div>
                <label className="field-label">Mês</label>
                <select
                  value={selectedMonth}
                  onChange={(e) => setSelectedMonth(e.target.value)}
                  className="field-select"
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
                <label className="field-label">Ano</label>
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(e.target.value)}
                  className="field-select"
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
        <div className="surface-muted p-4">
          <h4 className="section-title !text-base">Filtros manuais</h4>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div>
              <label className="field-label">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="field-select"
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
              <label className="field-label">Carrier ID</label>
              <input
                type="number"
                value={carrierIdFilter}
                onChange={(e) => setCarrierIdFilter(e.target.value)}
                placeholder="ID da transportadora"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Criticidade</label>
              <select
                value={criticalityFilter}
                onChange={(e) => setCriticalityFilter(e.target.value)}
                className="field-select"
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
              <label className="field-label">Cliente</label>
              <input
                type="text"
                value={customerNameFilter}
                onChange={(e) => setCustomerNameFilter(e.target.value)}
                placeholder="Nome do cliente"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">UF Destino</label>
              <input
                type="text"
                value={destinationUfFilter}
                onChange={(e) => setDestinationUfFilter(e.target.value)}
                placeholder="UF (ex: SP)"
                maxLength={2}
                className="field uppercase"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Entrega estimada (de)</label>
              <input
                type="date"
                value={estimatedDeliveryFrom}
                onChange={(e) => setEstimatedDeliveryFrom(e.target.value)}
                className="field"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="field-label">Entrega estimada (até)</label>
              <input
                type="date"
                value={estimatedDeliveryTo}
                onChange={(e) => setEstimatedDeliveryTo(e.target.value)}
                className="field"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="field-label">Vencimento (de)</label>
              <input
                type="date"
                value={dueDateFrom}
                onChange={(e) => setDueDateFrom(e.target.value)}
                className="field"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="field-label">Vencimento (até)</label>
              <input
                type="date"
                value={dueDateTo}
                onChange={(e) => setDueDateTo(e.target.value)}
                className="field"
                disabled={loading || useMonthYearFilter}
              />
            </div>
            <div>
              <label className="field-label">Coleta/Saída (de)</label>
              <input
                type="date"
                value={collectionDepartureFrom}
                onChange={(e) => setCollectionDepartureFrom(e.target.value)}
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Coleta/Saída (até)</label>
              <input
                type="date"
                value={collectionDepartureTo}
                onChange={(e) => setCollectionDepartureTo(e.target.value)}
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Número NF</label>
              <input
                type="text"
                value={invoiceNumberFilter}
                onChange={(e) => setInvoiceNumberFilter(e.target.value)}
                placeholder="Número da NF"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Chave NF-e</label>
              <input
                type="text"
                value={invoiceKeyFilter}
                onChange={(e) => setInvoiceKeyFilter(e.target.value)}
                placeholder="Chave de acesso NF-e"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Documento Fiscal</label>
              <input
                type="text"
                value={fiscalDocumentFilter}
                onChange={(e) => setFiscalDocumentFilter(e.target.value)}
                placeholder="Documento fiscal"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor Frete Mín.</label>
              <input
                type="number"
                step="0.01"
                value={freightValueMin}
                onChange={(e) => setFreightValueMin(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor Frete Máx.</label>
              <input
                type="number"
                step="0.01"
                value={freightValueMax}
                onChange={(e) => setFreightValueMax(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor NF Mín.</label>
              <input
                type="number"
                step="0.01"
                value={invoiceValueMin}
                onChange={(e) => setInvoiceValueMin(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor NF Máx.</label>
              <input
                type="number"
                step="0.01"
                value={invoiceValueMax}
                onChange={(e) => setInvoiceValueMax(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">% Frete Mín.</label>
              <input
                type="number"
                step="0.01"
                value={freightPercentageMin}
                onChange={(e) => setFreightPercentageMin(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">% Frete Máx.</label>
              <input
                type="number"
                step="0.01"
                value={freightPercentageMax}
                onChange={(e) => setFreightPercentageMax(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor Total Mín.</label>
              <input
                type="number"
                step="0.01"
                value={amountMin}
                onChange={(e) => setAmountMin(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
            <div>
              <label className="field-label">Valor Total Máx.</label>
              <input
                type="number"
                step="0.01"
                value={amountMax}
                onChange={(e) => setAmountMax(e.target.value)}
                placeholder="0.00"
                className="field"
                disabled={loading}
              />
            </div>
          </div>
        </div>

        {/* Ordenação */}
        <div className="surface-muted flex flex-col gap-2 p-4 md:flex-row md:items-center">
          <div className="flex-1">
            <label className="field-label">Ordenar por</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="field-select"
              disabled={loading}
>>>>>>> fix/infra-setup-local
            >
              <IconFilter className="h-4 w-4" />
              Filtros {activeFiltersCount > 0 && (
                <span className="ml-1 rounded-full bg-red-600 px-1.5 py-0.5 text-[10px] font-bold text-white">
                  {activeFiltersCount}
                </span>
              )}
            </button>
            <button onClick={onClearFilters} disabled={loading} className="btn-secondary">
              Limpar
            </button>
          </div>
<<<<<<< HEAD
        </div>

        {/* Collapsible filters */}
        {showFilters && (
          <div className="mt-5 border-t border-zinc-100 pt-5">
            <div className="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
              <SelectGroup label="Status" value={statusFilter} onChange={setStatusFilter} options={[{ value: "", label: "Todos" }, ...STATUS_OPTIONS]} />
              <SelectGroup label="Criticidade" value={criticalityFilter} onChange={setCriticalityFilter} options={[{ value: "", label: "Todas" }, ...CRITICALITY_OPTIONS]} />
              <SelectGroup label="SLA" value={slaStatusFilter} onChange={setSlaStatusFilter} options={[{ value: "", label: "Todos" }, ...SLA_OPTIONS]} />
              <SelectGroup
                label="Atrasado?"
                value={isLateFilter}
                onChange={setIsLateFilter}
                options={[
                  { value: "", label: "Todos" },
                  { value: "true", label: "Sim" },
                  { value: "false", label: "Não" },
                ]}
              />
              <InputGroup label="Carrier ID" value={carrierIdFilter} onChange={setCarrierIdFilter} type="number" placeholder="ID" />
              <InputGroup label="UF Destino" value={destinationUfFilter} onChange={setDestinationUfFilter} placeholder="UF" maxLength={2} upper />
              <InputGroup label="Cliente" value={customerNameFilter} onChange={setCustomerNameFilter} placeholder="Nome do cliente" />
              <InputGroup label="Número NF" value={invoiceNumberFilter} onChange={setInvoiceNumberFilter} placeholder="NF" />
              <InputGroup label="Chave NF-e" value={invoiceKeyFilter} onChange={setInvoiceKeyFilter} placeholder="Chave NF-e" />
              <InputGroup label="Documento Fiscal" value={fiscalDocumentFilter} onChange={setFiscalDocumentFilter} placeholder="Documento fiscal" />
              <RangeGroup label="Valor Frete" min={freightValueMin} max={freightValueMax} onMinChange={setFreightValueMin} onMaxChange={setFreightValueMax} />
              <RangeGroup label="Valor NF" min={invoiceValueMin} max={invoiceValueMax} onMinChange={setInvoiceValueMin} onMaxChange={setInvoiceValueMax} />
              <RangeGroup label="% Frete" min={freightPercentageMin} max={freightPercentageMax} onMinChange={setFreightPercentageMin} onMaxChange={setFreightPercentageMax} />
              <RangeGroup label="Valor Total" min={amountMin} max={amountMax} onMinChange={setAmountMin} onMaxChange={setAmountMax} />
              <DateGroup label="Entrega estimada" from={estimatedDeliveryFrom} to={estimatedDeliveryTo} onFromChange={setEstimatedDeliveryFrom} onToChange={setEstimatedDeliveryTo} disabled={useMonthYearFilter} />
              <DateGroup label="Vencimento" from={dueDateFrom} to={dueDateTo} onFromChange={setDueDateFrom} onToChange={setDueDateTo} disabled={useMonthYearFilter} />
              <DateGroup label="Coleta/Saída" from={collectionDepartureFrom} to={collectionDepartureTo} onFromChange={setCollectionDepartureFrom} onToChange={setCollectionDepartureTo} />
            </div>

            {/* Month/Year filter */}
            <div className="mt-5 rounded-xl border border-zinc-100 bg-zinc-50/50 p-4">
              <div className="flex items-center gap-2">
                <input
                  id="useMonthYearFilter"
                  type="checkbox"
                  checked={useMonthYearFilter}
                  onChange={(e) => setUseMonthYearFilter(e.target.checked)}
                  className="h-4 w-4 rounded border-zinc-300 text-red-600 focus:ring-red-500"
                />
                <label htmlFor="useMonthYearFilter" className="text-sm font-semibold text-zinc-700">Filtro por Mês/Ano</label>
              </div>
              {useMonthYearFilter && (
                <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-3">
                  <select value={monthYearTarget} onChange={(e) => setMonthYearTarget(e.target.value as "estimated_delivery" | "due_date")} className="input">
                    <option value="estimated_delivery">Entrega estimada</option>
                    <option value="due_date">Vencimento</option>
                  </select>
                  <select value={selectedMonth} onChange={(e) => setSelectedMonth(e.target.value)} className="input">
                    <option value="">Mês</option>
                    {Array.from({ length: 12 }, (_, i) => (
                      <option key={i + 1} value={i + 1}>{new Date(0, i).toLocaleString("pt-BR", { month: "long" })}</option>
                    ))}
                  </select>
                  <select value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)} className="input">
                    <option value="">Ano</option>
                    {[2024, 2025, 2026, 2027].map((y) => (
                      <option key={y} value={y}>{y}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <div className="mt-5 flex items-center justify-end gap-2">
              <button onClick={onApplyFilters} disabled={loading} className="btn-primary">
                Aplicar Filtros
              </button>
            </div>
          </div>
        )}

        {/* Sort */}
        <div className="mt-5 flex flex-col gap-3 border-t border-zinc-100 pt-5 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ordenar</span>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="input w-48">
              {SORT_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
            <button onClick={toggleSortOrder} className="btn-secondary px-3">
              {sortOrder === "asc" ? "↑" : "↓"}
            </button>
          </div>
          <p className="text-[11px] text-zinc-400">
            {total} {total === 1 ? "registro" : "registros"} • {pageSize} por página
          </p>
        </div>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {/* Table */}
      <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-100 bg-zinc-50/80">
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Tracking</th>
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">NF</th>
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Cliente</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wide text-zinc-500">UF</th>
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Valor NF</th>
                <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Frete</th>
                <th className="px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Atraso</th>
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Criticidade</th>
                <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Entrega</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={10} className="px-4 py-10 text-center">
                    <div className="flex items-center justify-center gap-3 text-zinc-500">
                      <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-300 border-t-red-600" />
                      <span className="text-sm font-medium">Carregando envios...</span>
                    </div>
=======
          <button
            onClick={toggleSortOrder}
            disabled={loading}
            className="button-secondary"
          >
            {sortOrder === "asc" ? "Ascendente" : "Descendente"}
          </button>
          <button
            onClick={onApplyFilters}
            disabled={loading}
            className="button-primary"
          >
            Aplicar Filtros
          </button>
          <button
            onClick={onClearFilters}
            disabled={loading}
            className="button-ghost"
          >
            Limpar Filtros
          </button>
        </div>
      </div>

      {error && <p className="error-state">{error}</p>}

      {/* Tabela */}
      <div className="table-shell overflow-x-auto">
        <table className="data-table">
          <thead className="text-left">
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
                <td colSpan={13} className="px-3 py-3 text-slate-700">
                  Carregando...
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={13} className="px-3 py-3 text-slate-700">
                  Nenhum envio encontrado.
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id}>
                  <td className="px-3 py-2">
                    <a href={`/shipments/${item.id}`} className="text-blue-700 hover:underline">
                      {item.tracking_code}
                    </a>
>>>>>>> fix/infra-setup-local
                  </td>
                </tr>
              ) : items.length === 0 ? (
                <tr>
                  <td colSpan={10} className="px-4 py-10 text-center text-sm text-zinc-400">
                    Nenhum envio encontrado.
                  </td>
                </tr>
              ) : (
                items.map((item) => (
                  <tr key={item.id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/60">
                    <td className="px-4 py-3">
                      <Link href={`/shipments/${item.id}`} className="font-semibold text-zinc-900 transition-colors hover:text-red-600">
                        {item.tracking_code}
                      </Link>
                      <p className="text-[11px] text-zinc-400">{formatDateBR(item.collection_departure_date)}</p>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-zinc-600">{formatUnavailable(item.invoice_number)}</td>
                    <td className="px-4 py-3">
                      <p className="font-medium text-zinc-700">{formatUnavailable(item.customer_name)}</p>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="inline-flex rounded-md bg-zinc-100 px-2 py-0.5 text-xs font-semibold text-zinc-600">
                        {formatUnavailable(item.destination_uf)}
                      </span>
                    </td>
                    <td className="px-4 py-3">{getStatusBadge(item.status)}</td>
                    <td className="px-4 py-3 text-right font-mono text-xs font-medium text-zinc-700">{formatCurrencyBRL(item.invoice_value)}</td>
                    <td className="px-4 py-3 text-right font-mono text-xs text-zinc-500">{formatCurrencyBRL(item.freight_value)}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`font-mono text-xs font-bold tabular-nums ${item.delay_days > 0 ? "text-red-600" : "text-zinc-400"}`}>
                        {item.delay_days > 0 ? `${item.delay_days}d` : "—"}
                      </span>
                    </td>
                    <td className="px-4 py-3">{getCriticalityBadge(item.criticality)}</td>
                    <td className="px-4 py-3 text-xs text-zinc-500">
                      <p>{formatDateBR(item.estimated_delivery)}</p>
                      <p className="text-[11px] text-zinc-400">Venc: {formatDateBR(item.due_date)}</p>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {!loading && totalPages > 1 && (
<<<<<<< HEAD
        <div className="flex items-center justify-between rounded-2xl border border-zinc-200 bg-white px-4 py-3 shadow-sm">
          <p className="text-sm text-zinc-500">
            Página <span className="font-semibold text-zinc-900">{page}</span> de <span className="font-semibold text-zinc-900">{totalPages}</span>
=======
        <div className="surface-panel-strong flex items-center justify-between px-4 py-3">
          <p className="text-sm text-slate-700">
            Página {page} de {totalPages} ({total} registros)
>>>>>>> fix/infra-setup-local
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
<<<<<<< HEAD
              className="btn-secondary disabled:opacity-40"
=======
              className="button-secondary !px-3 !py-2"
>>>>>>> fix/infra-setup-local
            >
              ← Anterior
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
<<<<<<< HEAD
              className="btn-secondary disabled:opacity-40"
=======
              className="button-secondary !px-3 !py-2"
>>>>>>> fix/infra-setup-local
            >
              Próxima →
            </button>
          </div>
        </div>
      )}

<<<<<<< HEAD
      {showCreateModal && (
        <CreateShipmentModal
          carriers={carriers}
          form={form}
          onChange={updateForm}
          onSubmit={onSubmitCreate}
          onClose={closeCreateModal}
          loading={createLoading}
          error={createError}
        />
      )}
    </div>
  );
}

function Header({ total, children }: { total: number; children?: React.ReactNode }) {
  return (
    <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Envios</h1>
        <p className="mt-1 text-sm font-medium text-zinc-500">Gestão e acompanhamento de todos os envios</p>
      </div>
      <div className="flex flex-col items-start gap-3 sm:flex-row sm:items-center">
        <div className="flex items-center gap-3 rounded-xl border border-zinc-200 bg-white px-4 py-2.5 shadow-sm">
          <span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" />
          <span className="text-sm font-semibold text-zinc-900">{total}</span>
          <span className="text-xs text-zinc-500">{total === 1 ? "registro" : "registros"}</span>
        </div>
        {children}
      </div>
    </header>
  );
}

function InputGroup({
  label,
  value,
  onChange,
  type = "text",
  placeholder,
  maxLength,
  upper,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  placeholder?: string;
  maxLength?: number;
  upper?: boolean;
}) {
  return (
    <div>
      <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(upper ? e.target.value.toUpperCase() : e.target.value)}
        placeholder={placeholder}
        maxLength={maxLength}
        className="input"
      />
    </div>
  );
}

function SelectGroup({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
}) {
  return (
    <div>
      <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)} className="input">
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  );
}

function RangeGroup({
  label,
  min,
  max,
  onMinChange,
  onMaxChange,
}: {
  label: string;
  min: string;
  max: string;
  onMinChange: (value: string) => void;
  onMaxChange: (value: string) => void;
}) {
  return (
    <div>
      <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</label>
      <div className="mt-1.5 grid grid-cols-2 gap-2">
        <input
          type="number"
          step="0.01"
          value={min}
          onChange={(e) => onMinChange(e.target.value)}
          placeholder="Mín"
          className="input"
        />
        <input
          type="number"
          step="0.01"
          value={max}
          onChange={(e) => onMaxChange(e.target.value)}
          placeholder="Máx"
          className="input"
        />
      </div>
    </div>
  );
}

function DateGroup({
  label,
  from,
  to,
  onFromChange,
  onToChange,
  disabled,
}: {
  label: string;
  from: string;
  to: string;
  onFromChange: (value: string) => void;
  onToChange: (value: string) => void;
  disabled?: boolean;
}) {
  return (
    <div>
      <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</label>
      <div className="mt-1.5 grid grid-cols-2 gap-2">
        <input type="date" value={from} onChange={(e) => onFromChange(e.target.value)} className="input" disabled={disabled} />
        <input type="date" value={to} onChange={(e) => onToChange(e.target.value)} className="input" disabled={disabled} />
      </div>
    </div>
  );
}

function NumberGroup({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) {
  return (
    <div>
      <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{label}</label>
      <input
        type="number"
        step="0.01"
        min="0"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="input"
      />
    </div>
  );
}

function CreateShipmentModal({
  carriers,
  form,
  onChange,
  onSubmit,
  onClose,
  loading,
  error,
}: {
  carriers: Carrier[];
  form: CreateShipmentRequest;
  onChange: <K extends keyof CreateShipmentRequest>(field: K, value: CreateShipmentRequest[K]) => void;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
  loading: boolean;
  error: string;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
      <div className="w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border border-zinc-200 bg-white shadow-2xl">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <div>
            <h2 className="text-lg font-bold text-zinc-900">Novo envio</h2>
            <p className="text-xs text-zinc-500">Preencha os dados obrigatórios para cadastrar um novo envio</p>
          </div>
          <button onClick={onClose} className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600">
            <IconX className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={onSubmit} className="space-y-5 p-6">
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <InputGroup
              label="Código de rastreio *"
              value={form.tracking_code}
              onChange={(v) => onChange("tracking_code", v)}
              placeholder="Ex: BR123456789"
              maxLength={100}
            />
            <div>
              <label className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Transportadora *</label>
              <select
                value={form.carrier_id}
                onChange={(e) => onChange("carrier_id", Number(e.target.value))}
                className="input"
                required
              >
                <option value={0}>Selecione...</option>
                {carriers.map((carrier) => (
                  <option key={carrier.id} value={carrier.id}>{carrier.name}</option>
                ))}
              </select>
            </div>
            <InputGroup
              label="Entrega estimada *"
              value={form.estimated_delivery}
              onChange={(v) => onChange("estimated_delivery", v)}
              type="datetime-local"
            />
            <InputGroup
              label="Cliente"
              value={form.customer_name ?? ""}
              onChange={(v) => onChange("customer_name", v || undefined)}
              placeholder="Nome do cliente"
            />
            <InputGroup
              label="Destinatário *"
              value={form.recipient_name}
              onChange={(v) => onChange("recipient_name", v)}
              placeholder="Nome do destinatário"
            />
            <InputGroup
              label="Telefone destinatário *"
              value={form.recipient_phone}
              onChange={(v) => onChange("recipient_phone", v)}
              placeholder="(00) 00000-0000"
            />
            <InputGroup
              label="Endereço origem *"
              value={form.origin_address}
              onChange={(v) => onChange("origin_address", v)}
              placeholder="Endereço completo de origem"
            />
            <InputGroup
              label="Endereço destino *"
              value={form.destination_address}
              onChange={(v) => onChange("destination_address", v)}
              placeholder="Endereço completo de destino"
            />
            <InputGroup
              label="Número NF"
              value={form.invoice_number ?? ""}
              onChange={(v) => onChange("invoice_number", v || undefined)}
              placeholder="123456"
              maxLength={50}
            />
            <InputGroup
              label="Chave NF-e"
              value={form.invoice_key ?? ""}
              onChange={(v) => onChange("invoice_key", v || undefined)}
              placeholder="Chave de acesso da NF-e"
              maxLength={100}
            />
            <InputGroup
              label="Documento fiscal"
              value={form.fiscal_document ?? ""}
              onChange={(v) => onChange("fiscal_document", v || undefined)}
              placeholder="Documento fiscal"
              maxLength={50}
            />
            <InputGroup
              label="UF destino"
              value={form.destination_uf ?? ""}
              onChange={(v) => onChange("destination_uf", v.toUpperCase() || undefined)}
              placeholder="SP"
              maxLength={2}
              upper
            />
            <NumberGroup
              label="Valor total (R$)"
              value={form.amount?.toString() ?? ""}
              onChange={(v) => onChange("amount", v ? Number(v) : undefined)}
              placeholder="0,00"
            />
            <InputGroup
              label="Vencimento"
              value={form.due_date ?? ""}
              onChange={(v) => onChange("due_date", v || undefined)}
              type="datetime-local"
            />
            <NumberGroup
              label="Valor frete (R$)"
              value={form.freight_value?.toString() ?? ""}
              onChange={(v) => onChange("freight_value", v ? Number(v) : undefined)}
              placeholder="0,00"
            />
            <NumberGroup
              label="Valor NF (R$)"
              value={form.invoice_value?.toString() ?? ""}
              onChange={(v) => onChange("invoice_value", v ? Number(v) : undefined)}
              placeholder="0,00"
            />
            <InputGroup
              label="Data coleta/saída"
              value={form.collection_departure_date ?? ""}
              onChange={(v) => onChange("collection_departure_date", v || undefined)}
              type="datetime-local"
            />
          </div>

          <div className="flex items-center justify-end gap-3 border-t border-zinc-100 pt-5">
            <button type="button" onClick={onClose} className="btn-secondary" disabled={loading}>
              Cancelar
            </button>
            <button type="submit" className="btn-primary flex items-center gap-2" disabled={loading}>
              {loading && <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-red-600" />}
              Salvar envio
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function ShipmentsPage() {
  return (
    <Suspense fallback={<div className="p-4 text-sm text-zinc-500">Carregando envios...</div>}>
      <ShipmentsPageContent />
    </Suspense>
  );
}

function IconPlus({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}

function IconX({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  );
}

function IconSearch({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
    </svg>
  );
}

function IconFilter({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.106 1.94l-1.92 1.12a2.25 2.25 0 01-3.406-1.94V13.36c0-.596.237-1.167.659-1.591l5.432-5.432A2.25 2.25 0 0012.659 3.878 41.445 41.445 0 0112 3z" />
    </svg>
=======
      {/* Limitação documentada */}
      <p className="text-xs text-slate-700">
        Esta listagem é limitada a 20 registros por página. Use os filtros para refinar sua busca.
      </p>
    </section>
>>>>>>> fix/infra-setup-local
  );
}
