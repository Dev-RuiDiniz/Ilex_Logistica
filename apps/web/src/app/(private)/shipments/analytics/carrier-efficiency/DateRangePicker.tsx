"use client";

import { useState } from "react";
import { parseISO, isValid } from "date-fns";

interface DateRangePickerProps {
  label: string;
  value: { from?: string; to?: string };
  onChange: (value: { from?: string; to?: string }) => void;
  placeholder?: { from?: string; to?: string };
}

export function DateRangePicker({
  label,
  value,
  onChange,
  placeholder = { from: "Data inicial", to: "Data final" },
}: DateRangePickerProps) {
  const [fromInput, setFromInput] = useState(value.from || "");
  const [toInput, setToInput] = useState(value.to || "");
  const [showFrom, setShowFrom] = useState(false);
  const [showTo, setShowTo] = useState(false);
  const [currentValue, setCurrentValue] = useState(value);

  const handleFromInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setFromInput(val);
    if (val.match(/^\d{4}-\d{2}-\d{2}$/) && isValid(parseISO(val))) {
      const newValue = { ...currentValue, from: val };
      setCurrentValue(newValue);
      onChange(newValue);
    } else if (!val) {
      const newValue = { ...currentValue, from: undefined };
      setCurrentValue(newValue);
      onChange(newValue);
    }
  };

  const handleToInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setToInput(val);
    if (val.match(/^\d{4}-\d{2}-\d{2}$/) && isValid(parseISO(val))) {
      const newValue = { ...currentValue, to: val };
      setCurrentValue(newValue);
      onChange(newValue);
    } else if (!val) {
      const newValue = { ...currentValue, to: undefined };
      setCurrentValue(newValue);
      onChange(newValue);
    }
  };

  // Simple popover-like dropdown for date picker
  // For simplicity, we'll use native date inputs with enhanced UX

  return (
    <div className="space-y-2">
      <label htmlFor="date-range-from" className="block text-sm font-medium">
        {label}
      </label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="relative">
          <input
            id="date-range-from"
            type="date"
            value={fromInput}
            onChange={handleFromInputChange}
            onFocus={() => setShowFrom(true)}
            onBlur={() => setTimeout(() => setShowFrom(false), 100)}
            placeholder={placeholder.from}
            className="w-full p-2 border rounded bg-white"
            max={toInput || undefined}
          />
          {showFrom && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded shadow-lg z-10 p-2">
              <div className="mb-1 text-xs text-slate-700">Início do período</div>
            </div>
          )}
        </div>
        <div className="relative">
          <input
            id="date-range-to"
            type="date"
            value={toInput}
            onChange={handleToInputChange}
            onFocus={() => setShowTo(true)}
            onBlur={() => setTimeout(() => setShowTo(false), 100)}
            placeholder={placeholder.to}
            className="w-full p-2 border rounded bg-white"
            min={fromInput || undefined}
          />
          {showTo && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-white border rounded shadow-lg z-10 p-2">
              <div className="mb-1 text-xs text-slate-700">Fim do período</div>
            </div>
          )}
        </div>
      </div>
      {(currentValue.from || currentValue.to) && (
        <button
          type="button"
          onClick={() => {
            setCurrentValue({});
            onChange({});
          }}
          className="text-sm text-blue-600 hover:text-blue-800 underline"
        >
          Limpar datas
        </button>
      )}
    </div>
  );
}
