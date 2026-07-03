import type { Permission, UserRole } from "@/lib/types";

// Role to permissions mapping (must match backend RBAC matrix)
const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  admin: [
    "audit:read",
    "reports:read",
    "reports:write",
    "alerts:read",
    "alerts:write",
    "sla:read",
    "sla:write",
    "shipments:read",
    "shipments:write",
    "imports:read",
    "imports:write",
    "carriers:read",
    "carriers:write",
    "users:read",
    "users:write",
    "orders:read",
    "orders:write",
    "quotes:read",
    "quotes:write",
    "quotes:override",
  ],
  manager: [
    "audit:read",
    "reports:read",
    "reports:write",
    "alerts:read",
    "alerts:write",
    "sla:read",
    "sla:write",
    "shipments:read",
    "imports:read",
    "carriers:read",
    "orders:read",
    "quotes:read",
    "quotes:override",
  ],
  operator: [
    "shipments:read",
    "shipments:write",
    "imports:read",
    "imports:write",
    "alerts:read",
    "alerts:write",
    "orders:read",
    "orders:write",
    "quotes:read",
    "quotes:write",
  ],
  viewer: [
    "shipments:read",
    "imports:read",
    "sla:read",
    "alerts:read",
    "reports:read",
    "carriers:read",
    "orders:read",
    "quotes:read",
  ],
  logistica: [
    "shipments:read",
    "shipments:write",
    "imports:read",
    "imports:write",
    "carriers:read",
    "carriers:write",
    "orders:read",
    "orders:write",
    "quotes:read",
    "quotes:write",
  ],
  gestor: [
    "shipments:read",
    "imports:read",
    "sla:read",
    "alerts:read",
    "reports:read",
    "carriers:read",
    "orders:read",
    "quotes:read",
    "quotes:override",
  ],
  auditoria: [
    "audit:read",
    "shipments:read",
    "imports:read",
    "carriers:read",
    "orders:read",
    "quotes:read",
  ],
};

// Legacy functions (for backward compatibility)
export function canEditCarriers(role: UserRole): boolean {
  return hasPermission(role, "carriers:write");
}

export function canViewCarriers(role: UserRole): boolean {
  return hasPermission(role, "carriers:read");
}

export function canEditShipments(role: UserRole): boolean {
  return hasPermission(role, "shipments:write");
}

export function canViewShipments(role: UserRole): boolean {
  return hasPermission(role, "shipments:read");
}

export function getCarriersAccessMode(role: UserRole): "edit" | "read" {
  return canEditCarriers(role) ? "edit" : "read";
}

// New RBAC helpers
export function getPermissionsForRole(role: UserRole): Permission[] {
  return ROLE_PERMISSIONS[role] ?? [];
}

export function hasPermission(role: UserRole, permission: Permission): boolean {
  return getPermissionsForRole(role).includes(permission);
}

export function hasAnyPermission(role: UserRole, permissions: Permission[]): boolean {
  return permissions.some((p) => hasPermission(role, p));
}

export function hasAllPermissions(role: UserRole, permissions: Permission[]): boolean {
  return permissions.every((p) => hasPermission(role, p));
}

// Specific permission helpers
export function canReadAudit(role: UserRole): boolean {
  return hasPermission(role, "audit:read");
}

export function canReadReports(role: UserRole): boolean {
  return hasPermission(role, "reports:read");
}

export function canWriteReports(role: UserRole): boolean {
  return hasPermission(role, "reports:write");
}

export function canReadAlerts(role: UserRole): boolean {
  return hasPermission(role, "alerts:read");
}

export function canWriteAlerts(role: UserRole): boolean {
  return hasPermission(role, "alerts:write");
}

export function canReadSla(role: UserRole): boolean {
  return hasPermission(role, "sla:read");
}

export function canWriteSla(role: UserRole): boolean {
  return hasPermission(role, "sla:write");
}

export function canReadShipments(role: UserRole): boolean {
  return hasPermission(role, "shipments:read");
}

export function canWriteShipments(role: UserRole): boolean {
  return hasPermission(role, "shipments:write");
}

export function canReadImports(role: UserRole): boolean {
  return hasPermission(role, "imports:read");
}

export function canWriteImports(role: UserRole): boolean {
  return hasPermission(role, "imports:write");
}

export function canReadCarriers(role: UserRole): boolean {
  return hasPermission(role, "carriers:read");
}

export function canWriteCarriers(role: UserRole): boolean {
  return hasPermission(role, "carriers:write");
}

export function canReadUsers(role: UserRole): boolean {
  return hasPermission(role, "users:read");
}

export function canWriteUsers(role: UserRole): boolean {
  return hasPermission(role, "users:write");
}

export function canReadOrders(role: UserRole): boolean {
  return hasPermission(role, "orders:read");
}

export function canWriteOrders(role: UserRole): boolean {
  return hasPermission(role, "orders:write");
}

export function canReadQuotes(role: UserRole): boolean {
  return hasPermission(role, "quotes:read");
}

export function canWriteQuotes(role: UserRole): boolean {
  return hasPermission(role, "quotes:write");
}

export function canOverrideQuotes(role: UserRole): boolean {
  return hasPermission(role, "quotes:override");
}
