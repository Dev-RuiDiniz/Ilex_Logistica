import { describe, expect, it } from "vitest";

import {
  apiLogin,
  buildApiUrl,
  confirmShipmentsImport,
  createCarrier,
  getApiBaseUrl,
  getDeliveryDetail,
  inactivateCarrier,
  listCarriers,
  listDeliveries,
  listShipments,
  updateCarrier,
  uploadShipmentsCsv,
} from "@/lib/api";

describe("api base url helpers", () => {
  it("normaliza barra final da base", () => {
    expect(getApiBaseUrl("http://localhost:8000/api/v1")).toBe("http://localhost:8000/api/v1");
  });

  it("usa fallback quando variavel nao existe", () => {
    expect(getApiBaseUrl(undefined)).toBe("http://127.0.0.1:8000/api/v1");
  });

  it("monta URL completa com path sem barra inicial", () => {
    expect(buildApiUrl("auth/login", "http://localhost:8000/api/v1")).toBe(
      "http://localhost:8000/api/v1/auth/login",
    );
  });

  it("monta URL completa com path com barra inicial", () => {
    expect(buildApiUrl("/auth/login", "http://localhost:8000/api/v1")).toBe(
      "http://localhost:8000/api/v1/auth/login",
    );
  });
});

describe("api exports e assinaturas", () => {
  it("apiLogin esta exportado", () => {
    expect(typeof apiLogin).toBe("function");
  });

  it("listCarriers esta exportado", () => {
    expect(typeof listCarriers).toBe("function");
  });

  it("createCarrier esta exportado", () => {
    expect(typeof createCarrier).toBe("function");
  });

  it("updateCarrier esta exportado", () => {
    expect(typeof updateCarrier).toBe("function");
  });

  it("inactivateCarrier esta exportado", () => {
    expect(typeof inactivateCarrier).toBe("function");
  });

  it("uploadShipmentsCsv esta exportado", () => {
    expect(typeof uploadShipmentsCsv).toBe("function");
  });

  it("confirmShipmentsImport esta exportado", () => {
    expect(typeof confirmShipmentsImport).toBe("function");
  });

  it("listShipments esta exportado", () => {
    expect(typeof listShipments).toBe("function");
  });

  it("listDeliveries esta exportado (LOG-011)", () => {
    expect(typeof listDeliveries).toBe("function");
  });

  it("getDeliveryDetail esta exportado (LOG-012)", () => {
    expect(typeof getDeliveryDetail).toBe("function");
  });

  it("uploadShipmentsCsv recebe token e file", () => {
    expect(uploadShipmentsCsv.length).toBe(2);
  });

  it("confirmShipmentsImport recebe token e importId", () => {
    expect(confirmShipmentsImport.length).toBe(2);
  });

  it("listShipments recebe token e params opcionais", () => {
    expect(listShipments.length).toBe(1);
  });

  it("listDeliveries recebe token e params opcionais (LOG-011)", () => {
    expect(listDeliveries.length).toBe(1);
  });

  it("getDeliveryDetail recebe token e deliveryId (LOG-012)", () => {
    expect(getDeliveryDetail.length).toBe(2);
  });
});
