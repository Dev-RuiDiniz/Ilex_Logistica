# Diagnóstico do Domínio Existente - BETA-013A

## Campos Já Existentes no Shipment

### Campos de Data
- `estimated_delivery` (DateTime) - data estimada de entrega (obrigatório)
- `actual_delivery` (DateTime | None) - data real de entrega (nullable)
- `due_date` (DateTime | None) - data de vencimento fiscal (nullable)
- `collection_departure_date` (DateTime | None) - data de coleta/saída (nullable, BETA-011A)

### Campos de SLA/Criticidade
- `delay_days` (Integer, default=0) - dias de atraso calculados baseado em `due_date`
- `criticality` (String, default="normal") - criticidade operacional

### Campos de Identificação
- `tracking_code` (String) - código de rastreio
- `invoice_number` (String | None) - número da NF
- `carrier_id` (Integer) - ID da transportadora
- `destination_uf` (String | None) - UF de destino

### Outros Campos
- `status` (String) - status do shipment
- `customer_name` (String | None) - nome do cliente (BETA-011A)
- `freight_value` (Numeric | None) - valor do frete (BETA-011A)
- `invoice_value` (Numeric | None) - valor da NF (BETA-011A)
- `freight_percentage` (Numeric | None) - percentual do frete (BETA-011A)

## Funções Já Existentes em service.py

### calculate_delay_days(due_date, reference_date)
- Calcula atraso baseado em `due_date` (data fiscal de vencimento)
- Retorna max(0, delta.days)
- Usa `due_date` como referência, não `estimated_delivery`

### classify_criticality(delay_days, amount)
- Classifica criticidade baseado em `delay_days`
- Valores retornados: "normal", "baixa", "media", "alta"
- Regras:
  - delay_days == 0 → "normal"
  - delay_days <= 7 → "baixa"
  - delay_days <= 30 → "media"
  - delay_days > 30 → "alta"

## Filtros Já Implementados (BETA-011A)

Em `list_shipments()`:
- status
- carrier_id
- tracking_code
- invoice_number
- fiscal_document
- criticality
- estimated_delivery_from/to
- due_date_from/to
- customer_name
- destination_uf
- month/year
- search

## Campos que Serão Reaproveitados

- `estimated_delivery` - pode ser usado como `sla_due_date` se já estiver preenchido
- `actual_delivery` - pode ser usado como `delivered_at`
- `collection_departure_date` - usado para calcular SLA quando `estimated_delivery` não existe
- `delay_days` - será recalculado baseado em SLA operacional
- `criticality` - será recalculado com novos valores/status

## Novos Campos/Tabelas Necessários

### Tabela SlaRule (nova)
- id
- carrier_id (opcional)
- destination_uf (opcional)
- transit_days (obrigatório)
- warning_threshold_days (obrigatório)
- critical_delay_days (obrigatório)
- is_active (default=True)
- created_at
- updated_at

### Campos adicionais no Shipment
- `sla_due_date` (DateTime | None) - data de vencimento SLA operacional
- `sla_status` (String | None) - status SLA: "on_time", "warning", "late", "critical", "unknown"
- `is_late` (Boolean, default=False) - flag se está atrasado
- `sla_rule_id` (Integer | None) - ID da regra SLA aplicada
- `sla_calculated_at` (DateTime | None) - timestamp do último cálculo SLA

## Nomes Reais Usados

O projeto já usa:
- `criticality` com valores: "normal", "baixa", "media", "alta"
- `delay_days` como campo calculado
- `due_date` como data fiscal de vencimento

Para BETA-013A, adaptaremos:
- `sla_status` com valores: "on_time", "warning", "late", "critical", "unknown"
- `sla_due_date` para data de vencimento SLA operacional (diferente de `due_date` fiscal)
- `is_late` como flag booleana
- Manter `criticality` existente mas recalculá-lo com base em SLA

## Diferença Entre SLA Operacional e Fiscal

- **SLA Fiscal (due_date):** Data de vencimento da nota fiscal, para pagamento
- **SLA Operacional (sla_due_date):** Data de entrega prometida ao cliente, para operação logística

O BETA-013A foca em SLA operacional, não fiscal.
