import { formatSlaStatusLabel, getSlaStatusBadgeColor } from "@/lib/sla-helpers";

interface SlaBadgeProps {
  status: string | null;
}

export function SlaBadge({ status }: SlaBadgeProps) {
  if (!status) {
    return <span className="text-slate-400">-</span>;
  }

  return (
    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${getSlaStatusBadgeColor(status)}`}>
      {formatSlaStatusLabel(status)}
    </span>
  );
}
