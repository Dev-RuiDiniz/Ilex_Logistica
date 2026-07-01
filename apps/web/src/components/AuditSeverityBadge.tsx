import type { AuditSeverity } from "@/lib/audit-api";

interface AuditSeverityBadgeProps {
  severity: AuditSeverity;
}

export function AuditSeverityBadge({ severity }: AuditSeverityBadgeProps) {
  const styles: Record<string, string> = {
    info: "bg-blue-50 text-blue-700 ring-1 ring-blue-600/20",
    warning: "bg-amber-50 text-amber-700 ring-1 ring-amber-600/20",
    critical: "bg-red-50 text-red-700 ring-1 ring-red-600/20",
  };

  const labels: Record<string, string> = {
    info: "Info",
    warning: "Warning",
    critical: "Critical",
  };

  return (
    <span
      data-testid="audit-severity-badge"
      className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold ${styles[severity] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20"}`}
    >
      {labels[severity] || severity}
    </span>
  );
}
