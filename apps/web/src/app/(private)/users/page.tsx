"use client";

import { FormEvent, useEffect, useState } from "react";
import { createUser, listUsers, updateUser } from "@/lib/api";
import { canReadUsers, canWriteUsers } from "@/lib/permissions";
import { useAuth } from "@/features/auth/auth-provider";
import { useApiErrorHandler } from "@/lib/useApiErrorHandler";
import { AccessDenied } from "@/components/AccessDenied";
import type { UserListItem, UserRole } from "@/lib/types";

const roleOptions: UserRole[] = ["admin", "manager", "operator", "viewer", "logistica", "gestor", "auditoria"];

export default function UsersPage() {
  const { session } = useAuth();
  const role = session?.role ?? "auditoria";
  const [items, setItems] = useState<UserListItem[]>([]);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [selectedRole, setSelectedRole] = useState<UserRole>("logistica");
  const [loading, setLoading] = useState(true);
  const { handleApiError, accessDenied, accessDeniedMessage } = useApiErrorHandler();

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      try {
        setLoading(true);
        const users = await listUsers(session.accessToken);
        if (!cancelled) setItems(users);
      } catch {
        if (!cancelled) setError("Falha ao carregar usuários.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    void run();
    return () => { cancelled = true; };
  }, [session]);

  if (accessDenied) {
    return <AccessDenied message={accessDeniedMessage} />;
  }

  if (!canReadUsers(role)) {
    return (
      <div className="flex items-center justify-center rounded-2xl border border-red-200 bg-red-50 p-8">
        <div className="text-center">
          <svg className="mx-auto h-10 w-10 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          <p className="mt-2 text-sm font-medium text-red-600">Você não tem permissão para acessar esta página.</p>
        </div>
      </div>
    );
  }

  const reloadUsers = async () => {
    if (!session) return;
    try {
      setItems(await listUsers(session.accessToken));
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao recarregar usuários"));
      setError(err instanceof Error ? err.message : "Erro ao recarregar usuários");
    }
  };

  const onCreate = async (event: FormEvent) => {
    event.preventDefault();
    if (!session) return;
    try {
      await createUser(session.accessToken, { email, full_name: fullName, password: "123456", roles: [role] });
      setEmail("");
      setFullName("");
      setSelectedRole("logistica");
      await reloadUsers();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao criar usuário"));
      setError(err instanceof Error ? err.message : "Erro ao criar usuário");
    }
  };

  const onPromote = async (item: UserListItem, nextRole: UserRole) => {
    if (!session) return;
    try {
      await updateUser(session.accessToken, item.id, { roles: [nextRole] });
      await reloadUsers();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao atualizar usuário"));
      setError(err instanceof Error ? err.message : "Erro ao atualizar usuário");
    }
  };

  const onInactivate = async (item: UserListItem) => {
    if (!session) return;
    try {
      await updateUser(session.accessToken, item.id, { is_active: false });
      await reloadUsers();
    } catch (err) {
      handleApiError(err instanceof Error ? err : new Error("Erro ao inativar usuário"));
      setError(err instanceof Error ? err.message : "Erro ao inativar usuário");
    }
  };

  const canWrite = canWriteUsers(role);
  const inputClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black placeholder:text-zinc-400 transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const selectClass = "w-full rounded-lg border border-zinc-200 bg-white px-3 py-2.5 text-sm text-black transition-colors focus:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500/20 disabled:opacity-50";
  const btnPrimary = "rounded-lg bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white transition-all hover:bg-zinc-800 disabled:opacity-50";

  return (
<<<<<<< HEAD
    <section className="space-y-6">
      {/* Header */}
      <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-zinc-900">Usuários e Permissões</h1>
          <p className="mt-1 text-sm font-medium text-zinc-500">Gestão de contas e papéis de acesso</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-zinc-500">
          <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
          {items.length} usuário{items.length !== 1 ? "s" : ""}
        </div>
      </header>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {error}
        </div>
      )}

      {/* Create Form */}
      {canWrite && (
        <form onSubmit={onCreate} className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-base font-bold text-zinc-900">Novo Usuário</h3>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">E-mail</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="email@empresa.com"
                required
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Nome completo</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Nome do usuário"
                required
                className={inputClass}
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Perfil</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value as UserRole)}
                className={selectClass}
              >
                {roleOptions.map((item) => (
                  <option key={item} value={item}>{item}</option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <button type="submit" className={btnPrimary + " w-full"}>
                Criar Usuário
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Users Table */}
      <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="flex items-center justify-between border-b border-zinc-100 px-6 py-4">
          <p className="text-sm font-semibold text-zinc-700">
            {items.length} usuário{items.length !== 1 ? "s" : ""} cadastrado{items.length !== 1 ? "s" : ""}
          </p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center p-12">
            <div className="flex items-center gap-3">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-zinc-200 border-t-red-500" />
              <p className="text-sm font-medium text-zinc-500">Carregando usuários...</p>
            </div>
          </div>
        ) : items.length === 0 ? (
          <div className="p-12 text-center">
            <svg className="mx-auto h-12 w-12 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
            </svg>
            <p className="mt-3 text-sm font-medium text-zinc-500">Nenhum usuário encontrado</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-zinc-100 bg-zinc-50/80">
                  <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">E-mail</th>
                  <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Nome</th>
                  <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Perfil</th>
                  <th className="px-6 py-3 text-left text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Status</th>
                  {canWrite && <th className="px-6 py-3 text-right text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Ações</th>}
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-b border-zinc-50 transition-colors hover:bg-zinc-50/50">
                    <td className="px-6 py-3.5 font-medium text-zinc-900">{item.email}</td>
                    <td className="px-6 py-3.5 text-zinc-700">{item.full_name}</td>
                    <td className="px-6 py-3.5">
                      <div className="flex flex-wrap gap-1">
                        {item.roles.map((r) => (
                          <span key={r} className="inline-flex rounded-full bg-zinc-100 px-2.5 py-0.5 text-[11px] font-semibold text-zinc-600 ring-1 ring-zinc-300">
                            {r}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-3.5">
                      <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold ${
                        item.is_active
                          ? "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20"
                          : "bg-zinc-100 text-zinc-500 ring-1 ring-zinc-300"
                      }`}>
                        {item.is_active ? "Ativo" : "Inativo"}
                      </span>
                    </td>
                    {canWrite && (
                      <td className="px-6 py-3.5">
                        <div className="flex justify-end gap-2">
                          <select
                            className="rounded-lg border border-zinc-200 bg-white px-2.5 py-1.5 text-xs font-semibold text-zinc-700 transition-colors hover:border-zinc-300 disabled:bg-zinc-100 disabled:text-zinc-400 disabled:cursor-not-allowed"
                            defaultValue={item.roles[0] ?? "logistica"}
                            onChange={(e) => void onPromote(item, e.target.value as UserRole)}
                            disabled={!canWrite}
                          >
                            {roleOptions.map((roleItem) => (
                              <option key={roleItem} value={roleItem}>{roleItem}</option>
                            ))}
                          </select>
                          <button
                            onClick={() => void onInactivate(item)}
                            disabled={!canWrite}
                            className="rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-semibold text-red-600 transition-all hover:border-red-300 hover:bg-red-50 disabled:text-zinc-400 disabled:cursor-not-allowed"
                          >
                            Inativar
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
=======
    <section className="page-stack">
      <header className="page-hero">
        <p className="page-kicker">Segurança e acesso</p>
        <h2 className="page-title !text-[clamp(1.65rem,1.3rem+0.8vw,2.4rem)]">Usuários e Permissões</h2>
        <p className="page-subtitle">Gerencie contas, papéis e governança de acesso com mais clareza operacional.</p>
      </header>
      {error && <p className="error-state">{error}</p>}
      <form onSubmit={onCreate} className="surface-panel grid gap-3 p-5 md:grid-cols-4 md:p-6">
        <input value={email} onChange={(e) => setEmail(e.target.value)} className="field" placeholder="E-mail" required />
        <input value={fullName} onChange={(e) => setFullName(e.target.value)} className="field" placeholder="Nome completo" required />
        <select value={selectedRole} onChange={(e) => setSelectedRole(e.target.value as UserRole)} className="field-select">
          {roleOptions.map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
        <button 
          className={canWriteUsers(role) ? "button-primary" : "button-secondary cursor-not-allowed"} 
          type="submit" 
          disabled={!canWriteUsers(role)}
        >
          Criar
        </button>
      </form>
      <div className="table-shell overflow-hidden">
        <table className="data-table">
          <thead className="text-left">
            <tr>
              <th className="px-3 py-2">E-mail</th>
              <th className="px-3 py-2">Nome</th>
              <th className="px-3 py-2">Perfil</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">Ações</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td className="px-3 py-2">{item.email}</td>
                <td className="px-3 py-2">{item.full_name}</td>
                <td className="px-3 py-2">{item.roles.join(", ")}</td>
                <td className="px-3 py-2">{item.is_active ? "Ativo" : "Inativo"}</td>
                <td className="px-3 py-2">
                  <div className="flex gap-2">
                    <select
                      className={`field-select !px-2 !py-1 text-xs ${canWriteUsers(role) ? "" : "bg-slate-100 text-slate-400 cursor-not-allowed"}`}
                      defaultValue={item.roles[0] ?? "logistica"}
                      onChange={(e) => void onPromote(item, e.target.value as UserRole)}
                      disabled={!canWriteUsers(role)}
                    >
                      {roleOptions.map((roleItem) => <option key={roleItem} value={roleItem}>{roleItem}</option>)}
                    </select>
                    <button 
                      className={canWriteUsers(role) ? "button-danger !px-3 !py-2 !text-xs" : "button-secondary cursor-not-allowed !px-3 !py-2 !text-xs"} 
                      onClick={() => void onInactivate(item)} 
                      type="button"
                      disabled={!canWriteUsers(role)}
                    >
                      Inativar
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
>>>>>>> fix/infra-setup-local
      </div>
    </section>
  );
}
