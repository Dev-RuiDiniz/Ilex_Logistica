import { describe, expect, it } from "vitest";
import type { Permission, UserRole } from "@/lib/types";
import {
  canReadAlerts,
  canReadAudit,
  canReadCarriers,
  canReadImports,
  canReadOrders,
  canReadQuotes,
  canReadReports,
  canReadShipments,
  canReadUsers,
  canWriteAlerts,
  canWriteImports,
  canWriteOrders,
  canOverrideQuotes,
  canWriteReports,
  canWriteShipments,
  canWriteSla,
  canWriteUsers,
  getPermissionsForRole,
  hasAllPermissions,
  hasAnyPermission,
  hasPermission,
} from "./permissions";

describe("RBAC Permissions Helpers", () => {
  describe("getPermissionsForRole", () => {
    it("admin tem todas as permissões", () => {
      const permissions = getPermissionsForRole("admin");
      expect(permissions).toContain("audit:read");
      expect(permissions).toContain("reports:write");
      expect(permissions).toContain("alerts:write");
      expect(permissions).toContain("sla:write");
      expect(permissions).toContain("shipments:write");
      expect(permissions).toContain("imports:write");
      expect(permissions).toContain("carriers:write");
      expect(permissions).toContain("users:write");
    });

    it("manager tem permissões esperadas", () => {
      const permissions = getPermissionsForRole("manager");
      expect(permissions).toContain("audit:read");
      expect(permissions).toContain("reports:write");
      expect(permissions).toContain("alerts:write");
      expect(permissions).toContain("sla:write");
      expect(permissions).toContain("shipments:read");
      expect(permissions).toContain("imports:read");
      expect(permissions).toContain("carriers:read");
      expect(permissions).not.toContain("users:read");
      expect(permissions).not.toContain("users:write");
    });

    it("operator não acessa audit", () => {
      const permissions = getPermissionsForRole("operator");
      expect(permissions).not.toContain("audit:read");
      expect(permissions).toContain("shipments:write");
      expect(permissions).toContain("imports:write");
    });

    it("viewer não escreve", () => {
      const permissions = getPermissionsForRole("viewer");
      expect(permissions).toContain("shipments:read");
      expect(permissions).toContain("imports:read");
      expect(permissions).not.toContain("shipments:write");
      expect(permissions).not.toContain("imports:write");
      expect(permissions).not.toContain("reports:write");
    });

    it("aplica a matriz de pedidos e cotações", () => {
      expect(canWriteOrders("logistica")).toBe(true);
      expect(canReadOrders("auditoria")).toBe(true);
      expect(canReadQuotes("gestor")).toBe(true);
      expect(canOverrideQuotes("gestor")).toBe(true);
      expect(canWriteOrders("viewer")).toBe(false);
      expect(canOverrideQuotes("logistica")).toBe(false);
    });

    it("role desconhecida falha seguro", () => {
      const permissions = getPermissionsForRole("unknown" as UserRole);
      expect(permissions).toEqual([]);
    });

    it("usuário nulo/undefined falha seguro", () => {
      expect(hasPermission(null as unknown as UserRole, "audit:read")).toBe(false);
      expect(hasPermission(undefined as unknown as UserRole, "audit:read")).toBe(false);
      expect(getPermissionsForRole(null as unknown as UserRole)).toEqual([]);
      expect(getPermissionsForRole(undefined as unknown as UserRole)).toEqual([]);
    });
  });

  describe("hasPermission", () => {
    it("admin tem todas as permissões", () => {
      expect(hasPermission("admin", "audit:read")).toBe(true);
      expect(hasPermission("admin", "users:write")).toBe(true);
    });

    it("manager tem permissões específicas", () => {
      expect(hasPermission("manager", "audit:read")).toBe(true);
      expect(hasPermission("manager", "reports:write")).toBe(true);
      expect(hasPermission("manager", "users:read")).toBe(false);
    });

    it("permissão inexistente retorna false", () => {
      expect(hasPermission("viewer", "unknown:permission" as Permission)).toBe(false);
    });
  });

  describe("hasAnyPermission", () => {
    it("retorna true se tiver qualquer permissão", () => {
      expect(hasAnyPermission("manager", ["audit:read", "users:read"])).toBe(true);
    });

    it("retorna false se não tiver nenhuma", () => {
      expect(hasAnyPermission("viewer", ["users:read", "users:write"])).toBe(false);
    });
  });

  describe("hasAllPermissions", () => {
    it("retorna true se tiver todas as permissões", () => {
      expect(hasAllPermissions("admin", ["audit:read", "reports:write"])).toBe(true);
    });

    it("retorna false se faltar alguma", () => {
      expect(hasAllPermissions("manager", ["audit:read", "users:write"])).toBe(false);
    });
  });

  describe("Specific permission helpers", () => {
    it("canReadAudit", () => {
      expect(canReadAudit("admin")).toBe(true);
      expect(canReadAudit("manager")).toBe(true);
      expect(canReadAudit("auditoria")).toBe(true);
      expect(canReadAudit("operator")).toBe(false);
      expect(canReadAudit("viewer")).toBe(false);
    });

    it("canReadReports", () => {
      expect(canReadReports("admin")).toBe(true);
      expect(canReadReports("manager")).toBe(true);
      expect(canReadReports("viewer")).toBe(true);
      expect(canReadReports("operator")).toBe(false);
    });

    it("canWriteReports", () => {
      expect(canWriteReports("admin")).toBe(true);
      expect(canWriteReports("manager")).toBe(true);
      expect(canWriteReports("viewer")).toBe(false);
      expect(canWriteReports("operator")).toBe(false);
    });

    it("canReadShipments", () => {
      expect(canReadShipments("admin")).toBe(true);
      expect(canReadShipments("manager")).toBe(true);
      expect(canReadShipments("operator")).toBe(true);
      expect(canReadShipments("viewer")).toBe(true);
      expect(canReadShipments("auditoria")).toBe(true);
    });

    it("canWriteShipments", () => {
      expect(canWriteShipments("admin")).toBe(true);
      expect(canWriteShipments("operator")).toBe(true);
      expect(canWriteShipments("logistica")).toBe(true);
      expect(canWriteShipments("viewer")).toBe(false);
      expect(canWriteShipments("manager")).toBe(false);
    });

    it("canReadImports", () => {
      expect(canReadImports("admin")).toBe(true);
      expect(canReadImports("manager")).toBe(true);
      expect(canReadImports("operator")).toBe(true);
      expect(canReadImports("viewer")).toBe(true);
      expect(canReadImports("logistica")).toBe(true);
    });

    it("canWriteImports", () => {
      expect(canWriteImports("admin")).toBe(true);
      expect(canWriteImports("operator")).toBe(true);
      expect(canWriteImports("logistica")).toBe(true);
      expect(canWriteImports("viewer")).toBe(false);
      expect(canWriteImports("manager")).toBe(false);
    });

    it("canReadCarriers", () => {
      expect(canReadCarriers("admin")).toBe(true);
      expect(canReadCarriers("manager")).toBe(true);
      expect(canReadCarriers("viewer")).toBe(true);
      expect(canReadCarriers("logistica")).toBe(true);
      expect(canReadCarriers("gestor")).toBe(true);
      expect(canReadCarriers("auditoria")).toBe(true);
      expect(canReadCarriers("operator")).toBe(false);
    });

    it("canReadUsers", () => {
      expect(canReadUsers("admin")).toBe(true);
      expect(canReadUsers("manager")).toBe(false);
      expect(canReadUsers("operator")).toBe(false);
      expect(canReadUsers("viewer")).toBe(false);
    });

    it("canWriteUsers", () => {
      expect(canWriteUsers("admin")).toBe(true);
      expect(canWriteUsers("manager")).toBe(false);
      expect(canWriteUsers("operator")).toBe(false);
      expect(canWriteUsers("viewer")).toBe(false);
    });

    it("canReadAlerts", () => {
      expect(canReadAlerts("admin")).toBe(true);
      expect(canReadAlerts("manager")).toBe(true);
      expect(canReadAlerts("operator")).toBe(true);
      expect(canReadAlerts("viewer")).toBe(true);
    });

    it("canWriteAlerts", () => {
      expect(canWriteAlerts("admin")).toBe(true);
      expect(canWriteAlerts("manager")).toBe(true);
      expect(canWriteAlerts("operator")).toBe(true);
      expect(canWriteAlerts("viewer")).toBe(false);
    });

    it("canWriteSla", () => {
      expect(canWriteSla("admin")).toBe(true);
      expect(canWriteSla("manager")).toBe(true);
      expect(canWriteSla("operator")).toBe(false);
      expect(canWriteSla("viewer")).toBe(false);
    });
  });
});
