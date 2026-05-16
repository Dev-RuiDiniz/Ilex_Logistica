import { describe, expect, it } from "vitest";
import { buildSearchParams, monthYearToDateRange } from "./shipment-utils";

describe("shipment-utils", () => {
  describe("monthYearToDateRange", () => {
    it("converte mês/ano para intervalo de datas correto", () => {
      const result = monthYearToDateRange(5, 2026);
      expect(result.from).toBe("2026-05-01");
      expect(result.to).toBe("2026-05-31");
    });

    it("converte janeiro corretamente", () => {
      const result = monthYearToDateRange(1, 2026);
      expect(result.from).toBe("2026-01-01");
      expect(result.to).toBe("2026-01-31");
    });

    it("converte dezembro corretamente", () => {
      const result = monthYearToDateRange(12, 2026);
      expect(result.from).toBe("2026-12-01");
      expect(result.to).toBe("2026-12-31");
    });

    it("converte ano bissexto fevereiro corretamente", () => {
      const result = monthYearToDateRange(2, 2024);
      expect(result.from).toBe("2024-02-01");
      expect(result.to).toBe("2024-02-29");
    });
  });

  describe("buildSearchParams", () => {
    it("retorna objeto vazio para busca vazia", () => {
      const result = buildSearchParams("tracking", "");
      expect(result).toEqual({});
    });

    it("retorna tracking_code para tipo tracking", () => {
      const result = buildSearchParams("tracking", "ABC123");
      expect(result).toEqual({ tracking_code: "ABC123" });
    });

    it("retorna invoice_number para tipo invoice", () => {
      const result = buildSearchParams("invoice", "NF12345");
      expect(result).toEqual({ invoice_number: "NF12345" });
    });

    it("retorna invoice_number para tipo all com valor numérico", () => {
      const result = buildSearchParams("all", "12345");
      expect(result).toEqual({ invoice_number: "12345" });
    });

    it("retorna tracking_code para tipo all com valor não numérico", () => {
      const result = buildSearchParams("all", "ABC123");
      expect(result).toEqual({ tracking_code: "ABC123" });
    });

    it("retorna tracking_code para tipo all com valor alfanumérico", () => {
      const result = buildSearchParams("all", "ABC123XYZ");
      expect(result).toEqual({ tracking_code: "ABC123XYZ" });
    });

    it("retorna tracking_code para tipo all com valor alfanumérico misto", () => {
      const result = buildSearchParams("all", "123ABC");
      expect(result).toEqual({ tracking_code: "123ABC" });
    });
  });

  describe("comportamento de integração", () => {
    it("verifica que monthYearToDateRange retorna formato ISO compatível com API", () => {
      const result = monthYearToDateRange(3, 2026);
      expect(result.from).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(result.to).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    });

    it("verifica que buildSearchParams não retorna ambos tracking_code e invoice_number simultaneamente", () => {
      const result = buildSearchParams("all", "ABC123");
      const hasTracking = "tracking_code" in result;
      const hasInvoice = "invoice_number" in result;
      expect(hasTracking || hasInvoice).toBe(true);
      expect(hasTracking && hasInvoice).toBe(false);
    });
  });
});
