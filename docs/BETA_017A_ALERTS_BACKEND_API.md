# BETA-017A: Alertas Backend/API

## Escopo

Implementação do backend do Épico 5 — Alertas e notificações — criando estrutura real de alertas operacionais, regras de geração, endpoints de listagem/contagem/marcação e integração com SLA, exceções e dashboard. Este PR é backend-only.

## Base Usada

BETA-016B - Dashboard Beta Frontend e UX Operacional

## Confirmação de Backend-Only

Este PR contém apenas alterações no backend (apps/api):
- Model/tabela: `app/modules/alerts/models.py`
- Migration: `migrations/versions/20260620_01_create_alerts.py`
- Service: `app/modules/alerts/service.py`
- Schemas: `app/modules/alerts/schemas.py`
- Router: `app/modules/alerts/router.py`
- Integração com dashboard: `app/modules/dashboard/service.py`
- Testes: `tests/test_alerts_model.py`, `tests/test_alerts_generation.py`, `tests/test_alerts_api.py`, `tests/test_dashboard_alerts_integration.py`

Nenhuma alteração foi feita no frontend (apps/web).

## Diagnóstico do Domínio Atual

### Entidades Existentes
- **Shipment**: shipments com SLA calculado (BETA-013A)
- **SlaRule**: regras de SLA por carrier/UF/global (BETA-013A)
- **ImportHistory**: histórico de importações com status
- **Carrier**: transportadoras

### Services Existentes
- **SLA service** (`app/modules/sla/service.py`): cálculo de SLA, atraso, status
- **Exceptions service** (`app/modules/shipments/exceptions_service.py`): classificação de exceções
- **Dashboard service** (`app/modules/dashboard/service.py`): KPIs operacionais

### Fontes Reais de Alertas
Alertas são gerados a partir de:
- Exceções críticas (SLA critical)
- Atrasos (SLA late)
- Atenção/warning (SLA warning)
- SLA unknown (quando não há regra ou dados)
- Falhas de importação (ImportHistory com status failed, não implementado nesta versão)

### Alertas Fora do Escopo
- Alertas por eficiência de transportadora (carrier_efficiency_drop) - não implementado
- Alertas por atualização antiga (no_update_count) - não implementado
- Alertas por entrega resolvida (resolved_count) - não implementado

## Model/Tabela Criada

**Tabela:** `alerts`

**Campos:**
- `id`: int (PK)
- `alert_type`: string (sla_critical, sla_late, sla_warning, unknown_sla, import_failure)
- `severity`: string (info, warning, critical)
- `title`: string
- `message`: text
- `source_type`: string (shipment, import)
- `source_id`: int (ID da origem)
- `shipment_id`: int (FK para shipments, opcional)
- `carrier_id`: int (FK para carriers, opcional)
- `status`: string (active, read, resolved, dismissed)
- `is_read`: boolean
- `is_resolved`: boolean
- `generated_at`: datetime
- `read_at`: datetime (opcional)
- `resolved_at`: datetime (opcional)
- `created_at`: datetime
- `updated_at`: datetime

**Índices:**
- alert_type, severity, status, source_type, source_id, shipment_id, carrier_id, generated_at

## Migration Criada

**Arquivo:** `migrations/versions/20260620_01_create_alerts.py`

**Validação:**
- ✅ `python -m pytest tests/test_migrations.py -v` (1/1 passed)

## Tipos de Alerta

- `sla_critical`: Atraso crítico (excede critical_delay_days)
- `sla_late`: Atraso (excede warning_threshold_days mas não critical)
- `sla_warning`: Atenção (próximo ao prazo)
- `unknown_sla`: SLA desconhecido (sem regra ou dados)
- `import_failure`: Falha de importação (não implementado nesta versão)

## Severidades

- `critical`: sla_critical
- `warning`: sla_late, sla_warning
- `info`: unknown_sla

## Status

- `active`: Alerta ativo e não resolvido
- `read`: Alerta lido pelo usuário
- `resolved`: Alerta resolvido
- `dismissed`: Alerta descartado (não usado nesta versão)

## Regras de Geração

1. **Idempotência**: Não duplica alerta ativo para a mesma origem
2. **Fontes**: Usa SLA service e exceptions service existentes
3. **Severidade coerente**: Mapeia SLA status para severidade correta
4. **Resolução automática**: Alertas são resolvidos quando condição não persiste (não implementado nesta versão)
5. **Sem recálculo duplicado**: Usa service de SLA existente, não recalcula regra
6. **Sem classificação duplicada**: Usa service de exceções existente

## Endpoints Criados

### GET /api/v1/alerts
Lista alertas com filtros.

**Filtros:**
- status, severity, alert_type, is_read, is_resolved, carrier_id, shipment_id
- limit, offset (paginação)

**Retorna:** AlertListResponse (alerts, total)

### GET /api/v1/alerts/summary
Retorna contadores de alertas.

**Retorna:** AlertSummaryResponse (total_alerts, active_count, read_count, resolved_count, critical_count, warning_count, info_count)

### POST /api/v1/alerts/generate
Gera/reprocessa alertas internos.

**Retorna:** AlertGenerationResponse (success, processed_count, created_count, skipped_count, resolved_count, error_count)

### PATCH /api/v1/alerts/{alert_id}/read
Marca alerta como lido.

**Retorna:** AlertMarkReadResponse (success, message)

### PATCH /api/v1/alerts/{alert_id}/resolve
Marca alerta como resolvido.

**Retorna:** AlertMarkResolvedResponse (success, message)

## Integração com Dashboard

**Alteração:** `app/modules/dashboard/service.py`

**Antes:**
```python
active_alerts_count = 0  # módulo não existe
```

**Depois:**
```python
from app.modules.alerts.service import get_active_alerts_count
active_alerts_count = get_active_alerts_count(db)
```

**Impacto:** Dashboard agora retorna contagem real de alertas ativos, ignorando resolvidos.

## Autenticação/Autorização

**Status atual:** Endpoints de alertas são públicos (sem auth) - gap documentado para Épico 9 (RBAC granular)

**Comportamento testado:** Sem RBAC granular ainda, endpoints são públicos para facilitar desenvolvimento beta

## Testes Criados

### test_alerts_model.py (9 testes)
- Cria alerta válido
- Valida alert_type
- Valida severity
- Valida status
- Cria alerta associado a shipment
- Evita campos obrigatórios ausentes
- Status default active
- is_read default False
- is_resolved default False

### test_alerts_generation.py (7 testes)
- Gera alerta para SLA critical
- Gera alerta para SLA late
- Gera alerta para SLA warning
- Não duplica alerta ativo para mesma origem
- Geração retorna contadores
- Respeita service de SLA existente
- Não usa dados reais

### test_alerts_api.py (8 testes)
- GET /alerts retorna lista
- GET /alerts/summary retorna contadores
- POST /alerts/generate gera alertas
- PATCH /alerts/{id}/read marca como lido
- PATCH /alerts/{id}/resolve marca como resolvido
- Filtros por status/severity/type funcionam
- Payload é estável para frontend
- Rota não conflita com rotas existentes

### test_dashboard_alerts_integration.py (3 testes)
- Dashboard summary retorna active_alerts_count real
- active_alerts_count ignora resolvidos
- Dashboard mantém payload estável

## Evidência de Red → Green → Refactor

1. **Red**: Testes criados antes da implementação
2. **Green**: Implementação do model, migration, service, schemas, router
3. **Refactor**: Ajustes para usar services existentes, correção de imports, integração com dashboard

## Comandos Executados

### Validações Python (raiz)
- python scripts/check_secrets.py --repo-root . ✅
- python scripts/check_secrets.py --repo-root . --self-test ✅
- python scripts/validate_migrations.py ✅
- python scripts/validate_docs.py ✅
- python scripts/beta_validate.py ✅

### Testes Backend (apps/api)
- python -m pytest tests/test_alerts_model.py -v ✅ (9/9 passed)
- python -m pytest tests/test_alerts_generation.py -v ✅ (7/7 passed)
- python -m pytest tests/test_alerts_api.py -v ✅ (8/8 passed)
- python -m pytest tests/test_dashboard_alerts_integration.py -v ✅ (3/3 passed)
- python -m pytest tests/test_dashboard_summary.py -v ✅ (25/25 passed)
- python -m pytest tests/test_dashboard_api.py -v ✅ (5/5 passed)
- python -m pytest tests/test_exceptions_panel_sla.py -v ✅ (30/30 passed)
- python -m pytest tests/test_exceptions_panel_api.py -v ✅ (5/5 passed)
- python -m pytest tests/test_carrier_efficiency_report.py -v ✅ (26/26 passed)
- python -m pytest tests/test_carrier_efficiency_api.py -v ✅ (4/4 passed)
- python -m pytest tests/test_sla_calculation.py -v ✅ (14/14 passed)
- python -m pytest tests/test_sla_rules.py -v ✅ (27/27 passed)
- python -m pytest tests/test_sla_api.py -v -rs ✅ (5/5 passed)
- python -m pytest tests/test_braspress_assisted_import.py -v -rs ✅ (29/29 passed)

### Validações Frontend (apps/web)
- npm run lint ✅ (0 errors, 7 warnings)
- npm run test ✅ (206/206 passed)
- npm run build ✅

## Resultados

- ✅ Secrets check: OK
- ✅ Migrations: OK
- ✅ Docs: OK
- ✅ Beta validation: OK
- ✅ Frontend tests total: 206/206 passed
- ✅ Backend tests alerts: 27/27 passed
- ✅ Backend tests dashboard: 30/30 passed
- ✅ Backend tests críticos: 192/192 passed
- ✅ Lint: 0 errors
- ✅ Build: sucesso

## Limitações

- Sem e-mail (fora do escopo beta)
- Sem WhatsApp (fora do escopo beta)
- Sem webhook externo (fora do escopo beta)
- Sem push notification (fora do escopo beta)
- Sem relatório diário (já existe endpoint separado)
- Sem auditoria completa (Épico 7)
- Sem frontend (BETA-017B)
- Sem RBAC granular (Épico 9)
- Alertas por eficiência de transportadora não implementados
- Alertas por atualização antiga não implementados
- Resolução automática de alertas não implementada

## O Que Fica Para BETA-017B

- Frontend de alertas
- Badges/ícone no dashboard
- Filtros visuais
- Ações de ler/resolver

## O Que Fica Para Épicos Posteriores

- E-mail/WhatsApp/webhook (Épico 5 - segunda parte)
- Relatório diário (Épico 6)
- Auditoria completa (Épico 7)
- RBAC granular (Épico 9)

## Governança

- ✅ Sem merge em main
- ✅ Sem auto-merge
- ✅ Sem force push
- ✅ Sem comando destrutivo
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
