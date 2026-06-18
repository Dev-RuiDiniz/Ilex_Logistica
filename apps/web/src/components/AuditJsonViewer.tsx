interface AuditJsonViewerProps {
  data: string | null;
  label: string;
  dataTestId?: string;
}

export function AuditJsonViewer({ data, label, dataTestId }: AuditJsonViewerProps) {
  if (!data) {
    return null;
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(data);
  } catch {
    return (
      <div data-testid={dataTestId} className="mt-2">
        <span className="text-sm font-medium text-slate-800">{label}:</span>
        <pre className="mt-1 rounded bg-slate-50 p-2 text-xs text-slate-700 overflow-x-auto">
          {data}
        </pre>
      </div>
    );
  }

  return (
    <div data-testid={dataTestId} className="mt-2">
      <span className="text-sm font-medium text-slate-800">{label}:</span>
      <pre className="mt-1 max-h-64 overflow-y-auto rounded bg-slate-50 p-2 text-xs text-slate-700 overflow-x-auto">
        {JSON.stringify(parsed, null, 2)}
      </pre>
    </div>
  );
}
