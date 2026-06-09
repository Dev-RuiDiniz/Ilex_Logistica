# Contrato de API Verificado - BETA-014A

## Endpoint

**Método:** GET
**URL:** /api/v1/shipments/analytics/carrier-efficiency

## Query Params Aceitos

- estimated_delivery_from: string | None (ISO 8601)
- estimated_delivery_to: string | None (ISO 8601)
- month: int | None
- year: int | None
- customer_name: string | None
- destination_uf: string | None
- carrier_id: int | None
- status: string | None
- criticality: string | None
- sla_status: string | None
- is_late: boolean | None

## Formato de Resposta

```typescript
{
  carriers: [
    {
      carrier_id: number;
      carrier_name: string | null;
      total_invoices: number;
      total_shipments: number;
      on_time_count: number;
      on_time_percentage: number;
      late_count: number;
      late_percentage: number;
      critical_count: number;
      lost_count: number;
      lost_percentage: number;
      total_freight_value: number;
      total_invoice_value: number;
      average_freight_percentage: number;
      average_freight_value: number;
      ranking_by_efficiency: number;
      ranking_by_cost: number;
      ranking_by_volume: number;
    }
  ];
  generated_at: string; // ISO 8601
}
```

## Métricas Retornadas

- carrier_id: ID da transportadora
- carrier_name: Nome da transportadora (pode ser null)
- total_invoices: Total de NFs
- total_shipments: Total de shipments
- on_time_count: Entregas no prazo
- on_time_percentage: Percentual de entregas no prazo
- late_count: Entregas atrasadas
- late_percentage: Percentual de entregas atrasadas
- critical_count: Entregas críticas
- lost_count: Extraviadas (sempre 0, status não existe no domínio)
- lost_percentage: Percentual de extraviadas (sempre 0)
- total_freight_value: Valor total do frete
- total_invoice_value: Valor total das NFs
- average_freight_percentage: Percentual médio do frete
- average_freight_value: Valor médio do frete
- ranking_by_efficiency: Ranking por eficiência (1 = melhor)
- ranking_by_cost: Ranking por custo (1 = melhor)
- ranking_by_volume: Ranking por volume (1 = melhor)
- generated_at: Data/hora de geração (ISO 8601)

## Observações

- lost_count e lost_percentage sempre retornam 0 (status de extraviada não existe no domínio)
- carrier_name pode ser null
- Rankings já calculados pelo backend, não recalcular no frontend
- Filtros SLA (sla_status, is_late) aplicados on-demand pelo backend
