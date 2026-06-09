"use client";

import { useEffect, useState } from "react";
import { getCarrierEfficiency } from "@/lib/api";
import type { CarrierEfficiencyResponse, CarrierEfficiencyFilters } from "@/lib/types";

export default function CarrierEfficiencyPage() {
  const [data, setData] = useState<CarrierEfficiencyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters] = useState<CarrierEfficiencyFilters>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem("accessToken") || "";
        const result = await getCarrierEfficiency(token, filters);
        setData(result);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro ao carregar dados");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>Erro: {error}</div>;
  }

  if (!data || data.carriers.length === 0) {
    return <div>Sem dados</div>;
  }

  return (
    <div>
      <h1>Eficiência por Transportadora</h1>
      <table>
        <thead>
          <tr>
            <th>Transportadora</th>
            <th>Total NFs</th>
            <th>Total Entregas</th>
            <th>No Prazo</th>
            <th>Atrasadas</th>
            <th>Frete Total</th>
            <th>Frete Médio</th>
            <th>Ranking Eficiência</th>
            <th>Ranking Custo</th>
            <th>Ranking Volume</th>
          </tr>
        </thead>
        <tbody>
          {data.carriers.map((carrier) => (
            <tr key={carrier.carrier_id}>
              <td>{carrier.carrier_name || "-"}</td>
              <td>{carrier.total_invoices}</td>
              <td>{carrier.total_shipments}</td>
              <td>{carrier.on_time_percentage}%</td>
              <td>{carrier.late_percentage}%</td>
              <td>R$ {carrier.total_freight_value.toFixed(2)}</td>
              <td>{carrier.average_freight_percentage}%</td>
              <td>{carrier.ranking_by_efficiency}</td>
              <td>{carrier.ranking_by_cost}</td>
              <td>{carrier.ranking_by_volume}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
