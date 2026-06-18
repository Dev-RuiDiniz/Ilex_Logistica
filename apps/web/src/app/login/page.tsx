"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { apiLogin } from "@/lib/api";
import { getPrimaryRole, saveSession } from "@/lib/session";

export function getLoginErrorMessage(): string {
  return "Credenciais invalidas. Verifique e tente novamente.";
}

const highlights = [
  "Priorize alertas críticos sem perder o contexto operacional.",
  "Acompanhe envios, importações e transportadoras em um único fluxo.",
  "Dê visibilidade executiva para exceções, SLA e governança.",
];

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await apiLogin(email, password);
      saveSession({
        email,
        accessToken: result.access_token,
        refreshToken: result.refresh_token,
        role: getPrimaryRole(result.roles),
      });
      router.push("/");
    } catch {
      setError(getLoginErrorMessage());
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative overflow-hidden px-4 py-8 lg:px-8">
      <div className="mx-auto grid min-h-[calc(100vh-4rem)] max-w-[1420px] items-stretch gap-6 lg:grid-cols-[minmax(0,1.15fr)_470px]">
        <section
          data-testid="login-showcase"
          className="relative overflow-hidden rounded-[32px] border border-slate-200/80 bg-[linear-gradient(180deg,rgba(255,255,255,0.98),rgba(247,250,253,0.96))] p-7 text-slate-950 shadow-[0_24px_80px_rgba(16,32,51,0.08)] lg:p-10"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(198,125,47,0.12),transparent_24%),radial-gradient(circle_at_bottom_left,rgba(90,157,197,0.16),transparent_34%)]" />
          <div className="relative flex h-full flex-col justify-between gap-8">
            <div className="space-y-5">
              <div className="inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white/90 px-4 py-2 shadow-sm">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#15314b] text-xs font-black tracking-[0.2em] text-white">
                  IX
                </span>
                <span className="text-xs font-bold uppercase tracking-[0.24em] text-slate-600">
                  Ilex Logistica
                </span>
              </div>

              <div className="space-y-4">
                <p className="text-[0.72rem] font-bold uppercase tracking-[0.28em] text-[#4d6782]">
                  Torre de controle para exceções
                </p>
                <h1 className="max-w-3xl text-4xl font-black tracking-[-0.06em] text-slate-950 md:text-5xl">
                  Priorize alertas, acompanhe envios e reaja mais rápido.
                </h1>
                <p className="max-w-2xl text-base leading-8 text-slate-600">
                  Um painel pensado para operação logística com leitura clara, contexto executivo
                  e decisões mais rápidas em SLA, transportadoras e tratativas.
                </p>
              </div>
            </div>

            <div className="grid gap-4 lg:grid-cols-[1.2fr_0.9fr]">
              <div className="rounded-[28px] border border-slate-200 bg-white/88 p-5 backdrop-blur">
                <p className="mb-4 text-[0.68rem] font-bold uppercase tracking-[0.22em] text-slate-500">
                  O que muda na rotina
                </p>
                <ul className="space-y-3">
                  {highlights.map((item) => (
                    <li key={item} className="flex items-start gap-3 text-sm leading-6 text-slate-700">
                      <span className="mt-1.5 h-2.5 w-2.5 rounded-full bg-amber-300 shadow-[0_0_0_6px_rgba(198,125,47,0.15)]" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-[28px] border border-slate-200 bg-[#f8fbfe] p-5 backdrop-blur">
                <p className="text-[0.68rem] font-bold uppercase tracking-[0.22em] text-slate-500">
                  Leituras essenciais
                </p>
                <div className="mt-4 grid gap-3">
                  <div className="rounded-2xl border border-slate-200 bg-white p-4">
                    <div className="text-[0.7rem] uppercase tracking-[0.2em] text-slate-500">Exceções críticas</div>
                    <div className="mt-2 text-3xl font-black tracking-[-0.05em] text-slate-950">24</div>
                    <div className="mt-1 text-sm text-slate-600">Foco imediato para tratativa</div>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-white p-4">
                    <div className="text-[0.7rem] uppercase tracking-[0.2em] text-slate-500">SLA monitorado</div>
                    <div className="mt-2 text-3xl font-black tracking-[-0.05em] text-slate-950">92,4%</div>
                    <div className="mt-1 text-sm text-slate-600">Clareza para operação e liderança</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section
          data-testid="login-form-panel"
          className="surface-panel flex items-center justify-center px-5 py-7 lg:px-7"
        >
          <form onSubmit={onSubmit} className="w-full max-w-md space-y-5">
            <div className="space-y-3">
              <p className="text-[0.72rem] font-bold uppercase tracking-[0.24em] text-slate-500">
                Acesso seguro
              </p>
              <h2 className="text-3xl font-black tracking-[-0.05em] text-slate-950">
                Entrar no painel
              </h2>
              <p className="text-sm leading-7 text-slate-600">
                Use suas credenciais para acessar a operação privada da Ilex com contexto,
                prioridade e governança.
              </p>
            </div>

            <div className="grid gap-4">
              <div>
                <label className="field-label" htmlFor="email">E-mail</label>
                <input
                  id="email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="field"
                  placeholder="voce@empresa.com"
                />
              </div>

              <div>
                <label className="field-label" htmlFor="password">Senha</label>
                <input
                  id="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="field"
                  placeholder="Digite sua senha"
                />
              </div>
            </div>

            {error && (
              <p className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
                {error}
              </p>
            )}

            <div className="space-y-3">
              <button type="submit" disabled={loading} className="button-primary w-full !py-4 !text-sm">
                {loading ? "Entrando..." : "Entrar na operação"}
              </button>
              <div className="rounded-[20px] border border-slate-200/80 bg-slate-50 px-4 py-3 text-sm text-slate-600">
                Ambientes de desenvolvimento usam os acessos seed documentados no README.
              </div>
            </div>
          </form>
        </section>
      </div>
    </main>
  );
}
