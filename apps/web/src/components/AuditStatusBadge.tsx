import type { AuditStatus } from "@/lib/audit-api";

interface AuditStatusBadgeProps {
  status: AuditStatus;
}

export function AuditStatusBadge({ status }: AuditStatusBadgeProps) {
  const styles: Record<string, string> = {
    success: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-600/20",
    failed: "bg-red-50 text-red-700 ring-1 ring-red-600/20",
    skipped: "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20",
  };

  const labels: Record<string, string> = {
    success: "Success",
    failed: "Failed",
    skipped: "Skipped",
  };

  return (
    <span
      data-testid="audit-status-badge"
      className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold ${styles[status] || "bg-zinc-100 text-zinc-600 ring-1 ring-zinc-500/20"}`}
    >
      {labels[status] || status}
    </span>
  );
}
