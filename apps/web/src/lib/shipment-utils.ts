import type { ShipmentListParams } from "./types";

/**
 * Converte mês/ano em intervalo de datas (primeiro e último dia do mês)
 * @param month Mês (1-12)
 * @param year Ano (ex: 2026)
 * @returns Objeto com from e to em formato ISO (YYYY-MM-DD)
 */
export function monthYearToDateRange(month: number, year: number): { from: string; to: string } {
  const from = new Date(year, month - 1, 1);
  const to = new Date(year, month, 0); // Último dia do mês

  return {
    from: from.toISOString().split("T")[0],
    to: to.toISOString().split("T")[0],
  };
}

/**
 * Monta parâmetros de busca para listagem de shipments
 * @param searchType Tipo de busca: 'tracking' | 'invoice' | 'all'
 * @param searchQuery Termo de busca
 * @returns Objeto com parâmetros de busca apropriados
 */
export function buildSearchParams(searchType: "tracking" | "invoice" | "all", searchQuery: string): Partial<ShipmentListParams> {
  if (!searchQuery.trim()) return {};

  if (searchType === "tracking") {
    return { tracking_code: searchQuery };
  }

  if (searchType === "invoice") {
    return { invoice_number: searchQuery };
  }

  // searchType === 'all': busca heurística
  // Se parece com número, assume invoice_number, senão tracking_code
  const isNumeric = /^\d+$/.test(searchQuery.trim());
  if (isNumeric) {
    return { invoice_number: searchQuery };
  }
  return { tracking_code: searchQuery };
}

/**
 * Monta parâmetros de busca global para listagem de shipments
 * @param searchQuery Termo de busca global
 * @returns Objeto com parâmetro de busca global
 */
export function buildGlobalSearchParams(searchQuery: string): Partial<ShipmentListParams> {
  if (!searchQuery.trim()) return {};
  return { search: searchQuery };
}

// BETA-011B: Formatting helpers for fiscal/financial fields

/**
 * Formata valor monetário em Reais (BRL)
 * @param value Valor numérico
 * @returns String formatada (ex: R$ 1.234,56) ou "-" se null/undefined
 */
export function formatCurrencyBRL(value: number | null): string {
  if (value === null || value === undefined) return "-";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

/**
 * Formata valor percentual
 * @param value Valor numérico
 * @returns String formatada (ex: 12,34%) ou "-" se null/undefined
 */
export function formatPercentage(value: number | null): string {
  if (value === null || value === undefined) return "-";
  return `${value.toFixed(2)}%`;
}

/**
 * Formata data para formato brasileiro (DD/MM/YYYY)
 * @param dateString String de data em formato ISO
 * @returns String formatada (ex: 10/06/2026) ou "-" se null/undefined/vazio
 */
export function formatDateBR(dateString: string | null): string {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("pt-BR");
}

/**
 * Formata valor genérico, retornando "-" se null/undefined/vazio
 * @param value Valor string ou numérico
 * @returns Valor original ou "-" se null/undefined/vazio
 */
export function formatUnavailable(value: string | number | null): string {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
}
