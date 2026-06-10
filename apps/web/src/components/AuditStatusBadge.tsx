import type { AuditStatus } from "@/lib/audit-api";

interface AuditStatusBadgeProps {
  status: AuditStatus;
}

export function AuditStatusBadge({ status }: AuditStatusBadgeProps) {
  const colors = {
    success: "bg-green-100 text-green-800",
    failed: "bg-red-100 text-red-800",
    skipped: "bg-gray-100 text-gray-800",
  };

  const labels = {
    success: "Success",
    failed: "Failed",
    skipped: "Skipped",
  };

  return (
    <span
      data-testid="audit-status-badge"
      className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}
    >
      {labels[status]}
    </span>
  );
}
