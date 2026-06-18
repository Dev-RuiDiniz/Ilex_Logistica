"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { AppShell } from "@/components/app-shell";
import { AuthProvider, useAuth } from "@/features/auth/auth-provider";

function Guard({ children }: { children: React.ReactNode }) {
  const { session } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!session) {
      router.replace("/login");
    }
  }, [router, session]);

  if (!session) {
    return (
      <div className="app-shell-root flex min-h-screen items-center justify-center px-4">
        <div className="surface-panel max-w-md px-8 py-8 text-center">
          <p className="page-kicker !text-slate-500">Segurança</p>
          <h2 className="mt-3 text-2xl font-black tracking-[-0.05em] text-slate-950">
            Validando sessão...
          </h2>
          <p className="mt-3 text-sm leading-7 text-slate-600">
            Aguarde enquanto confirmamos seu acesso ao centro de comando.
          </p>
        </div>
      </div>
    );
  }
  return <AppShell>{children}</AppShell>;
}

export default function PrivateLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <Guard>{children}</Guard>
    </AuthProvider>
  );
}
