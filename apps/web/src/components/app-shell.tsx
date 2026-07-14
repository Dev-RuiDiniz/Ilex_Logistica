"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import {
  canReadAudit,
  canReadCarriers,
  canReadReports,
  canReadOrders,
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
<<<<<<< HEAD
    <div className="flex min-h-screen bg-white">
      {/* Sidebar — Black */}
      <aside className="hidden w-64 flex-shrink-0 flex-col border-r border-white/[0.08] bg-black lg:flex">
        {/* Logo */}
        <div className="flex h-16 items-center gap-3 border-b border-white/[0.08] px-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-red-600 shadow-lg shadow-red-600/20">
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7v10l10 5 10-5V7L12 2z" fill="white" fillOpacity="0.95" />
              <path d="M12 2v20M2 7l10 5 10-5M2 17l10-5 10 5" stroke="white" strokeWidth="0.75" strokeOpacity="0.4" />
            </svg>
          </div>
          <div>
            <span className="text-[15px] font-bold tracking-tight text-white">Ilex</span>
            <span className="ml-1 text-[15px] font-bold tracking-tight text-red-400">Logística</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-0.5 p-4">
          <p className="mb-2 px-3 text-[10px] font-bold uppercase tracking-widest text-zinc-400">Menu</p>
          <SidebarLink href="/" active={pathname === "/"}>
            <IconDashboard />
            Dashboard
          </SidebarLink>
          {canReadShipments(role) && (
            <SidebarLink href="/shipments" active={pathname.startsWith("/shipments")}>
              <IconShipment />
              Envios
            </SidebarLink>
          )}
          {canWriteImports(role) && (
            <SidebarLink href="/shipments/import" active={pathname === "/shipments/import"}>
              <IconImport />
              Importar Envios
            </SidebarLink>
          )}
          {canReadCarriers(role) && (
            <SidebarLink href="/carriers" active={pathname.startsWith("/carriers")}>
              <IconCarrier />
              Transportadoras
            </SidebarLink>
          )}
          {canReadOrders(role) && (
            <SidebarLink href="/orders" active={pathname.startsWith("/orders") || pathname.startsWith("/quote-rounds")}>
              <IconShipment />
              Pedidos e Cotações
            </SidebarLink>
          )}
          <SidebarLink href="/alerts" active={pathname.startsWith("/alerts")}>
            <IconAlert />
            Alertas
          </SidebarLink>
          {canReadReports(role) && (
            <SidebarLink href="/reports/daily" active={pathname.startsWith("/reports")}>
              <IconReport />
              Relatório Diário
            </SidebarLink>
          )}

          <div className="my-3 border-t border-white/[0.08]" />
          <p className="mb-2 px-3 text-[10px] font-bold uppercase tracking-widest text-zinc-400">Sistema</p>

          {canReadAudit(role) && (
            <SidebarLink href="/audit" active={pathname.startsWith("/audit")}>
              <IconAudit />
              Auditoria
            </SidebarLink>
          )}
          {canReadUsers(role) && (
            <SidebarLink href="/users" active={pathname.startsWith("/users")}>
              <IconUsers />
              Usuários
            </SidebarLink>
          )}
        </nav>

        {/* Footer */}
        <div className="border-t border-white/[0.08] p-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-red-600/15 text-xs font-bold text-red-400">
              {session?.email?.[0]?.toUpperCase() ?? "D"}
            </div>
            <div className="min-w-0 flex-1" suppressHydrationWarning>
              <p className="truncate text-sm font-medium text-zinc-300">{session?.email}</p>
              <p className="text-[11px] text-zinc-400">{session?.role} {getRoleUiLabel(session?.role ?? "auditoria")}</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main area — White */}
      <div className="flex flex-1 flex-col bg-white">
        {/* Top bar (mobile) */}
        <header className="flex h-14 items-center justify-between border-b border-zinc-200 bg-white px-4 lg:hidden">
          <span className="text-base font-bold tracking-tight text-zinc-900">
            Ilex <span className="text-red-600">Logística</span>
          </span>
          <button
            onClick={onLogout}
            className="rounded-lg bg-zinc-900 px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-zinc-800"
          >
            Sair
          </button>
        </header>

        {/* Top bar desktop */}
        <header className="hidden h-14 items-center justify-end border-b border-zinc-200 bg-white px-6 lg:flex">
          <button
            onClick={onLogout}
            className="rounded-lg border border-zinc-200 bg-white px-4 py-2 text-xs font-semibold text-zinc-700 transition-all hover:border-zinc-300 hover:bg-zinc-50"
          >
            Sair
          </button>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto bg-white p-6 lg:p-8">{children}</main>
=======
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
>>>>>>> fix/infra-setup-local
      </div>
    </div>
  );
}

function SidebarLink({ href, active, children }: { href: string; active: boolean; children: React.ReactNode }) {
  return (
    <Link
      href={href}
      className={`flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-semibold transition-all ${
        active
          ? "bg-white/[0.1] text-white"
          : "text-zinc-400 hover:bg-white/[0.05] hover:text-zinc-200"
      }`}
    >
      {children}
    </Link>
  );
}

function IconDashboard() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
    </svg>
  );
}

function IconShipment() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
    </svg>
  );
}

function IconImport() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
    </svg>
  );
}

function IconCarrier() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
    </svg>
  );
}

function IconAlert() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
    </svg>
  );
}

function IconReport() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
    </svg>
  );
}

function IconAudit() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  );
}

function IconUsers() {
  return (
    <svg className="h-[18px] w-[18px]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
    </svg>
  );
}
