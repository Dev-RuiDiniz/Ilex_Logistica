"use client";

import { useState } from "react";

interface SlaFiltersProps {
  slaStatus: string;
  isLate: "" | "true" | "false";
  onSlaStatusChange: (value: string) => void;
  onIsLateChange: (value: "" | "true" | "false") => void;
  disabled?: boolean;
}

export function SlaFilters({ slaStatus, isLate, onSlaStatusChange, onIsLateChange, disabled }: SlaFiltersProps) {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <div>
        <label className="block text-sm font-medium">Status SLA</label>
        <select
          value={slaStatus}
          onChange={(e) => onSlaStatusChange(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2 text-sm"
          disabled={disabled}
        >
          <option value="">Todos</option>
          <option value="on_time">No prazo</option>
          <option value="warning">Atenção</option>
          <option value="late">Atrasada</option>
          <option value="critical">Crítica</option>
          <option value="unknown">Sem SLA</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium">Atrasada</label>
        <select
          value={isLate}
          onChange={(e) => onIsLateChange(e.target.value as "" | "true" | "false")}
          className="mt-1 w-full rounded border px-3 py-2 text-sm"
          disabled={disabled}
        >
          <option value="">Todas</option>
          <option value="true">Sim</option>
          <option value="false">Não</option>
        </select>
      </div>
    </div>
  );
}
