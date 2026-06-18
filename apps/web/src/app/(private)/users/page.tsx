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
  const { accessDenied, accessDeniedMessage, handleApiError } = useApiErrorHandler();

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      if (!session) return;
      try {
        const users = await listUsers(session.accessToken);
        if (!cancelled) setItems(users);
      } catch {
        if (!cancelled) setError("Falha ao carregar usuários.");
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
      <div className="rounded border bg-red-50 p-4 text-center">
        <p className="text-sm text-red-700">Você não tem permissão para acessar esta página.</p>
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

  return (
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
      </div>
    </section>
  );
}
