import { describe, expect, it } from "vitest";

import {
  canEditCarriers,
  canViewCarriers,
  canEditShipments,
  canViewShipments,
  getCarriersAccessMode,
} from "@/lib/permissions";

describe("permissions", () => {
  describe("canEditCarriers", () => {
    it("permite edicao para admin, logistica e gestor", () => {
      expect(canEditCarriers("admin")).toBe(true);
      expect(canEditCarriers("logistica")).toBe(true);
      expect(canEditCarriers("gestor")).toBe(true);
    });

    it("bloqueia edicao para auditoria", () => {
      expect(canEditCarriers("auditoria")).toBe(false);
    });
  });

  describe("canViewCarriers", () => {
    it("permite leitura para admin, logistica, gestor e auditoria", () => {
      expect(canViewCarriers("admin")).toBe(true);
      expect(canViewCarriers("logistica")).toBe(true);
      expect(canViewCarriers("gestor")).toBe(true);
      expect(canViewCarriers("auditoria")).toBe(true);
    });
  });

  describe("canEditShipments", () => {
    it("allows admin to edit shipments", () => {
      expect(canEditShipments("admin")).toBe(true);
    });

    it("allows logistica to edit shipments", () => {
      expect(canEditShipments("logistica")).toBe(true);
    });

    it("allows gestor to edit shipments", () => {
      expect(canEditShipments("gestor")).toBe(true);
    });

    it("denies auditoria to edit shipments", () => {
      expect(canEditShipments("auditoria")).toBe(false);
    });
  });

  describe("canViewShipments", () => {
    it("allows admin to view shipments", () => {
      expect(canViewShipments("admin")).toBe(true);
    });

    it("allows logistica to view shipments", () => {
      expect(canViewShipments("logistica")).toBe(true);
    });

    it("allows gestor to view shipments", () => {
      expect(canViewShipments("gestor")).toBe(true);
    });

    it("allows auditoria to view shipments", () => {
      expect(canViewShipments("auditoria")).toBe(true);
    });
  });

  it("retorna modo de acesso textual para a UI", () => {
    expect(getCarriersAccessMode("admin")).toBe("edit");
    expect(getCarriersAccessMode("auditoria")).toBe("read");
  });
});
