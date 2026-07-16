"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import {
  canReadAudit,
  canReadCarriers,
  canReadOrders,
  canReadReports,
  canReadShipments,
  canReadUsers,
  canWriteImports,
} from "@/lib/permissions";
import type { UserRole } from "@/lib/types";
import { useAuth } from "@/features/auth/auth-provider";

type NavItem = {
  href: string;
  label: string;
  visible: boolean;
};

type NavSection = {
  heading: string;
  items: NavItem[];
};

export function getRoleUiLabel(role: UserRole): string {
  return canReadCarriers(role) ? "(acesso)" : "(sem acesso)";
}

function getRoleBadgeLabel(role: UserRole): string {
  const labels: Record<UserRole, string> = {
    admin: "Controle total",
    manager: "Gestão ampliada",
    operator: "Execução focada",
    viewer: "Leitura operacional",
    logistica: "Operação logística",
    gestor: "Visão gerencial",
    auditoria: "Governança e trilha",
  };
  return labels[role];
}

export function getNavigationSections(role: UserRole): NavSection[] {
  return [
    {
      heading: "Visão geral",
      items: [
        { href: "/", label: "Dashboard", visible: true },
        { href: "/reports/daily", label: "Relatório Diário", visible: canReadReports(role) },
      ],
    },
    {
      heading: "Operação",
      items: [
        { href: "/shipments", label: "Envios", visible: canReadShipments(role) },
        { href: "/shipments/import", label: "Importar Envios", visible: canWriteImports(role) },
        { href: "/carriers", label: "Transportadoras", visible: canReadCarriers(role) },
        { href: "/orders", label: "Pedidos e Cotações", visible: canReadOrders(role) },
      ],
    },
    {
      heading: "Governança",
      items: [
        { href: "/audit", label: "Auditoria", visible: canReadAudit(role) },
        { href: "/users", label: "Usuários", visible: canReadUsers(role) },
      ],
    },
  ].filter((section) => section.items.some((item) => item.visible));
}

function getPageContext(pathname: string): { title: string; note: string } {
  if (pathname.startsWith("/shipments")) {
    return {
      title: "Monitoramento operacional",
      note: "Priorize pendências, filtre criticidades e acompanhe janelas de entrega.",
    };
  }

  if (pathname.startsWith("/carriers")) {
    return {
      title: "Rede de transportadoras",
      note: "Mantenha parceiros, códigos e integrações em ordem com leitura rápida do status.",
    };
  }

  if (pathname.startsWith("/reports")) {
    return {
      title: "Leitura executiva diária",
      note: "Consolide operação, alertas e exceções com visão objetiva para decisão.",
    };
  }

  if (pathname.startsWith("/audit")) {
    return {
      title: "Trilha de governança",
      note: "Acompanhe alterações, eventos e rastreabilidade da operação.",
    };
  }

  if (pathname.startsWith("/users")) {
    return {
      title: "Acesso e perfis",
      note: "Controle papéis, responsabilidades e segurança do painel.",
    };
  }

  return {
    title: "Centro de comando Ilex",
    note: "Uma visão clara para agir rápido em entregas, transportadoras e exceções.",
  };
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const { session, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const role = session?.role ?? "auditoria";
  const navSections = getNavigationSections(role);
  const pageContext = getPageContext(pathname);

  const onLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="app-shell-root text-slate-950">
      <header className="app-shell-header">
        <div className="mx-auto flex max-w-[1440px] flex-col gap-4 px-4 py-4 lg:px-8">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-white/8 text-lg font-black tracking-tight text-white">
                IX
              </div>
              <div className="space-y-1">
                <p className="text-[0.7rem] font-bold uppercase tracking-[0.28em] text-slate-200/90">
                  Ilex Logistica
                </p>
                <h1 className="text-xl font-extrabold tracking-[-0.04em] text-white">
                  Exceções com inteligência
                </h1>
                <p className="max-w-2xl text-sm text-slate-200/95">{pageContext.note}</p>
              </div>
            </div>

            <div className="flex flex-col gap-3 lg:items-end">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-full border border-white/10 bg-white/6 px-3 py-1.5 text-xs font-semibold text-slate-100">
                  {getRoleBadgeLabel(role)}
                </span>
                <span className="rounded-full border border-white/10 bg-white/6 px-3 py-1.5 text-xs font-semibold text-slate-200">
                  {session?.email}
                </span>
                <button onClick={onLogout} className="button-secondary !border-white/10 !bg-white !px-4 !py-2 !text-xs !font-bold">
                  Sair
                </button>
              </div>
              <p className="text-xs uppercase tracking-[0.16em] text-slate-300">
                {pageContext.title}
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="app-shell-main mx-auto grid max-w-[1440px] gap-5 px-4 py-5 lg:grid-cols-[300px_minmax(0,1fr)] lg:px-8 lg:py-8">
        <aside className="app-shell-sidebar rounded-[28px] p-4 lg:p-5">
          <div className="mb-5 rounded-[22px] border border-white/8 bg-white/4 p-4">
            <p className="text-[0.68rem] uppercase tracking-[0.24em] text-slate-300">Controle da operação</p>
            <p className="mt-2 text-sm leading-6 text-slate-100">
              Navegue por prioridade, monitore a rede e mantenha contexto claro em cada fluxo.
            </p>
          </div>

          <nav className="space-y-5">
            {navSections.map((section) => (
              <div key={section.heading}>
                <p className="mb-2 px-3 text-[0.7rem] font-bold uppercase tracking-[0.22em] text-slate-300">
                  {section.heading}
                </p>
                <div className="space-y-1.5">
                  {section.items
                    .filter((item) => item.visible)
                    .map((item) => {
                      const active = item.href === "/"
                        ? pathname === "/"
                        : pathname.startsWith(item.href);

                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          className={`group flex items-center justify-between rounded-2xl px-3 py-3 text-sm font-semibold ${
                            active
                              ? "bg-white text-slate-950 shadow-lg"
                              : "text-slate-100 hover:bg-white/8 hover:text-white"
                          }`}
                        >
                          <span>{item.label}</span>
                          <span className={`text-[0.68rem] uppercase tracking-[0.16em] ${active ? "text-slate-600" : "text-slate-300 group-hover:text-slate-200"}`}>
                            abrir
                          </span>
                        </Link>
                      );
                    })}
                </div>
              </div>
            ))}
          </nav>
        </aside>

        <main className="space-y-5">{children}</main>
      </div>
    </div>
  );
}
