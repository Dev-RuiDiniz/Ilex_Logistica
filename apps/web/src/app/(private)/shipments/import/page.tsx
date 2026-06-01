"use client";

import { ChangeEvent, useState } from "react";

import { confirmShipmentsImport, uploadShipmentsCsv } from "@/lib/api";
import { canEditShipments } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";
import type { CSVRowError, UploadResponse, ImportConfirmResponse } from "@/lib/types";

type ImportState = "idle" | "uploading" | "validated" | "importing" | "completed" | "failed";

export default function ShipmentsImportPage() {
  const { session } = useAuth();
  const [state, setState] = useState<ImportState>("idle");
  const [error, setError] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploadResponse, setUploadResponse] = useState<UploadResponse | null>(null);
  const [importResponse, setImportResponse] = useState<ImportConfirmResponse | null>(null);
  const [fileName, setFileName] = useState("");

  const editable = canEditShipments(session?.role ?? "auditoria");

  const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selected = event.target.files?.[0];
    if (!selected) {
      setFile(null);
      setFileName("");
      setError("");
      return;
    }

    // Validar por MIME type e extensão
    const isCsvByType = selected.type === "text/csv" || selected.type === "application/vnd.ms-excel";
    const isCsvByExtension = selected.name.toLowerCase().endsWith(".csv");

    if (isCsvByType || isCsvByExtension) {
      setFile(selected);
      setFileName(selected.name);
      setError("");
    } else {
      setFile(null);
      setFileName("");
      setError("Por favor, selecione um arquivo CSV válido (.csv).");
    }
  };

  const onUpload = async () => {
    if (!session || !file || !editable) return;
    setState("uploading");
    setError("");
    try {
      const response = await uploadShipmentsCsv(session.accessToken, file);
      setUploadResponse(response);
      if (response.status === "validated") {
        setState("validated");
      } else {
        setState("failed");
        if (response.errors.length > 0) {
          setError("Validação falhou. Verifique os erros abaixo.");
        } else {
          setError("Falha na validação do arquivo CSV.");
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Falha ao fazer upload do arquivo CSV.";
      setError(errorMessage);
      setState("failed");
    }
  };

  const onConfirm = async () => {
    if (!session || !uploadResponse?.import_id || !editable) return;
    setState("importing");
    setError("");
    try {
      const response = await confirmShipmentsImport(session.accessToken, uploadResponse.import_id);
      setImportResponse(response);
      if (response.status === "completed") {
        setState("completed");
      } else {
        setState("failed");
        if (response.errors.length > 0) {
          setError("Importação falhou. Verifique os erros abaixo.");
        } else {
          setError("Falha ao confirmar importação.");
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Falha ao confirmar importação.";
      setError(errorMessage);
      setState("failed");
    }
  };

  const onReset = () => {
    setFile(null);
    setFileName("");
    setUploadResponse(null);
    setImportResponse(null);
    setError("");
    setState("idle");
  };

  const isUploadingOrImporting = state === "uploading" || state === "importing";

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Importar Envios</h2>
        <p className="text-sm text-slate-600">Upload de arquivo CSV para importação em lote de envios.</p>
      </header>

      {!editable && <p className="rounded bg-amber-50 px-3 py-2 text-sm text-amber-700">Perfil com permissão somente leitura.</p>}

      {state === "idle" && (
        <div className="rounded border bg-white p-4">
          <label className="block text-sm font-medium">Arquivo CSV</label>
          <input
            type="file"
            accept=".csv,text/csv"
            onChange={onFileChange}
            disabled={!editable || isUploadingOrImporting}
            className="mt-1 w-full rounded border px-3 py-2 disabled:opacity-60"
          />
          {fileName && <p className="mt-1 text-sm text-slate-600">Arquivo selecionado: {fileName}</p>}
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          {file && (
            <div className="mt-4 flex gap-2">
              <button
                onClick={onUpload}
                disabled={!editable || isUploadingOrImporting}
                className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
              >
                Fazer Upload
              </button>
              <button
                onClick={onReset}
                disabled={isUploadingOrImporting}
                className="rounded border px-4 py-2 text-sm disabled:opacity-60"
              >
                Limpar
              </button>
            </div>
          )}
        </div>
      )}

      {state === "uploading" && (
        <div className="rounded border bg-white p-4">
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
            <p className="text-sm text-slate-600">Fazendo upload do arquivo...</p>
          </div>
        </div>
      )}

      {(state === "validated" || state === "failed") && uploadResponse && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold">Resumo da Validação</h3>
            <div className="mt-2 grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-slate-600">Total de linhas:</span>
                <span className="ml-2 font-semibold">{uploadResponse.total_rows}</span>
              </div>
              <div>
                <span className="text-slate-600">Linhas válidas:</span>
                <span className="ml-2 font-semibold text-green-700">{uploadResponse.valid_rows}</span>
              </div>
              <div>
                <span className="text-slate-600">Linhas inválidas:</span>
                <span className="ml-2 font-semibold text-red-700">{uploadResponse.invalid_rows}</span>
              </div>
            </div>
          </div>

          {uploadResponse.errors.length > 0 && (
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
                    </tr>
                  </thead>
                  <tbody>
                    {uploadResponse.errors.map((err: CSVRowError, idx: number) => (
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

          {state === "validated" && uploadResponse.valid_rows > 0 && editable && (
            <div className="flex gap-2">
              <button
                onClick={onConfirm}
                disabled={!editable || isUploadingOrImporting}
                className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
              >
                Confirmar Importação
              </button>
              <button
                onClick={onReset}
                disabled={isUploadingOrImporting}
                className="rounded border px-4 py-2 text-sm disabled:opacity-60"
              >
                Cancelar
              </button>
            </div>
          )}

          {state === "failed" && (
            <div className="flex gap-2">
              <button
                onClick={onReset}
                disabled={isUploadingOrImporting}
                className="rounded border px-4 py-2 text-sm disabled:opacity-60"
              >
                Tentar Novamente
              </button>
            </div>
          )}

          {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
        </div>
      )}

      {state === "importing" && (
        <div className="rounded border bg-white p-4">
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent" />
            <p className="text-sm text-slate-600">Processando importação...</p>
          </div>
        </div>
      )}

      {state === "completed" && importResponse && (
        <div className="rounded border bg-white p-4 space-y-4">
          <div>
            <h3 className="text-base font-semibold text-green-700">Importação Concluída</h3>
            <div className="mt-2 grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-slate-600">Total de linhas:</span>
                <span className="ml-2 font-semibold">{importResponse.total_rows}</span>
              </div>
              <div>
                <span className="text-slate-600">Importados:</span>
                <span className="ml-2 font-semibold text-green-700">{importResponse.imported_count}</span>
              </div>
              <div>
                <span className="text-slate-600">Rejeitados:</span>
                <span className="ml-2 font-semibold text-red-700">{importResponse.rejected_count}</span>
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <button
              onClick={onReset}
              className="rounded bg-slate-900 px-4 py-2 text-sm text-white"
            >
              Nova Importação
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
