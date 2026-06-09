import { describe, expect, it } from "vitest";
import {
  formatSlaStatusLabel,
  formatCriticalityLabel,
  formatDelayDays,
  formatDateBR,
  formatUnavailable,
  getSlaStatusBadgeColor,
  getCriticalityBadgeColor,
} from "./sla-helpers";

describe("SLA presentation helpers", () => {
  describe("formatSlaStatusLabel", () => {
    it("deve renderizar 'No prazo' para on_time", () => {
      expect(formatSlaStatusLabel("on_time")).toBe("No prazo");
    });

    it("deve renderizar 'Atenção' para warning", () => {
      expect(formatSlaStatusLabel("warning")).toBe("Atenção");
    });

    it("deve renderizar 'Atrasada' para late", () => {
      expect(formatSlaStatusLabel("late")).toBe("Atrasada");
    });

    it("deve renderizar 'Crítica' para critical", () => {
      expect(formatSlaStatusLabel("critical")).toBe("Crítica");
    });

    it("deve renderizar 'Sem SLA' para unknown", () => {
      expect(formatSlaStatusLabel("unknown")).toBe("Sem SLA");
    });

    it("deve renderizar 'Sem SLA' para null", () => {
      expect(formatSlaStatusLabel(null)).toBe("Sem SLA");
    });
  });

  describe("formatCriticalityLabel", () => {
    it("deve renderizar 'Normal' para normal", () => {
      expect(formatCriticalityLabel("normal")).toBe("Normal");
    });

    it("deve renderizar 'Baixa' para baixa", () => {
      expect(formatCriticalityLabel("baixa")).toBe("Baixa");
    });

    it("deve renderizar 'Média' para media", () => {
      expect(formatCriticalityLabel("media")).toBe("Média");
    });

    it("deve renderizar 'Alta' para alta", () => {
      expect(formatCriticalityLabel("alta")).toBe("Alta");
    });

    it("deve retornar o valor original para criticidade desconhecida", () => {
      expect(formatCriticalityLabel("desconhecida")).toBe("desconhecida");
    });
  });

  describe("formatDelayDays", () => {
    it("deve exibir '-' para null", () => {
      expect(formatDelayDays(null)).toBe("-");
    });

    it("deve exibir '-' para undefined", () => {
      expect(formatDelayDays(undefined)).toBe("-");
    });

    it("deve exibir '0 dias' para 0", () => {
      expect(formatDelayDays(0)).toBe("0 dias");
    });

    it("deve exibir '+2 dias' para 2", () => {
      expect(formatDelayDays(2)).toBe("+2 dias");
    });

    it("deve exibir '-1 dias' para -1", () => {
      expect(formatDelayDays(-1)).toBe("-1 dias");
    });
  });

  describe("formatDateBR", () => {
    it("deve exibir '-' para null", () => {
      expect(formatDateBR(null)).toBe("-");
    });

    it("deve exibir '-' para string vazia", () => {
      expect(formatDateBR("")).toBe("-");
    });

    it("deve formatar data ISO para formato brasileiro", () => {
      // Usando data com timezone local para evitar problemas de conversão
      const date = new Date(2025, 0, 20); // 20/01/2025
      const dateString = date.toISOString();
      expect(formatDateBR(dateString)).toBe("20/01/2025");
    });
  });

  describe("formatUnavailable", () => {
    it("deve exibir '-' para null", () => {
      expect(formatUnavailable(null)).toBe("-");
    });

    it("deve exibir '-' para undefined", () => {
      expect(formatUnavailable(undefined)).toBe("-");
    });

    it("deve exibir '-' para string vazia", () => {
      expect(formatUnavailable("")).toBe("-");
    });

    it("deve retornar o valor como string para valor válido", () => {
      expect(formatUnavailable("teste")).toBe("teste");
    });

    it("deve retornar o valor como string para número", () => {
      expect(formatUnavailable(123)).toBe("123");
    });
  });

  describe("getSlaStatusBadgeColor", () => {
    it("deve retornar cor verde para on_time", () => {
      expect(getSlaStatusBadgeColor("on_time")).toBe("bg-green-100 text-green-800");
    });

    it("deve retornar cor amarela para warning", () => {
      expect(getSlaStatusBadgeColor("warning")).toBe("bg-yellow-100 text-yellow-800");
    });

    it("deve retornar cor laranja para late", () => {
      expect(getSlaStatusBadgeColor("late")).toBe("bg-orange-100 text-orange-800");
    });

    it("deve retornar cor vermelha para critical", () => {
      expect(getSlaStatusBadgeColor("critical")).toBe("bg-red-100 text-red-800");
    });

    it("deve retornar cor cinza para unknown", () => {
      expect(getSlaStatusBadgeColor("unknown")).toBe("bg-gray-100 text-gray-800");
    });

    it("deve retornar cor cinza para null", () => {
      expect(getSlaStatusBadgeColor(null)).toBe("bg-gray-100 text-gray-800");
    });
  });

  describe("getCriticalityBadgeColor", () => {
    it("deve retornar cor verde para normal", () => {
      expect(getCriticalityBadgeColor("normal")).toBe("bg-green-100 text-green-800");
    });

    it("deve retornar cor amarela para baixa", () => {
      expect(getCriticalityBadgeColor("baixa")).toBe("bg-yellow-100 text-yellow-800");
    });

    it("deve retornar cor laranja para media", () => {
      expect(getCriticalityBadgeColor("media")).toBe("bg-orange-100 text-orange-800");
    });

    it("deve retornar cor vermelha para alta", () => {
      expect(getCriticalityBadgeColor("alta")).toBe("bg-red-100 text-red-800");
    });

    it("deve retornar cor cinza para criticidade desconhecida", () => {
      expect(getCriticalityBadgeColor("desconhecida")).toBe("bg-gray-100 text-gray-800");
    });
  });
});
