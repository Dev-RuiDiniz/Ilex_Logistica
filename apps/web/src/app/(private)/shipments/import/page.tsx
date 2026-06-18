"use client";

import { ChangeEvent, useState } from "react";

import { confirmShipmentsImport, previewShipmentImport } from "@/lib/api";
import { canEditShipments } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { ImportConfirmResponse, ImportPreviewV2Response, RowValidationError, ValidatedRowData } from "@/lib/types";

// Formatting helpers
function formatCurrencyBRL(value: number | null | undefined): string {
  if (value === null || value === undefined) return "-";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
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
  const [layout, setLayout] = useState<"generic" | "braspress_assisted">("generic"); // BETA-012C: Layout selector
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

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

    // Validar por MIME type e extensão - aceitar CSV e XLSX
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
    setLayout("generic"); // BETA-012C: Reset layout
    setState("idle");
  };

  const isLoading = state === "preview_loading" || state === "confirm_loading";
  const hasBlockingErrors = previewResponse?.errors.some((err) => err.is_blocking) ?? false;
  const canConfirm = !hasBlockingErrors && (previewResponse?.valid_rows ?? 0) > 0;

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Importar Envios</h2>
        <p className="text-sm text-slate-700">Upload de arquivo CSV ou XLSX para importação em lote de envios.</p>
      </header>

      {!editable && <p className="rounded bg-amber-50 px-3 py-2 text-sm text-amber-700">Perfil com permissão somente leitura.</p>}

      {state === "idle" && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium">Layout de importação</label>
            <select
              value={layout}
              onChange={(e) => setLayout(e.target.value as "generic" | "braspress_assisted")}
              disabled={!editable || isLoading}
              className="mt-1 w-full rounded border px-3 py-2 disabled:opacity-60"
            >
              <option value="generic">Genérico</option>
              <option value="braspress_assisted">Braspress assistido</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium">Arquivo CSV ou XLSX</label>
            <input
              type="file"
              accept=".csv,.xlsx,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              onChange={onFileChange}
              disabled={!editable || isLoading}
              className="mt-1 w-full rounded border px-3 py-2 disabled:opacity-60"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
      )}

      {state === "file_selected" && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <p className="text-sm text-slate-700">Arquivo selecionado: {fileName}</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onPreview}
              disabled={!editable || isLoading}
              className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
            >
              Validar Arquivo
            </button>
            <button
              onClick={onReset}
              disabled={isLoading}
              className="rounded border px-4 py-2 text-sm disabled:opacity-60"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      {state === "preview_loading" && (
        <div className="rounded border bg-white p-4">
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
            <p className="text-sm text-slate-700">Validando arquivo...</p>
          </div>
        </div>
      )}

      {(state === "preview_success" || state === "preview_with_errors") && previewResponse && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold">Resumo da Validação</h3>
            <div className="mt-2 grid grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-slate-700">Total de linhas:</span>
                <span className="ml-2 font-semibold">{previewResponse.total_rows}</span>
              </div>
              <div>
                <span className="text-slate-700">Linhas válidas:</span>
                <span className="ml-2 font-semibold text-green-700">{previewResponse.valid_rows}</span>
              </div>
              <div>
                <span className="text-slate-700">Linhas inválidas:</span>
                <span className="ml-2 font-semibold text-red-700">{previewResponse.invalid_rows}</span>
              </div>
              <div>
                <span className="text-slate-700">Duplicatas:</span>
                <span className="ml-2 font-semibold text-amber-700">{previewResponse.duplicate_rows}</span>
              </div>
            </div>
          </div>

          {/* Preview table with fiscal/financial fields */}
          {previewResponse.preview_items.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold">Preview (primeiras linhas)</h4>
              <div className="mt-2 max-h-64 overflow-y-auto rounded border">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-left sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Linha</th>
                      <th className="px-3 py-2">NF</th>
                      <th className="px-3 py-2">Cliente</th>
                      <th className="px-3 py-2">UF</th>
                      <th className="px-3 py-2">Data Coleta</th>
                      <th className="px-3 py-2">Valor NF</th>
                      <th className="px-3 py-2">Valor Frete</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.preview_items.map((item: ValidatedRowData) => (
                      <tr key={item.row_number} className="border-t">
                        <td className="px-3 py-2">{item.row_number}</td>
                        <td className="px-3 py-2">{formatUnavailable(item.data.invoice_number)}</td>
                        <td className="px-3 py-2">{formatUnavailable(item.data.customer_name)}</td>
                        <td className="px-3 py-2">{formatUnavailable(item.data.destination_uf)}</td>
                        <td className="px-3 py-2">{formatDateBR(item.data.collection_departure_date)}</td>
                        <td className="px-3 py-2">{formatCurrencyBRL(item.data.invoice_value)}</td>
                        <td className="px-3 py-2">{formatCurrencyBRL(item.data.freight_value)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Errors by line */}
          {previewResponse.errors.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold">Erros por linha</h4>
              <div className="mt-2 max-h-64 overflow-y-auto rounded border">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-left sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Linha</th>
                      <th className="px-3 py-2">Campo</th>
                      <th className="px-3 py-2">Mensagem</th>
                      <th className="px-3 py-2">Valor</th>
                      <th className="px-3 py-2">Severidade</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.errors.map((err: RowValidationError, idx: number) => (
                      <tr key={idx} className="border-t">
                        <td className="px-3 py-2">{err.row_number}</td>
                        <td className="px-3 py-2">{err.field}</td>
                        <td className="px-3 py-2">{err.message}</td>
                        <td className="px-3 py-2">{err.value ?? "-"}</td>
                        <td className="px-3 py-2">
                          <span
                            className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${
                              err.severity === "error"
                                ? "bg-red-100 text-red-800"
                                : "bg-amber-100 text-amber-800"
                            }`}
                          >
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

          {/* Warnings separately */}
          {previewResponse.warnings.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold">Avisos</h4>
              <div className="mt-2 max-h-64 overflow-y-auto rounded border">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-left sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Linha</th>
                      <th className="px-3 py-2">Campo</th>
                      <th className="px-3 py-2">Mensagem</th>
                      <th className="px-3 py-2">Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewResponse.warnings.map((err: RowValidationError, idx: number) => (
                      <tr key={idx} className="border-t">
                        <td className="px-3 py-2">{err.row_number}</td>
                        <td className="px-3 py-2">{err.field}</td>
                        <td className="px-3 py-2">{err.message}</td>
                        <td className="px-3 py-2">{err.value ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-2">
            {canConfirm && editable && (
              <button
                onClick={onConfirm}
                disabled={!editable || isLoading || !canConfirm}
                className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
              >
                Confirmar Importação
              </button>
            )}
            <button onClick={onReset} disabled={isLoading} className="rounded border px-4 py-2 text-sm disabled:opacity-60">
              Cancelar
            </button>
          </div>

          {hasBlockingErrors && (
            <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">
              Existem erros bloqueantes. Corrija o arquivo e tente novamente.
            </p>
          )}

          {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        </div>
      )}

      {state === "confirm_loading" && (
        <div className="rounded border bg-white p-4">
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
            <p className="text-sm text-slate-700">Processando importação...</p>
          </div>
        </div>
      )}

      {state === "confirm_success" && confirmResponse && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold text-green-700">Importação Concluída</h3>
            <div className="mt-2 grid grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-slate-700">Total de linhas:</span>
                <span className="ml-2 font-semibold">{confirmResponse.total_rows}</span>
              </div>
              <div>
                <span className="text-slate-700">Importados:</span>
                <span className="ml-2 font-semibold text-green-700">{confirmResponse.imported_count}</span>
              </div>
              <div>
                <span className="text-slate-700">Rejeitados:</span>
                <span className="ml-2 font-semibold text-red-700">{confirmResponse.rejected_count}</span>
              </div>
              <div>
                <span className="text-slate-700">Duplicatas:</span>
                <span className="ml-2 font-semibold text-amber-700">{confirmResponse.duplicates_count}</span>
              </div>
            </div>
          </div>

          {confirmResponse.created_shipments.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold">Shipments Criados ({confirmResponse.created_shipments.length})</h4>
              <div className="mt-2 max-h-32 overflow-y-auto rounded border p-2 text-sm">
                {confirmResponse.created_shipments.map((id: number) => (
                  <span key={id} className="inline-block mr-2 mb-1">
                    <span className="rounded bg-slate-100 px-2 py-1">#{id}</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <button onClick={onReset} className="rounded bg-slate-900 px-4 py-2 text-sm text-white">
              Nova Importação
            </button>
          </div>
        </div>
      )}

      {state === "confirm_error" && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold text-red-700">Importação Falhou</h3>
            {confirmResponse && (
              <div className="mt-2 grid grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-slate-700">Total de linhas:</span>
                  <span className="ml-2 font-semibold">{confirmResponse.total_rows}</span>
                </div>
                <div>
                  <span className="text-slate-700">Importados:</span>
                  <span className="ml-2 font-semibold text-green-700">{confirmResponse.imported_count}</span>
                </div>
                <div>
                  <span className="text-slate-700">Rejeitados:</span>
                  <span className="ml-2 font-semibold text-red-700">{confirmResponse.rejected_count}</span>
                </div>
                <div>
                  <span className="text-slate-700">Duplicatas:</span>
                  <span className="ml-2 font-semibold text-amber-700">{confirmResponse.duplicates_count}</span>
                </div>
              </div>
            )}
          </div>

          {(confirmResponse?.errors?.length ?? 0) > 0 && (
            <div>
              <h4 className="text-sm font-semibold">Erros</h4>
              <div className="mt-2 max-h-64 overflow-y-auto rounded border">
                <table className="w-full text-sm">
                  <thead className="bg-slate-100 text-left sticky top-0">
                    <tr>
                      <th className="px-3 py-2">Linha</th>
                      <th className="px-3 py-2">Campo</th>
                      <th className="px-3 py-2">Mensagem</th>
                      <th className="px-3 py-2">Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    {confirmResponse!.errors.map((err, idx: number) => (
                      <tr key={idx} className="border-t">
                        <td className="px-3 py-2">{err.row_number}</td>
                        <td className="px-3 py-2">{err.field}</td>
                        <td className="px-3 py-2">{err.message}</td>
                        <td className="px-3 py-2">{err.value ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <button onClick={onReset} className="rounded border px-4 py-2 text-sm">
              Tentar Novamente
            </button>
          </div>

          {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        </div>
      )}

      {state === "api_error" && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold text-red-700">Erro na API</h3>
          </div>

          <div className="flex gap-2">
            <button onClick={onReset} className="rounded border px-4 py-2 text-sm">
              Tentar Novamente
            </button>
          </div>

          {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        </div>
      )}
    </section>
  );
}
