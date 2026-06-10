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
        <span className="text-sm font-medium text-gray-700">{label}:</span>
        <pre className="mt-1 p-2 bg-gray-50 rounded text-xs text-gray-600 overflow-x-auto">
          {data}
        </pre>
      </div>
    );
  }

  return (
    <div data-testid={dataTestId} className="mt-2">
      <span className="text-sm font-medium text-gray-700">{label}:</span>
      <pre className="mt-1 p-2 bg-gray-50 rounded text-xs text-gray-600 overflow-x-auto max-h-64 overflow-y-auto">
        {JSON.stringify(parsed, null, 2)}
      </pre>
    </div>
  );
}
