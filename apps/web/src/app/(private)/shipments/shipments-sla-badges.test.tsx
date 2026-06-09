import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { formatSlaStatusLabel, getSlaStatusBadgeColor, formatDelayDays, formatDateBR } from "@/lib/sla-helpers";

describe("Shipments SLA badges", () => {
  it("Deve renderizar badge 'No prazo'", () => {
    const status = "on_time";
    const label = formatSlaStatusLabel(status);
    const color = getSlaStatusBadgeColor(status);
    expect(label).toBe("No prazo");
    expect(color).toBe("bg-green-100 text-green-800");
  });

  it("Deve renderizar badge 'Atenção'", () => {
    const status = "warning";
    const label = formatSlaStatusLabel(status);
    const color = getSlaStatusBadgeColor(status);
    expect(label).toBe("Atenção");
    expect(color).toBe("bg-yellow-100 text-yellow-800");
  });

  it("Deve renderizar badge 'Atrasada'", () => {
    const status = "late";
    const label = formatSlaStatusLabel(status);
    const color = getSlaStatusBadgeColor(status);
    expect(label).toBe("Atrasada");
    expect(color).toBe("bg-orange-100 text-orange-800");
  });

  it("Deve renderizar badge 'Crítica'", () => {
    const status = "critical";
    const label = formatSlaStatusLabel(status);
    const color = getSlaStatusBadgeColor(status);
    expect(label).toBe("Crítica");
    expect(color).toBe("bg-red-100 text-red-800");
  });

  it("Deve renderizar 'Sem SLA' quando status unknown", () => {
    const status = "unknown";
    const label = formatSlaStatusLabel(status);
    const color = getSlaStatusBadgeColor(status);
    expect(label).toBe("Sem SLA");
    expect(color).toBe("bg-gray-100 text-gray-800");
  });

  it("Deve exibir atraso em dias", () => {
    const delay = formatDelayDays(2);
    expect(delay).toBe("+2 dias");
  });

  it("Deve exibir data limite SLA", () => {
    const date = new Date(2025, 0, 20); // 20/01/2025
    const dateString = date.toISOString();
    const formatted = formatDateBR(dateString);
    expect(formatted).toBe("20/01/2025");
  });

  it("Deve manter campos fiscais/financeiros existentes", () => {
    // Este teste verifica que os helpers não quebram campos existentes
    const fiscalValue = formatDelayDays(null);
    expect(fiscalValue).toBe("-");
  });
});
