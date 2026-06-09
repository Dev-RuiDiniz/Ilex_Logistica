"use client";

import { FormEvent, useEffect, useState } from "react";

import { createUser, listUsers, updateUser } from "@/lib/api";
import { useAuth } from "@/features/auth/auth-provider";
import type { UserListItem, UserRole } from "@/lib/types";

const roleOptions: UserRole[] = ["admin", "logistica", "gestor", "auditoria"];

export default function UsersPage() {
  const { session } = useAuth();
  const [items, setItems] = useState<UserListItem[]>([]);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState<UserRole>("logistica");

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

  const reloadUsers = async () => {
    if (!session) return;
    try {
      setItems(await listUsers(session.accessToken));
    } catch {
      setError("Falha ao carregar usuários.");
    }
  };

  const onCreate = async (event: FormEvent) => {
    event.preventDefault();
    if (!session) return;
    try {
      await createUser(session.accessToken, { email, full_name: fullName, password: "123456", roles: [role] });
      setEmail("");
      setFullName("");
      setRole("logistica");
      await reloadUsers();
    } catch {
      setError("Falha ao criar usuário.");
    }
  };

  const onPromote = async (item: UserListItem, nextRole: UserRole) => {
    if (!session) return;
    try {
      await updateUser(session.accessToken, item.id, { roles: [nextRole] });
      await reloadUsers();
    } catch {
      setError("Falha ao atualizar perfil.");
    }
  };

  const onInactivate = async (item: UserListItem) => {
    if (!session) return;
    try {
      await updateUser(session.accessToken, item.id, { is_active: false });
      await reloadUsers();
    } catch {
      setError("Falha ao inativar usuário.");
    }
  };

  return (
    <section className="space-y-4">
      <header>
        <h2 className="text-xl font-semibold">Usuários e Permissões</h2>
        <p className="text-sm text-slate-600">Gestão de contas e papéis de acesso.</p>
      </header>
      {error && <p className="rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}
      <form onSubmit={onCreate} className="grid gap-2 rounded border p-4 md:grid-cols-4">
        <input value={email} onChange={(e) => setEmail(e.target.value)} className="rounded border px-3 py-2 text-sm" placeholder="E-mail" required />
        <input value={fullName} onChange={(e) => setFullName(e.target.value)} className="rounded border px-3 py-2 text-sm" placeholder="Nome completo" required />
        <select value={role} onChange={(e) => setRole(e.target.value as UserRole)} className="rounded border px-3 py-2 text-sm">
          {roleOptions.map((item) => <option key={item} value={item}>{item}</option>)}
        </select>
        <button className="rounded bg-slate-900 px-4 py-2 text-sm text-white" type="submit">Criar</button>
      </form>
      <div className="overflow-hidden rounded border">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 text-left">
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
              <tr key={item.id} className="border-t">
                <td className="px-3 py-2">{item.email}</td>
                <td className="px-3 py-2">{item.full_name}</td>
                <td className="px-3 py-2">{item.roles.join(", ")}</td>
                <td className="px-3 py-2">{item.is_active ? "Ativo" : "Inativo"}</td>
                <td className="px-3 py-2">
                  <div className="flex gap-2">
                    <select
                      className="rounded border px-2 py-1 text-xs"
                      defaultValue={item.roles[0] ?? "logistica"}
                      onChange={(e) => void onPromote(item, e.target.value as UserRole)}
                    >
                      {roleOptions.map((roleItem) => <option key={roleItem} value={roleItem}>{roleItem}</option>)}
                    </select>
                    <button className="rounded border px-2 py-1 text-xs text-red-700" onClick={() => void onInactivate(item)} type="button">
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
