"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { apiLogin } from "@/lib/api";
import { getPrimaryRole, saveSession } from "@/lib/session";

export function getLoginErrorMessage(): string {
  return "Credenciais invalidas. Verifique e tente novamente.";
}

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
    <div className="flex min-h-screen">
      {/* Left column — Premium brand */}
      <section className="hidden w-1/2 flex-col justify-between bg-black p-10 text-white lg:flex">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-600 shadow-lg shadow-red-600/20">
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7v10l10 5 10-5V7L12 2z" fill="white" fillOpacity="0.95" />
              <path d="M12 2v20M2 7l10 5 10-5M2 17l10-5 10 5" stroke="white" strokeWidth="0.75" strokeOpacity="0.4" />
            </svg>
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight">Ilex</span>
            <span className="ml-1 text-lg font-bold tracking-tight text-red-400">Logística</span>
          </div>
        </div>

        <div className="max-w-md">
          <h2 className="text-4xl font-bold leading-tight tracking-tight">
            Gestão inteligente de <span className="text-red-500">envios</span> e exceções operacionais.
          </h2>
          <p className="mt-4 text-lg text-zinc-400">
            Acompanhe rastreios, identifique atrasos e tome decisões com dados em tempo real.
          </p>

          <div className="mt-10 grid grid-cols-2 gap-4">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-sm">
              <p className="text-3xl font-bold text-red-400">+500</p>
              <p className="mt-1 text-sm text-zinc-400">Envios monitorados</p>
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-sm">
              <p className="text-3xl font-bold text-red-400">98%</p>
              <p className="mt-1 text-sm text-zinc-400">Entregas no prazo</p>
            </div>
          </div>
        </div>

        <p className="text-sm text-zinc-500">© 2026 Ilex Logística. Todos os direitos reservados.</p>
      </section>

      {/* Right column — Login form */}
      <main className="flex w-full flex-col justify-center bg-slate-50 px-6 lg:w-1/2 lg:px-16">
        {/* Mobile logo */}
        <div className="mb-8 flex items-center gap-3 lg:hidden">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-600 shadow-lg shadow-red-600/20">
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7v10l10 5 10-5V7L12 2z" fill="white" fillOpacity="0.95" />
              <path d="M12 2v20M2 7l10 5 10-5M2 17l10-5 10 5" stroke="white" strokeWidth="0.75" strokeOpacity="0.4" />
            </svg>
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight text-zinc-900">Ilex</span>
            <span className="ml-1 text-lg font-bold tracking-tight text-red-600">Logística</span>
          </div>
        </div>

        <div className="mx-auto w-full max-w-md">
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900">Entrar no painel</h1>
          <p className="mt-2 text-zinc-500">Use suas credenciais para acessar a área privada.</p>

          <form onSubmit={onSubmit} className="mt-8 space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-zinc-700">
                E-mail
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-2 w-full rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition-all placeholder:text-zinc-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10"
                placeholder="seu@email.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-zinc-700">
                Senha
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-2 w-full rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-900 outline-none transition-all placeholder:text-zinc-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-red-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-red-600/20 transition-all hover:bg-red-700 disabled:opacity-60"
            >
              {loading ? "Entrando..." : "Entrar"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
