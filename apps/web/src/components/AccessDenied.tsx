"use client";

import Link from "next/link";

interface AccessDeniedProps {
  message?: string;
  showBackButton?: boolean;
}

export function AccessDenied({ message = "Você não tem permissão para acessar esta página.", showBackButton = true }: AccessDeniedProps) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="rounded border bg-white p-8 text-center shadow-sm">
        <h1 className="mb-2 text-2xl font-semibold text-slate-900">Acesso Negado</h1>
        <p className="mb-6 text-slate-600">{message}</p>
        {showBackButton && (
          <Link
            href="/"
            className="inline-block rounded bg-slate-900 px-4 py-2 text-sm text-white hover:bg-slate-800"
          >
            Voltar ao Dashboard
          </Link>
        )}
      </div>
    </div>
  );
}
