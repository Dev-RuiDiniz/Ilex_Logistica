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
