# BETA-015A: Painel de Exceções com SLA - Backend/API

## Escopo

Implementação do backend do painel de exceções operacionais com regras de SLA, usando dados já criados nos épicos anteriores (SLA, criticidade, importação, campos fiscais/financeiros e eficiência por transportadora).

## Base Técnica

- **Branch:** `feature/beta-015a-exceptions-panel-sla-backend`
- **Base:** `feature/beta-014b-carrier-efficiency-frontend`
- **Tipo:** Backend-only (sem frontend)

## Diagnóstico do Painel de Exceções Existente

### Campos Já Existentes

No model `Shipment` (apps/api/app/modules/shipments/models.py):
- `id`: ID do shipment
- `tracking_code`: Código de rastreamento
- `carrier_id`: ID da transportadora
- `status`: Status da entrega
- `estimated_delivery`: Data estimada de entrega
- `actual_delivery`: Data real de entrega
- `invoice_number`: Número da nota fiscal
- `invoice_key`: Chave da nota fiscal
- `fiscal_document`: Documento fiscal
- `amount`: Valor
- `due_date`: Data de vencimento
- `delay_days`: Dias de atraso
- `criticality`: Criticidade (normal, baixa, media, alta)
- `freight_value`: Valor do frete
- `invoice_value`: Valor da nota fiscal
- `freight_percentage`: Percentual do frete
- `collection_departure_date`: Data de coleta
- `customer_name`: Nome do cliente
- `destination_uf`: UF de destino
- `created_at`: Data de criação
- `updated_at`: Data de atualização

Campos de SLA (calculados on-demand via `calculate_shipment_sla`):
- `sla_due_date`: Data de vencimento do SLA
- `sla_status`: Status do SLA (on_time, warning, late, critical, unknown)
- `is_late`: Se está atrasado
- `sla_rule_id`: ID da regra de SLA aplicada

### Exceções Que Já Aparecem Hoje

Endpoint existente: `GET /api/v1/shipments/exceptions`
- Filtro: `(delay_days > 0) OR (criticality != "normal")`
- Ordenação: `delay_days DESC`
- Payload: Lista de shipments com campos básicos
- Limitação: Não usa SLA, não tem priorização, não tem resumo

### Novas Exceções Calculadas

Com base em SLA e criticidade:
1. **critical**: sla_status = "critical" (mais urgente)
2. **late**: sla_status = "late" ou criticality in ("media", "alta")
3. **warning**: sla_status = "warning" ou criticality = "baixa"
4. **unknown_sla**: sla_status = "unknown" (sem SLA definido)

### Endpoints Criados/Ajustados

**Novo endpoint:** `GET /api/v1/shipments/analytics/exceptions`
- Path: `/api/v1/shipments/analytics/exceptions`
- Response: `ExceptionsPanelResponse`
- Query params: período, mês, ano, cliente, UF, transportadora, status, criticality, sla_status, is_late, exception_type
- Payload: summary, items, filters_applied, generated_at

**Endpoint mantido:** `GET /api/v1/shipments/exceptions`
- Continua existindo para compatibilidade
- Não foi alterado neste PR

## Implementação

### Service de Exceções Operacionais

**Arquivo:** `apps/api/app/modules/shipments/exceptions_service.py`

**Funções principais:**

1. `classify_exception_type(sla_status, criticality, is_late)`
   - Classifica o tipo de exceção baseado em SLA e criticidade
   - Retorna: "critical", "late", "warning", "unknown_sla" ou None

2. `calculate_exception_priority(exception_type, delay_days, estimated_delivery, id)`
   - Calcula prioridade numérica para ordenação
   - Prioridade: critical (1) < late (2) < warning (3) < unknown_sla (4)
   - Empates: maior delay_days, data mais antiga, ID menor

3. `calculate_exception_summary(items)`
   - Calcula resumo operacional das exceções
   - Retorna: total_exceptions, critical_count, late_count, warning_count, unknown_sla_count

4. `get_exception_items(db, filters...)`
   - Retorna lista de exceções com filtros aplicados
   - Calcula SLA on-demand via `calculate_shipment_sla`
   - Classifica exceções e calcula prioridade
   - Ordena por prioridade

5. `get_exceptions_panel(db, filters...)`
   - Retorna painel completo com resumo e lista
   - Payload: summary, items, filters_applied, generated_at

### Schemas/DTO

**Arquivo:** `apps/api/app/modules/shipments/analytics_schemas.py`

**Novos schemas:**

1. `ExceptionSummary`
   - total_exceptions: int
   - critical_count: int
   - late_count: int
   - warning_count: int
   - unknown_sla_count: int

2. `ExceptionItem`
   - shipment_id: int
   - tracking_code: str
   - invoice_number: str | None
   - carrier_id: int
   - carrier_name: str | None
   - customer_name: str | None
   - destination_uf: str | None
   - status: str
   - sla_status: str | None
   - criticality: str
   - delay_days: int
   - sla_due_date: datetime | None
   - exception_type: str
   - exception_reason: str
   - priority: int
   - last_update_at: datetime

3. `ExceptionsPanelResponse`
   - summary: ExceptionSummary
   - items: list[ExceptionItem]
   - filters_applied: dict[str, Any]
   - generated_at: datetime

### Endpoint

**Arquivo:** `apps/api/app/modules/shipments/router.py`

**Novo endpoint:**
```python
@router.get("/analytics/exceptions", response_model=ExceptionsPanelResponse)
def get_exceptions_analytics(
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    month: int | None = None,
    year: int | None = None,
    customer_name: str | None = None,
    destination_uf: str | None = None,
    carrier_id: int | None = None,
    status: str | None = None,
    criticality: str | None = None,
    sla_status: str | None = None,
    is_late: bool | None = None,
    exception_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExceptionsPanelResponse
```

### Autenticação/Autorização

- **Autenticação:** Exigida via `get_current_user`
- **Autorização:** Segue padrão atual (sem RBAC granular)
- **Gap documentado:** Épico 9 (RBAC granular) ainda não implementado

## Tipos de Exceção

### critical
- **Definição:** sla_status = "critical"
- **Prioridade:** 1 (mais urgente)
- **Razão:** "Atraso crítico de {delay_days} dias"

### late
- **Definição:** sla_status = "late" ou criticality in ("media", "alta")
- **Prioridade:** 2
- **Razão:** "Atraso de {delay_days} dias"

### warning
- **Definição:** sla_status = "warning" ou criticality = "baixa"
- **Prioridade:** 3
- **Razão:** "Atenção: próximo ao prazo"

### unknown_sla
- **Definição:** sla_status = "unknown"
- **Prioridade:** 4 (menos urgente)
- **Razão:** "Sem SLA definido"

### on_time (sem exceção)
- **Definição:** sla_status = "on_time" e criticality = "normal"
- **Prioridade:** N/A (não é exceção)
- **Razão:** N/A

## Regras de Priorização

1. **critical** antes de **late**
2. **late** antes de **warning**
3. **warning** antes de **unknown_sla**
4. Empate por maior **delay_days**
5. Empate por data mais antiga
6. Empate por ID menor

## Filtros Suportados

- **Período:** estimated_delivery_from, estimated_delivery_to
- **Mês/Ano:** month, year
- **Cliente:** customer_name
- **UF:** destination_uf
- **Transportadora:** carrier_id
- **Status:** status
- **Criticidade:** criticality
- **Status SLA:** sla_status
- **Atrasado:** is_late
- **Tipo de exceção:** exception_type

## Payload de Resposta

```json
{
  "summary": {
    "total_exceptions": 10,
    "critical_count": 2,
    "late_count": 5,
    "warning_count": 2,
    "unknown_sla_count": 1
  },
  "items": [
    {
      "shipment_id": 1,
      "tracking_code": "ABC123",
      "invoice_number": "NF123",
      "carrier_id": 1,
      "carrier_name": "Transportadora A",
      "customer_name": "Cliente X",
      "destination_uf": "SP",
      "status": "delivered",
      "sla_status": "critical",
      "criticality": "alta",
      "delay_days": 15,
      "sla_due_date": "2025-01-01T00:00:00Z",
      "exception_type": "critical",
      "exception_reason": "Atraso crítico de 15 dias",
      "priority": 199850,
      "last_update_at": "2025-01-15T00:00:00Z"
    }
  ],
  "filters_applied": {
    "carrier_id": 1,
    "sla_status": "critical"
  },
  "generated_at": "2025-01-15T00:00:00Z"
}
```

## Testes

### Service Tests (test_exceptions_panel_sla.py)

**30 testes implementados:**
- Deve listar entregas críticas
- Deve listar entregas atrasadas
- Deve listar entregas warning/atenção
- Deve listar entregas sem SLA como unknown
- Deve não listar entregas no prazo sem exceção
- Deve calcular resumo por tipo de exceção
- Deve priorizar critical antes de late
- Deve ordenar por maior atraso
- Deve aplicar filtro por carrier_id
- Deve aplicar filtro por destination_uf
- Deve aplicar filtro por customer_name
- Deve aplicar filtro por criticality
- Deve aplicar filtro por sla_status
- Deve aplicar filtro por is_late
- Deve aplicar filtro por exception_type
- Deve retornar payload estável para frontend
- Deve retornar lista vazia quando não houver exceções
- Deve respeitar autenticação/autorização existente
- Deve não duplicar regra de SLA
- Deve lidar com registros antigos sem SLA
- test_classify_exception_type_critical
- test_classify_exception_type_late
- test_classify_exception_type_warning
- test_classify_exception_type_unknown
- test_classify_exception_type_on_time
- test_calculate_exception_priority_critical
- test_calculate_exception_priority_late
- test_calculate_exception_priority_warning
- test_calculate_exception_priority_unknown
- test_calculate_exception_priority_empate_por_maior_delay

### API Tests (test_exceptions_panel_api.py)

**5 testes implementados:**
- GET do endpoint retorna 200
- Endpoint retorna summary/items/generated_at
- Query params são aplicados
- Rota não conflita com rota dinâmica de shipments
- Usuário sem auth é bloqueado se o padrão atual exigir auth

### Fixture Adicionado

**Arquivo:** `apps/api/tests/conftest.py`

**Novo fixture:** `auth_headers`
- Cria usuário com role admin
- Faz login e retorna Bearer token
- Usado em testes de API que exigem autenticação

## Limitações

### Não Implementado Neste PR

- **Frontend:** Painel frontend de exceções com filtros e priorização visual (BETA-015B)
- **Alertas/e-mail:** Notificações de exceções (épico próprio)
- **Relatório diário:** Relatório automático de exceções (épico próprio)
- **Auditoria completa:** Logs detalhados de ações (épico próprio)
- **Filtros adicionais:** only_untreated (tratativas ainda não integradas)
- **Import failures:** Falhas de importação não integradas
- **No update:** Sem atualização não integrado
- **RBAC granular:** Épico 9 ainda não implementado

### Limitações do Domínio

- **Tratativas:** Modelo `ShipmentTreatment` existe mas não foi integrado ao painel
- **Import history:** Modelo `ImportHistory` existe mas não foi integrado ao painel
- **Last update:** Campo `updated_at` existe mas não há lógica de "sem atualização"

## Evidência de Red → Green → Refactor

### Red
- Testes criados antes da implementação
- test_exceptions_panel_sla.py: 30 testes
- test_exceptions_panel_api.py: 5 testes

### Green
- Service implementado: exceptions_service.py
- Schemas implementados: analytics_schemas.py
- Endpoint implementado: router.py
- Fixture implementado: conftest.py
- Todos os testes passam

### Refactor
- Prioridade simplificada para base_priority * 10000 + delay_priority
- Classificação de exceção centralizada em classify_exception_type
- Reuso de calculate_shipment_sla (sem duplicação)

## Arquivos Criados

- `apps/api/app/modules/shipments/exceptions_service.py` (354 linhas)
- `apps/api/tests/test_exceptions_panel_sla.py` (216 linhas)
- `apps/api/tests/test_exceptions_panel_api.py` (58 linhas)

## Arquivos Modificados

- `apps/api/app/modules/shipments/analytics_schemas.py` (adicionados 3 schemas)
- `apps/api/app/modules/shipments/router.py` (adicionado endpoint)
- `apps/api/tests/conftest.py` (adicionado fixture auth_headers)

## Confirmação de Backend-Only

- Nenhum arquivo frontend modificado
- Nenhum componente React criado
- Nenhum teste frontend criado
- Foco exclusivo em backend/API

## O Que Fica Para BETA-015B

- Painel frontend de exceções com filtros e priorização visual
- API client para consumir o endpoint
- Componentes de UI para exibir exceções
- Filtros visuais
- KPIs visuais

## O Que Fica Para Épicos Posteriores

- Alertas/e-mail de exceções
- Relatório diário de exceções
- Auditoria completa de ações
- RBAC granular (Épico 9)
- Integração com tratativas
- Integração com import history
- Lógica de "sem atualização"
