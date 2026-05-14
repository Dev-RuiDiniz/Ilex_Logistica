import type { UserRole } from "@/lib/types";

export function canEditCarriers(role: UserRole): boolean {
  return role === "admin" || role === "logistica" || role === "gestor";
}

export function canViewCarriers(role: UserRole): boolean {
  return canEditCarriers(role) || role === "auditoria";
}

export function getCarriersAccessMode(role: UserRole): "edit" | "read" {
  return canEditCarriers(role) ? "edit" : "read";
}
