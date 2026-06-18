"use client";

import Link from "next/link";

interface AccessDeniedProps {
  message?: string;
  showBackButton?: boolean;
}

export function AccessDenied({ message = "Você não tem permissão para acessar esta página.", showBackButton = true }: AccessDeniedProps) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="surface-panel max-w-xl px-8 py-10 text-center">
        <p className="page-kicker !text-slate-600">Governança</p>
        <h1 className="mt-3 text-3xl font-black tracking-[-0.05em] text-slate-950">Acesso Negado</h1>
        <p className="mx-auto mt-3 max-w-md text-sm leading-7 text-slate-700">{message}</p>
        {showBackButton && (
          <Link
            href="/"
            className="button-primary mt-6 inline-flex"
          >
            Voltar ao Dashboard
          </Link>
        )}
      </div>
    </div>
  );
}
