import type { AuditSeverity } from "@/lib/audit-api";

interface AuditSeverityBadgeProps {
  severity: AuditSeverity;
}

export function AuditSeverityBadge({ severity }: AuditSeverityBadgeProps) {
  const colors = {
    info: "bg-blue-100 text-blue-800",
    warning: "bg-yellow-100 text-yellow-800",
    critical: "bg-red-100 text-red-800",
  };

  const labels = {
    info: "Info",
    warning: "Warning",
    critical: "Critical",
  };

  return (
    <span
      data-testid="audit-severity-badge"
      className={`px-2 py-1 rounded-full text-xs font-medium ${colors[severity]}`}
    >
      {labels[severity]}
    </span>
  );
}
