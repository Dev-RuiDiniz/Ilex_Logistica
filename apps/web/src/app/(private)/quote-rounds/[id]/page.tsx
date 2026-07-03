"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { ChangeEvent, useCallback, useEffect, useMemo, useState } from "react";

import { AccessDenied } from "@/components/AccessDenied";
import { useAuth } from "@/features/auth/auth-provider";
import { confirmQuoteImport, getQuoteRound, listCarriers, overrideFreightQuote, previewQuoteImport, saveFreightQuote } from "@/lib/api";
import { canOverrideQuotes, canReadQuotes, canWriteQuotes } from "@/lib/permissions";
import type { Carrier, FreightQuote, QuoteRound } from "@/lib/types";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";

type Draft = { status: string; amount: string; transitDays: string; message: string };

export default function QuoteRoundPage() {
  const params = useParams<{ id: string }>();
  const roundId = Number(params.id);
  const { session } = useAuth();
  const role = session?.role ?? "auditoria";
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();
  const [round, setRound] = useState<QuoteRound | null>(null);
  const [carriers, setCarriers] = useState<Carrier[]>([]);
  const [drafts, setDrafts] = useState<Record<number, Draft>>({});
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [reason, setReason] = useState("");
  const [quoteFile, setQuoteFile] = useState<File | null>(null);

  const carrierNames = useMemo(() => new Map(carriers.map((carrier) => [carrier.id, carrier.name])), [carriers]);
  const load = useCallback(async () => {
    if (!session || !canReadQuotes(role)) return;
    setLoading(true);
    try {
      const [roundData, carrierData] = await Promise.all([getQuoteRound(session.accessToken, roundId), listCarriers(session.accessToken)]);
      setRound(roundData);
      setCarriers(carrierData);
    } catch (caught) {
      const apiError = caught instanceof Error ? caught : new Error("Erro ao carregar cotações");
      handleApiError(apiError); setError(apiError.message);
    } finally { setLoading(false); }
  }, [handleApiError, role, roundId, session]);
  useEffect(() => { queueMicrotask(() => void load()); }, [load]);

  const draftFor = (quote: FreightQuote): Draft => drafts[quote.id] ?? { status: quote.status === "pending" ? "quoted" : quote.status, amount: quote.amount ?? "", transitDays: quote.transit_days?.toString() ?? "", message: quote.message ?? "" };
  const updateDraft = (quote: FreightQuote, patch: Partial<Draft>) => setDrafts((current) => ({ ...current, [quote.id]: { ...draftFor(quote), ...patch } }));
  const save = async (quote: FreightQuote) => {
    if (!session) return; const draft = draftFor(quote); setBusy(quote.id); setError("");
    try { setRound(await saveFreightQuote(session.accessToken, roundId, { carrier_id: quote.carrier_id, status: draft.status, amount: draft.status === "quoted" ? draft.amount : undefined, transit_days: draft.transitDays ? Number(draft.transitDays) : undefined, message: draft.message || undefined })); }
    catch (caught) { const apiError = caught instanceof Error ? caught : new Error("Erro ao salvar cotação"); handleApiError(apiError); setError(apiError.message); }
    finally { setBusy(null); }
  };
  const override = async (quote: FreightQuote) => {
    if (!session) return; setBusy(quote.id);
    try { setRound(await overrideFreightQuote(session.accessToken, roundId, quote.id, reason)); setReason(""); }
    catch (caught) { const apiError = caught instanceof Error ? caught : new Error("Erro no override"); handleApiError(apiError); setError(apiError.message); }
    finally { setBusy(null); }
  };
  const importCsv = async () => {
    if (!session || !quoteFile) return; setBusy(-1);
    try { const preview = await previewQuoteImport(session.accessToken, roundId, quoteFile); if (preview.valid_rows === 0) throw new Error("CSV sem cotações válidas"); setRound(await confirmQuoteImport(session.accessToken, roundId, preview.import_id)); setQuoteFile(null); }
    catch (caught) { const apiError = caught instanceof Error ? caught : new Error("Erro ao importar cotações"); handleApiError(apiError); setError(apiError.message); }
    finally { setBusy(null); }
  };

  if (!canReadQuotes(role) || accessDenied) return <AccessDenied message={accessDeniedMessage || "Sem acesso às cotações."} />;
  if (loading) return <p role="status" className="p-8 text-sm text-zinc-500">Carregando rodada...</p>;
  if (!round) return <div role="alert" className="rounded-xl bg-red-50 p-4 text-red-700">{error || "Rodada não encontrada."}</div>;

  return <section className="space-y-5"><header><Link href={`/orders/${round.order_id}`} className="text-sm text-red-700 hover:underline">← Pedido</Link><h1 className="mt-2 text-2xl font-extrabold text-zinc-900">Comparação · rodada {round.sequence}</h1><p className="text-sm text-zinc-500">Status {round.status} · válida até {new Date(round.expires_at).toLocaleString("pt-BR")}</p></header>
    {error && <div role="alert" className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
    {canWriteQuotes(role) && <div className="flex flex-col gap-3 rounded-2xl border border-zinc-200 bg-white p-4 sm:flex-row sm:items-end"><label className="flex-1 text-sm font-medium">Importar cotações CSV<input type="file" accept=".csv" onChange={(event: ChangeEvent<HTMLInputElement>) => setQuoteFile(event.target.files?.[0] ?? null)} className="mt-1 block w-full rounded-lg border p-2" /></label><button onClick={importCsv} disabled={!quoteFile || busy !== null} className="rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50">Importar</button></div>}
    <div className="grid gap-4">{round.quotes.map((quote) => { const draft = draftFor(quote); const recommended = round.recommended_quote_id === quote.id; const selected = round.selected_quote_id === quote.id; return <article key={quote.id} className={`rounded-2xl border bg-white p-5 shadow-sm ${recommended ? "border-emerald-400 ring-2 ring-emerald-100" : "border-zinc-200"}`}><div className="flex flex-wrap items-start justify-between gap-3"><div><h2 className="font-bold text-zinc-900">{carrierNames.get(quote.carrier_id) ?? `Transportadora ${quote.carrier_id}`}</h2><p className="mt-1 text-sm text-zinc-500">{quote.status}{quote.message ? ` · ${quote.message}` : ""}</p></div><div className="flex gap-2">{recommended && <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-bold text-emerald-800">Recomendada</span>}{selected && <span className="rounded-full bg-red-100 px-2.5 py-1 text-xs font-bold text-red-800">Selecionada</span>}</div></div>
      {canWriteQuotes(role) && <div className="mt-4 grid gap-3 sm:grid-cols-4"><label className="text-xs font-semibold text-zinc-600">Status<select value={draft.status} onChange={(event) => updateDraft(quote, { status: event.target.value })} className="mt-1 w-full rounded-lg border p-2 text-sm"><option value="quoted">Cotada</option><option value="unavailable">Indisponível</option><option value="error">Erro</option></select></label><label className="text-xs font-semibold text-zinc-600">Valor<input value={draft.amount} disabled={draft.status !== "quoted"} onChange={(event) => updateDraft(quote, { amount: event.target.value })} className="mt-1 w-full rounded-lg border p-2 text-sm" inputMode="decimal" /></label><label className="text-xs font-semibold text-zinc-600">Prazo (dias)<input value={draft.transitDays} onChange={(event) => updateDraft(quote, { transitDays: event.target.value })} className="mt-1 w-full rounded-lg border p-2 text-sm" inputMode="numeric" /></label><button onClick={() => save(quote)} disabled={busy !== null} className="self-end rounded-lg border border-zinc-300 px-3 py-2 text-sm font-semibold disabled:opacity-50">Salvar</button></div>}
      {canOverrideQuotes(role) && quote.status === "quoted" && <div className="mt-4 flex flex-col gap-2 border-t border-zinc-100 pt-4 sm:flex-row"><label className="sr-only" htmlFor={`reason-${quote.id}`}>Justificativa do override</label><input id={`reason-${quote.id}`} value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Justificativa obrigatória (mín. 10 caracteres)" className="flex-1 rounded-lg border px-3 py-2 text-sm" /><button onClick={() => override(quote)} disabled={reason.trim().length < 10 || busy !== null} className="rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white disabled:opacity-50">Selecionar com justificativa</button></div>}</article>; })}</div>
    <p className="sr-only" aria-live="polite">{busy !== null ? "Operação em andamento" : ""}</p>
  </section>;
}
