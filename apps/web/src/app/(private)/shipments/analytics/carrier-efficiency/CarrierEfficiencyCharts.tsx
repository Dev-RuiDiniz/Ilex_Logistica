"use client";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";
import type { CarrierEfficiencyItem } from "@/lib/types";

interface CarrierEfficiencyChartsProps {
  data: CarrierEfficiencyItem[] | null;
}

const COLORS = {
  onTime: "#22c55e",
  late: "#ef4444",
  efficiency: "#3b82f6",
  cost: "#f59e0b",
  volume: "#8b5cf6",
};

export function CarrierEfficiencyCharts({ data }: CarrierEfficiencyChartsProps) {
  if (!data || data.length === 0) {
    return <div className="text-center py-8 text-gray-500">Sem dados para exibir gráficos</div>;
  }

  // Prepare data for charts
  const efficiencyData = data.map((carrier) => ({
    name: carrier.carrier_name || `ID ${carrier.carrier_id}`,
    "No Prazo": carrier.on_time_percentage,
    Atrasadas: carrier.late_percentage,
    "Frete %": carrier.average_freight_percentage,
  }));

  const volumeData = data.map((carrier) => ({
    name: carrier.carrier_name || `ID ${carrier.carrier_id}`,
    Volume: carrier.total_shipments,
    Frete: carrier.total_freight_value / 1000, // em milhares
  }));

  const rankingData = [...data]
    .sort((a, b) => a.ranking_by_efficiency - b.ranking_by_efficiency)
    .map((carrier) => ({
      name: carrier.carrier_name || `ID ${carrier.carrier_id}`,
      "Ranking Eficiência": carrier.ranking_by_efficiency,
      "Ranking Custo": carrier.ranking_by_cost,
      "Ranking Volume": carrier.ranking_by_volume,
    }));

  return (
    <div className="space-y-8">
      {/* Gráfico 1: Eficiência (Barras empilhadas) */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Eficiência por Transportadora (%)</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={efficiencyData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
              <YAxis type="category" dataKey="name" width={120} />
              <Tooltip
                formatter={(value: unknown, name: unknown) => [
                  typeof value === "number" ? `${value.toFixed(1)}%` : "-",
                  String(name || ""),
                ]}
              />
              <Legend />
              <Bar dataKey="No Prazo" fill={COLORS.onTime} radius={[0, 4, 4, 0]} />
              <Bar dataKey="Atrasadas" fill={COLORS.late} radius={[4, 0, 0, 4]} />
              <Bar dataKey="Frete %" fill={COLORS.efficiency} radius={[4, 0, 0, 4]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico 2: Volume vs Frete */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Volume de Entregas vs Frete Total</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={volumeData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="name" width={120} />
              <Tooltip
                formatter={(value: unknown, name: unknown) => {
                  if (name === "Frete" && typeof value === "number")
                    return [`R$ ${(value * 1000).toLocaleString("pt-BR")}`, String(name)];
                  return [typeof value === "number" ? value.toString() : "-", String(name || "")];
                }}
              />
              <Legend />
              <Bar dataKey="Volume" fill={COLORS.volume} radius={[0, 4, 4, 0]} />
              <Bar dataKey="Frete" fill={COLORS.cost} radius={[4, 0, 0, 4]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico 3: Rankings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Rankings Comparativos</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rankingData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                domain={[0, "auto"]}
                reversed
                tickFormatter={(v) => `#${v}`}
              />
              <YAxis type="category" dataKey="name" width={120} />
              <Tooltip
                formatter={(value: unknown) => [`#${typeof value === "number" ? value : "-"}`, "Posição no Ranking"]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="Ranking Eficiência"
                stroke={COLORS.efficiency}
                strokeWidth={3}
                dot={{ r: 6, strokeWidth: 2 }}
                activeDot={{ r: 8, strokeWidth: 3 }}
              />
              <Line
                type="monotone"
                dataKey="Ranking Custo"
                stroke={COLORS.cost}
                strokeWidth={3}
                dot={{ r: 6, strokeWidth: 2 }}
                activeDot={{ r: 8, strokeWidth: 3 }}
              />
              <Line
                type="monotone"
                dataKey="Ranking Volume"
                stroke={COLORS.volume}
                strokeWidth={3}
                dot={{ r: 6, strokeWidth: 2 }}
                activeDot={{ r: 8, strokeWidth: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico 4: Top 5 Transportadoras por Eficiência */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Top 5 - Maior Eficiência (On-Time %)</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data
                .sort((a, b) => b.on_time_percentage - a.on_time_percentage)
                .slice(0, 5)
                .map((c) => ({
                  name: c.carrier_name || `ID ${c.carrier_id}`,
                  Eficiência: c.on_time_percentage,
                }))}
              layout="vertical"
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
              <YAxis type="category" dataKey="name" width={150} />
              <Tooltip formatter={(value: unknown) => [`${typeof value === "number" ? value.toFixed(1) : "-"}%`, "Eficiência"]} />
              <Bar
                dataKey="Eficiência"
                radius={[0, 4, 4, 0]}
              >
                {data
                  .sort((a, b) => b.on_time_percentage - a.on_time_percentage)
                  .slice(0, 5)
                  .map((_, index) => (
                    <Cell key={`cell-${index}`} />
                  ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
