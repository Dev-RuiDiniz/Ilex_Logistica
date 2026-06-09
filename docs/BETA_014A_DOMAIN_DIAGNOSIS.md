# Diagnóstico do Domínio - BETA-014A

## Campos Usados para Cálculo

**No prazo:**
- `sla_status == "on_time"` (BETA-013A)
- `is_late == False` (BETA-013A)

**Atraso:**
- `is_late == True` (BETA-013A)
- `delay_days > 0`

**Críticas:**
- `criticality == "alta"` (BETA-011A)
- `sla_status == "critical"` (BETA-013A)

## Extraviadas

**Status existentes no domínio:**
- `pending`, `in_transit`, `delivered`, `failed`

**Status de extraviada:**
- Não existe status de extraviada/lost/missing no domínio
- Vou retornar `lost_count = 0` e documentar que status operacional de extravio ainda não está modelado
- Não vou inventar dado falso

## Filtros Reaproveitados

**Filtros existentes em shipments (BETA-013A + BETA-011A):**
- `status`, `carrier_id`, `tracking_code`, `invoice_number`, `fiscal_document`, `criticality`
- `estimated_delivery_from`, `estimated_delivery_to`, `due_date_from`, `due_date_to`
- `customer_name`, `destination_uf`, `month`, `year`, `search`
- `sla_status`, `is_late` (BETA-013A)

**Filtros a serem aplicados no endpoint de eficiência:**
- Período: `estimated_delivery_from`, `estimated_delivery_to`
- Mês/Ano: `month`, `year`
- Cliente: `customer_name`
- UF: `destination_uf`
- Transportadora: `carrier_id`
- Status: `status`
- Criticality: `criticality`
- SLA Status: `sla_status`
- Is Late: `is_late`

## Campos Fiscais/Financeiros (BETA-011A)

- `freight_value`: valor do frete
- `invoice_value`: valor da NF
- `freight_percentage`: percentual do frete (calculado automaticamente)
- `collection_departure_date`: data de coleta/saída
- `customer_name`: nome do cliente
- `destination_uf`: UF de destino

## SLA/Criticality (BETA-013A)

- `delay_days`: dias de atraso
- `criticality`: criticidade (normal, baixa, média, alta)
- `sla_due_date`: data limite SLA (calculado on-demand)
- `sla_status`: status SLA (on_time, warning, late, critical, unknown)
- `is_late`: está atrasada (boolean)
- `sla_rule_id`: ID da regra SLA aplicada
