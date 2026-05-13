"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { apiLogin } from "@/lib/api";
import { parseRoleFromEmail, saveSession } from "@/lib/session";

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
        role: parseRoleFromEmail(email),
      });
      router.push("/");
    } catch {
      setError("Credenciais inválidas. Verifique e tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <form onSubmit={onSubmit} className="w-full max-w-sm rounded border bg-white p-6 shadow-sm">
        <h1 className="text-xl font-semibold">Entrar no painel</h1>
        <p className="mt-1 text-sm text-slate-600">Use suas credenciais para acessar a área privada.</p>

        <label className="mt-4 block text-sm font-medium">E-mail</label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2"
        />

        <label className="mt-4 block text-sm font-medium">Senha</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2"
        />

        {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="mt-5 w-full rounded bg-slate-900 px-3 py-2 text-sm font-medium text-white disabled:opacity-60"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </main>
  );
}
