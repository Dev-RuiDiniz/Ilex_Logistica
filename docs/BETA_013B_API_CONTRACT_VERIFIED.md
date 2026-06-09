# BETA-013B: Contrato de API Verificado (BETA-013A)

## Tarefa 0 - Verificação do Contrato Backend

### 1. Campos de SLA na Listagem

**Endpoint:** GET /api/v1/shipments

**Campos SLA calculados on-demand:**
- `sla_due_date` (datetime | null): Data limite SLA
- `sla_status` (string | null): Status SLA (on_time, warning, late, critical, unknown)
- `is_late` (boolean): Se está atrasado
- `sla_rule_id` (int | null): ID da regra aplicada

**Campos existentes preservados:**
- `delay_days` (int): Atraso em dias
- `criticality` (string): Criticidade (normal, baixa, alta)
- `estimated_delivery` (datetime): Data estimada de entrega
- `collection_departure_date` (datetime | null): Data de coleta
- `carrier_id` (int): ID da transportadora
- `destination_uf` (string | null): UF de destino
- `status` (string): Status da entrega
- Campos fiscais/financeiros do BETA-011A preservados

### 2. Campos de SLA no Detalhe

**Endpoint:** GET /api/v1/shipments/{id}

**Campos:** Mesmos da listagem (não há campos adicionais específicos do detalhe)

### 3. Filtros Aceitos

**Endpoint:** GET /api/v1/shipments

**Filtros SLA:**
- `sla_status` (string | null): on_time, warning, late, critical, unknown
- `is_late` (boolean | null): true, false

**Filtros existentes preservados:**
- `status` (string | null)
- `carrier_id` (int | null)
- `tracking_code` (string | null)
- `invoice_number` (string | null)
- `fiscal_document` (string | null)
- `criticality` (string | null)
- `estimated_delivery_from` (string | null)
- `estimated_delivery_to` (string | null)
- `due_date_from` (string | null)
- `due_date_to` (string | null)
- `customer_name` (string | null)
- `destination_uf` (string | null)
- `month` (int | null)
- `year` (int | null)
- `search` (string | null)

### 4. Endpoints de Regras SLA

**Base URL:** /api/v1/sla

**Endpoints:**
- `GET /api/v1/sla/rules`: Listar regras SLA
  - Query params: `carrier_id` (int | null), `destination_uf` (string | null), `is_active` (boolean | null)
  - Response: Array de regras com campos: id, carrier_id, destination_uf, transit_days, warning_threshold_days, critical_delay_days, is_active, created_at, updated_at

- `POST /api/v1/sla/rules`: Criar regra SLA (admin only)
  - Body: { carrier_id (int | null), destination_uf (string | null), transit_days (int, gt=0), warning_threshold_days (int, gt=0), critical_delay_days (int, gt=0), is_active (boolean) }
  - Response: Regra criada com todos os campos

- `PUT /api/v1/sla/rules/{rule_id}`: Atualizar regra SLA (admin only)
  - Body: { carrier_id (int | null), destination_uf (string | null), transit_days (int | null, gt=0), warning_threshold_days (int | null, gt=0), critical_delay_days (int | null, gt=0), is_active (boolean | null) }
  - Response: Regra atualizada com todos os campos

- `POST /api/v1/sla/recalculate`: Reprocessar SLA de todas as shipments
  - Query params: `carrier_id` (int | null), `destination_uf` (string | null)
  - Response: { processed_count, updated_count, skipped_count, error_count }

- `POST /api/v1/sla/recalculate/{shipment_id}`: Reprocessar SLA de uma shipment específica
  - Response: { processed_count, updated_count, skipped_count, error_count }

### 5. Autenticação e RBAC

**Autenticação:** JWT token via header Authorization: Bearer {token}

**RBAC:**
- Endpoints de listagem exigem autenticação (get_current_user)
- Endpoints de criação/alteração de regras exigem role "admin" (require_roles(["admin"]))
- Reprocessamento exige autenticação

### 6. Observações Importantes

- Cálculo SLA é on-demand (não persistido no banco)
- Filtros SLA são aplicados em memória após paginação (pode afetar performance em grandes volumes)
- `sla_calculated_at` não é exposto na API (apenas cálculo on-demand)
- Regra de prioridade: carrier_id + destination_uf > carrier_id > global
- Regras inativas são ignoradas no cálculo
