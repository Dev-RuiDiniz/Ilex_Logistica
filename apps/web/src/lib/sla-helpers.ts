// BETA-013B: SLA presentation helpers

export type SlaStatus = "on_time" | "warning" | "late" | "critical" | "unknown" | null;

export function formatSlaStatusLabel(status: SlaStatus): string {
  const labels: Record<string, string> = {
    on_time: "No prazo",
    warning: "Atenção",
    late: "Atrasada",
    critical: "Crítica",
    unknown: "Sem SLA",
  };
  return labels[status || "unknown"] || "Sem SLA";
}

export function formatCriticalityLabel(criticality: string): string {
  const labels: Record<string, string> = {
    normal: "Normal",
    baixa: "Baixa",
    media: "Média",
    alta: "Alta",
  };
  return labels[criticality] || criticality;
}

export function formatDelayDays(delayDays: number | null): string {
  if (delayDays === null || delayDays === undefined) return "-";
  if (delayDays === 0) return "0 dias";
  if (delayDays > 0) return `+${delayDays} dias`;
  return `${delayDays} dias`;
}

export function formatDateBR(dateString: string | null): string {
  if (!dateString) return "-";
  return new Date(dateString).toLocaleDateString("pt-BR");
}

export function formatUnavailable(value: string | number | null): string {
  if (value === null || value === undefined || value === "") return "-";
  return String(value);
}

export function getSlaStatusBadgeColor(status: SlaStatus): string {
  const colors: Record<string, string> = {
    on_time: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    late: "bg-orange-100 text-orange-800",
    critical: "bg-red-100 text-red-800",
    unknown: "bg-gray-100 text-gray-800",
  };
  return colors[status || "unknown"] || colors.unknown;
}

export function getCriticalityBadgeColor(criticality: string): string {
  const colors: Record<string, string> = {
    normal: "bg-green-100 text-green-800",
    baixa: "bg-yellow-100 text-yellow-800",
    media: "bg-orange-100 text-orange-800",
    alta: "bg-red-100 text-red-800",
  };
  return colors[criticality] || "bg-gray-100 text-gray-800";
}
