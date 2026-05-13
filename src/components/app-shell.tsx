"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { canEditCarriers } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { session, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const onLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <h1 className="text-lg font-semibold">Ilex Logística Admin</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-slate-600">{session?.email}</span>
            <button
              onClick={onLogout}
              className="rounded bg-slate-900 px-3 py-1.5 text-sm text-white"
            >
              Sair
            </button>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-6xl grid-cols-1 gap-4 p-6 md:grid-cols-[220px_1fr]">
        <aside className="rounded border bg-white p-3">
          <nav className="space-y-1">
            <Link
              href="/"
              className={`block rounded px-3 py-2 text-sm ${pathname === "/" ? "bg-slate-900 text-white" : "hover:bg-slate-100"}`}
            >
              Dashboard
            </Link>
            <Link
              href="/carriers"
              className={`block rounded px-3 py-2 text-sm ${pathname.startsWith("/carriers") ? "bg-slate-900 text-white" : "hover:bg-slate-100"}`}
            >
              Transportadoras
            </Link>
            <p className="pt-2 text-xs text-slate-500">
              Perfil: {session?.role} {canEditCarriers(session?.role ?? "auditoria") ? "(edição)" : "(somente leitura)"}
            </p>
          </nav>
        </aside>
        <main className="rounded border bg-white p-4">{children}</main>
      </div>
    </div>
  );
}
