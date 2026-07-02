import { describe, expect, it } from "vitest";

function formatCurrencyBRL(value: number | null | undefined): string {
  if (value === null || value === undefined) return "\u2014";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

function formatPercentage(value: number | null | undefined): string {
  if (value === null || value === undefined) return "-";
  return `${value.toFixed(2)}%`;
}

function formatUnavailable(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
}

describe("Renderizacao de campos fiscais - edge cases (P1.1)", () => {
  describe("formatCurrencyBRL", () => {
    it("Deve exibir traco quando valor e null", () => {
      expect(formatCurrencyBRL(null)).toBe("\u2014");
    });

    it("Deve exibir traco quando valor e undefined", () => {
      expect(formatCurrencyBRL(undefined)).toBe("\u2014");
    });

    it("Deve exibir R$ 0,00 quando valor e zero", () => {
      expect(formatCurrencyBRL(0)).toBe("R$\u00A00,00");
    });

    it("Deve formatar valor normal corretamente", () => {
      expect(formatCurrencyBRL(150.0)).toContain("150");
    });

    it("Deve formatar valor maximo de precisao", () => {
      expect(formatCurrencyBRL(99999.99)).toContain("99.999,99");
    });
  });

  describe("formatPercentage", () => {
    it("Deve exibir traco quando percentual e null", () => {
      expect(formatPercentage(null)).toBe("-");
    });

    it("Deve exibir traco quando percentual e undefined", () => {
      expect(formatPercentage(undefined)).toBe("-");
    });

    it("Deve exibir 0,00% quando percentual e zero", () => {
      expect(formatPercentage(0)).toBe("0.00%");
    });

    it("Deve formatar percentual normal", () => {
      expect(formatPercentage(10.0)).toBe("10.00%");
    });

    it("Deve formatar percentual muito alto sem NaN/Infinity", () => {
      expect(formatPercentage(1000000.0)).toBe("1000000.00%");
    });
  });

  describe("formatUnavailable", () => {
    it("Deve exibir traco quando valor e null", () => {
      expect(formatUnavailable(null)).toBe("-");
    });

    it("Deve exibir traco quando valor e undefined", () => {
      expect(formatUnavailable(undefined)).toBe("-");
    });

    it("Deve exibir traco quando valor e string vazia", () => {
      expect(formatUnavailable("")).toBe("-");
    });

    it("Deve exibir valor quando preenchido", () => {
      expect(formatUnavailable("SP")).toBe("SP");
    });

    it("Deve exibir numero como string", () => {
      expect(formatUnavailable(42)).toBe("42");
    });
  });
});
