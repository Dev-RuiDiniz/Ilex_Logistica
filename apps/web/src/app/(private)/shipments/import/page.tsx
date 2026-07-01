"use client";

import { ChangeEvent, useState } from "react";

import { confirmShipmentsImport, previewShipmentImport } from "@/lib/api";
import { canEditShipments } from "@/lib/permissions";
import { handleApiError } from "@/lib/error-handler";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { ImportConfirmResponse, ImportPreviewV2Response, RowValidationError, ValidatedRowData } from "@/lib/types";

function formatCurrencyBRL(value: number | null | undefined): string {
  if (value === null || value === undefined) return "-";
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
}

function formatDateBR(dateString: string | null | undefined): string {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("pt-BR");
}

function formatUnavailable(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
}

type ImportState =
  | "idle"
  | "file_selected"
  | "preview_loading"
  | "preview_success"
  | "preview_with_errors"
  | "confirm_loading"
  | "confirm_success"
  | "confirm_error"
  | "api_error";

export default function ShipmentsImportPage() {
  const { session } = useAuth();
  const [state, setState] = useState<ImportState>("idle");
  const [error, setError] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [previewResponse, setPreviewResponse] = useState<ImportPreviewV2Response | null>(null);
  const [confirmResponse, setConfirmResponse] = useState<ImportConfirmResponse | null>(null);
  const [layout, setLayout] = useState<"generic" | "braspress_assisted">("generic");

  const editable = canEditShipments(session?.role ?? "auditoria");

  const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selected = event.target.files?.[0];
    if (!selected) {
      setFile(null);
      setFileName("");
      setError("");
      setState("idle");
      return;
    }
    const isCsvByType = selected.type === "text/csv" || selected.type === "application/vnd.ms-excel";
    const isCsvByExtension = selected.name.toLowerCase().endsWith(".csv");
    const isXlsxByType =
      selected.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
      selected.type === "application/vnd.ms-excel.sheet.macroEnabled.12";
    const isXlsxByExtension = selected.name.toLowerCase().endsWith(".xlsx");

    if (isCsvByType || isCsvByExtension || isXlsxByType || isXlsxByExtension) {
      setFile(selected);
      setFileName(selected.name);
      setError("");
      setState("file_selected");
    } else {
      setFile(null);
      setFileName("");
      setError("Por favor, selecione um arquivo CSV ou XLSX válido (.csv, .xlsx).");
      setState("idle");
    }
  };

  const onPreview = async () => {
    if (!session || !file || !editable) return;
    setState("preview_loading");
    setError("");
    try {
      const source = layout === "braspress_assisted" ? "braspress_assisted" : undefined;
      const response = await previewShipmentImport(session.accessToken, file, source);
      setPreviewResponse(response);
      if (response.errors.some((err) => err.is_blocking)) {
        setState("preview_with_errors");
      } else {
        setState("preview_success");
      }
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao fazer preview da importação"));
      setError(err instanceof Error ? err.message : "Erro ao fazer preview da importação");
      setState("api_error");
    }
  };

  const onConfirm = async () => {
    if (!session || !previewResponse?.import_id || !editable) return;
    setState("confirm_loading");
    setError("");
    try {
      const response = await confirmShipmentsImport(session.accessToken, previewResponse.import_id);
      setConfirmResponse(response);
      if (response.status === "completed") {
        setState("confirm_success");
      } else {
        setState("confirm_error");
        setError("Importação falhou. Verifique os erros abaixo.");
      }
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao confirmar importação"));
      setError(err instanceof Error ? err.message : "Erro ao confirmar importação");
      setState("confirm_error");
    }
  };

  const onReset = () => {
    setFile(null);
    setFileName("");
    setPreviewResponse(null);
    setConfirmResponse(null);
    setError("");
    setLayout("generic");
    setState("idle");
  };

  const isLoading = state === "preview_loading" || state === "confirm_loading";
  const hasBlockingErrors = previewResponse?.errors.some((err) => err.is_blocking) ?? false;
  const canConfirm = !hasBlockingErrors && (previewResponse?.valid_rows ?? 0) > 0;

  const inputClass = "mt-1.5 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const selectClass = "mt-1.5 w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800 disabled:opacity-50";
  const btnSecondary = "rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50 disabled:opacity-50";

  return (
    <section className="space-y-5">
      {/* Header */}
      <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Importar Envios</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Upload de arquivo CSV ou XLSX para importação em lote</p>
        </div>
      </header>

      {!editable && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-700">
          Perfil com permissão somente leitura.
        </div>
      )}

      {/* Upload Card - idle state */}
      {state === "idle" && (
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Layout de importação</label>
              <select
                value={layout}
                onChange={(e) => setLayout(e.target.value as "generic" | "braspress_assisted")}
                disabled={!editable || isLoading}
                className={selectClass}
              >
                <option value="generic">Genérico</option>
                <option value="braspress_assisted">Braspress assistido</option>
              </select>
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Arquivo CSV ou XLSX</label>
              <div className="mt-1.5 flex items-center gap-3">
                <label className="flex cursor-pointer items-center gap-2 rounded-lg border border-zinc-200 bg-white px-4 py-2.5 text-sm font-medium text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50">
                  <svg className="h-4 w-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z" />
                  </svg>
                  Escolher arquivo
                  <input
                    type="file"
                    accept=".csv,.xlsx,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    onChange={onFileChange}
                    disabled={!editable || isLoading}
                    className="hidden"
                  />
                </label>
                {fileName && <span className="text-sm text-zinc-500">{fileName}</span>}
              </div>
            </div>
          </div>
          {error && (
            <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}
        </div>
      )}

      {/* File selected */}
      {state === "file_selected" && (
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3 rounded-xl border border-zinc-100 bg-zinc-50 p-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-zinc-100 text-zinc-500">
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-zinc-900">{fileName}</p>
              <p className="text-[11px] text-zinc-500">Arquivo pronto para validação</p>
            </div>
          </div>
          <div className="mt-4 flex gap-2">
            <button onClick={onPreview} disabled={!editable || isLoading} className={btnPrimary}>
              Validar Arquivo
            </button>
            <button onClick={onReset} disabled={isLoading} className={btnSecondary}>
              Cancelar
            </button>
          </div>
        </div>
      )}

      {/* Loading states */}
      {(state === "preview_loading" || state === "confirm_loading") && (
        <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
            <p className="text-sm font-medium text-zinc-600">
              {state === "preview_loading" ? "Validando arquivo..." : "Processando importação..."}
            </p>
          </div>
        </div>
      )}

      {/* Preview results */}
      {(state === "preview_success" || state === "preview_with_errors") && previewResponse && (
        <div className="space-y-4">
          {/* Summary */}
          <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
            <h3 className="text-base font-bold text-zinc-900">Resumo da Validação</h3>
            <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
              <div className="rounded-xl border border-zinc-100 bg-zinc-50 p-4 text-center">
                <p className="text-2xl font-extrabold tabular-nums text-zinc-900">{previewResponse.total_rows}</p>
                <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total de linhas</p>
              </div>
              <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4 text-center">
                <p className="text-2xl font-extrabold tabular-nums text-emerald-600">{previewResponse.valid_rows}</p>
                <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70">Linhas válidas</p>
              </div>
              <div className="rounded-xl border border-red-100 bg-red-50 p-4 text-center">
                <p className="text-2xl font-extrabold tabular-nums text-red-600">{previewResponse.invalid_rows}</p>
                <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Linhas inválidas</p>
              </div>
              <div className="rounded-xl border border-amber-100 bg-amber-50 p-4 text-center">
                <p className="text-2xl font-extrabold tabular-nums text-amber-600">{previewResponse.duplicate_rows}</p>
                <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Duplicatas</p>
              </div>
            </div>
          </div>

          {/* Preview table */}
          {previewResponse.preview_items.length > 0 && (
            <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
              <div className="border-b border-zinc-100 px-6 py-4">
                <h4 className="text-sm font-bold text-zinc-900">Preview (primeiras linhas)</h4>
              </div>
              <div className="max-h-64 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 border-b border-zinc-100 bg-zinc-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Linha</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">NF</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Cliente</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">UF</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Data Coleta</th>
                      <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Valor NF</th>
                      <th className="px-4 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Frete</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.preview_items.map((item: ValidatedRowData) => (
                      <tr key={item.row_number} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-500">{item.row_number}</td>
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-700">{formatUnavailable(item.data.invoice_number)}</td>
                        <td className="px-4 py-2.5 font-medium text-zinc-700">{formatUnavailable(item.data.customer_name)}</td>
                        <td className="px-4 py-2.5 font-mono text-xs font-semibold text-zinc-600">{formatUnavailable(item.data.destination_uf)}</td>
                        <td className="px-4 py-2.5 text-xs text-zinc-500">{formatDateBR(item.data.collection_departure_date)}</td>
                        <td className="px-4 py-2.5 text-right font-mono text-xs font-medium text-zinc-700">{formatCurrencyBRL(item.data.invoice_value)}</td>
                        <td className="px-4 py-2.5 text-right font-mono text-xs font-medium text-zinc-700">{formatCurrencyBRL(item.data.freight_value)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Errors */}
          {previewResponse.errors.length > 0 && (
            <div className="rounded-2xl border border-red-200 bg-red-50/50 shadow-sm">
              <div className="border-b border-red-100 px-6 py-4">
                <h4 className="text-sm font-bold text-red-700">Erros por linha ({previewResponse.errors.length})</h4>
              </div>
              <div className="max-h-64 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 border-b border-red-100 bg-red-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Linha</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Campo</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Mensagem</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Valor</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Severidade</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.errors.map((err: RowValidationError, idx: number) => (
                      <tr key={idx} className="border-b border-red-50">
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-600">{err.row_number}</td>
                        <td className="px-4 py-2.5 font-medium text-zinc-700">{err.field}</td>
                        <td className="px-4 py-2.5 text-zinc-600">{err.message}</td>
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-500">{err.value ?? "-"}</td>
                        <td className="px-4 py-2.5">
                          <span className={`inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold ${
                            err.severity === "error"
                              ? "bg-red-100 text-red-700 ring-1 ring-red-600/20"
                              : "bg-amber-100 text-amber-700 ring-1 ring-amber-600/20"
                          }`}>
                            {err.severity === "error" ? "Erro" : "Aviso"}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Warnings */}
          {previewResponse.warnings.length > 0 && (
            <div className="rounded-2xl border border-amber-200 bg-amber-50/50 shadow-sm">
              <div className="border-b border-amber-100 px-6 py-4">
                <h4 className="text-sm font-bold text-amber-700">Avisos ({previewResponse.warnings.length})</h4>
              </div>
              <div className="max-h-48 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="sticky top-0 border-b border-amber-100 bg-amber-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Linha</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Campo</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Mensagem</th>
                      <th className="px-4 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.warnings.map((err: RowValidationError, idx: number) => (
                      <tr key={idx} className="border-b border-amber-50">
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-600">{err.row_number}</td>
                        <td className="px-4 py-2.5 font-medium text-zinc-700">{err.field}</td>
                        <td className="px-4 py-2.5 text-zinc-600">{err.message}</td>
                        <td className="px-4 py-2.5 font-mono text-xs text-zinc-500">{err.value ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-3">
            {canConfirm && editable && (
              <button onClick={onConfirm} disabled={!editable || isLoading || !canConfirm} className={btnPrimary}>
                Confirmar Importação
              </button>
            )}
            <button onClick={onReset} disabled={isLoading} className={btnSecondary}>
              Cancelar
            </button>
          </div>

          {hasBlockingErrors && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              Existem erros bloqueantes. Corrija o arquivo e tente novamente.
            </div>
          )}

          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}
        </div>
      )}

      {/* Confirm success */}
      {state === "confirm_success" && confirmResponse && (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/50 p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100">
              <svg className="h-5 w-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
            <div>
              <h3 className="text-base font-bold text-emerald-700">Importação Concluída</h3>
              <p className="text-sm text-emerald-600/80">Processamento finalizado com sucesso</p>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div className="rounded-xl bg-white p-4 text-center shadow-sm">
              <p className="text-2xl font-extrabold tabular-nums text-zinc-900">{confirmResponse.total_rows}</p>
              <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Total</p>
            </div>
            <div className="rounded-xl bg-white p-4 text-center shadow-sm">
              <p className="text-2xl font-extrabold tabular-nums text-emerald-600">{confirmResponse.imported_count}</p>
              <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-emerald-600/70">Importados</p>
            </div>
            <div className="rounded-xl bg-white p-4 text-center shadow-sm">
              <p className="text-2xl font-extrabold tabular-nums text-red-600">{confirmResponse.rejected_count}</p>
              <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-red-600/70">Rejeitados</p>
            </div>
            <div className="rounded-xl bg-white p-4 text-center shadow-sm">
              <p className="text-2xl font-extrabold tabular-nums text-amber-600">{confirmResponse.duplicates_count}</p>
              <p className="mt-1 text-[11px] font-semibold uppercase tracking-wide text-amber-600/70">Duplicatas</p>
            </div>
          </div>

          {confirmResponse.created_shipments.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-semibold text-zinc-700">Envios Criados ({confirmResponse.created_shipments.length})</h4>
              <div className="mt-2 flex flex-wrap gap-2">
                {confirmResponse.created_shipments.map((id: number) => (
                  <span key={id} className="inline-flex rounded-lg bg-white px-3 py-1.5 text-xs font-bold text-zinc-700 shadow-sm ring-1 ring-zinc-200">
                    #{id}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="mt-5">
            <button onClick={onReset} className={btnPrimary}>
              Nova Importação
            </button>
          </div>
        </div>
      )}

      {/* Confirm error */}
      {state === "confirm_error" && (
        <div className="rounded-2xl border border-red-200 bg-red-50/50 p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-100">
              <svg className="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div>
              <h3 className="text-base font-bold text-red-700">Importação Falhou</h3>
              {confirmResponse && (
                <p className="text-sm text-red-600/80">
                  {confirmResponse.imported_count} importados, {confirmResponse.rejected_count} rejeitados de {confirmResponse.total_rows}
                </p>
              )}
            </div>
          </div>

          {(confirmResponse?.errors?.length ?? 0) > 0 && (
            <div className="mt-4 max-h-48 overflow-auto rounded-xl bg-white shadow-sm">
              <table className="w-full text-sm">
                <thead className="border-b border-zinc-100 bg-zinc-50">
                  <tr>
                    <th className="px-4 py-2.5 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Linha</th>
                    <th className="px-4 py-2.5 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Campo</th>
                    <th className="px-4 py-2.5 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Mensagem</th>
                  </tr>
                </thead>
                <tbody>
                  {confirmResponse!.errors.map((err, idx: number) => (
                    <tr key={idx} className="border-b border-zinc-50">
                      <td className="px-4 py-2 font-mono text-xs text-zinc-600">{err.row_number}</td>
                      <td className="px-4 py-2 font-medium text-zinc-700">{err.field}</td>
                      <td className="px-4 py-2 text-zinc-600">{err.message}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="mt-5 flex gap-2">
            <button onClick={onReset} className={btnSecondary}>
              Tentar Novamente
            </button>
          </div>

          {error && (
            <div className="mt-3 rounded-lg bg-red-100 px-4 py-3 text-sm font-medium text-red-700">
              {error}
            </div>
          )}
        </div>
      )}

      {/* API error */}
      {state === "api_error" && (
        <div className="rounded-2xl border border-red-200 bg-red-50/50 p-6 shadow-sm">
          <h3 className="text-base font-bold text-red-700">Erro na API</h3>
          <p className="mt-2 text-sm text-red-600/80">{error}</p>
          <div className="mt-4">
            <button onClick={onReset} className={btnSecondary}>
              Tentar Novamente
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
