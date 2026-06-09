# BETA-016A: Dashboard Beta Backend/API

## Escopo

Implementação do backend do Épico 10 — Dashboard beta e UX operacional, criando endpoints de resumo operacional com KPIs reais, filtros globais e payload estável para o frontend.

## Base Usada

BETA-015B - Painel Frontend de Exceções com SLA e Priorização Visual

## Confirmação de Backend-Only

Este PR contém apenas alterações no backend (apps/api):
- Service: `app/modules/dashboard/service.py`
- Schemas: `app/modules/dashboard/schemas.py`
- Router: `app/modules/dashboard/router.py`
- Testes: `tests/test_dashboard_summary.py`, `tests/test_dashboard_api.py`

Nenhuma alteração foi feita no frontend (apps/web).

## Diagnóstico do Dashboard Atual

### Endpoint Existente
- `/api/v1/reports/daily` - relatório diário básico

### Dados Reais Existentes
- Shipment: status, criticality, delay_days, SLA fields
- ImportHistory: status, valid/invalid/imported/rejected counts
- ShipmentTreatment: tratativas existem
- Services: SLA (BETA-013A), Carrier Efficiency (BETA-014A), Exceptions (BETA-015A)

### Dados Calculados
- KPIs SLA (on_time, late, critical, warning, unknown)
- Eficiência por transportadora (reaproveitar BETA-014A)
- Exceções priorizadas (reaproveitar BETA-015A)
- Falhas de importação (ImportHistory)

### Dados Que Não Existem
- Módulo de alertas reais → `active_alerts_count = 0` (documentado como limitação)
- `resolved_count`, `no_update_count` → 0 (campos não existem no modelo)

## Endpoint Criado

### GET /api/v1/dashboard/summary

Endpoint de resumo do dashboard com KPIs operacionais.

## KPIs Retornados

- `total_shipments`: Total de entregas
- `on_time_count`: Entregas no prazo
- `late_count`: Entregas atrasadas
- `critical_count`: Entregas críticas
- `warning_count`: Entregas em warning/atenção
- `unknown_sla_count`: Entregas sem SLA
- `resolved_count`: 0 (campo não existe no modelo)
- `no_update_count`: 0 (campo não existe no modelo)
- `exceptions_count`: Total de exceções
- `import_failure_count`: Falhas de importação
- `active_alerts_count`: 0 (módulo de alertas não existe)
- `carriers_count`: Total de transportadoras
- `top_carriers_by_efficiency`: Top 5 transportadoras por eficiência
- `top_exceptions`: Top 10 exceções priorizadas
- `generated_at`: Timestamp de geração
- `filters_applied`: Filtros aplicados

## Filtros Globais Suportados

- `estimated_delivery_from`: Data inicial do período
- `estimated_delivery_to`: Data final do período
- `month`: Mês (1-12)
- `year`: Ano (2020-2100)
- `customer_name`: Nome do cliente
- `destination_uf`: UF de destino (2 caracteres)
- `carrier_id`: ID da transportadora
- `status`: Status do shipment
- `criticality`: Criticidade
- `sla_status`: Status SLA
- `is_late`: Se está atrasado (boolean)
- `exception_type`: Tipo de exceção

## Services Reaproveitados

- **SLA Service** (BETA-013A): `calculate_shipment_sla`
- **Carrier Efficiency** (BETA-014A): `calculate_carrier_efficiency`
- **Exceptions Panel** (BETA-015A): `classify_exception_type`, `calculate_exception_priority`

Não houve duplicação de:
- Cálculo de atraso
- Cálculo de criticidade
- Ranking de transportadora
- Classificação de exceções

## Tratamento de Alertas Ainda Não Implementados

O módulo de alertas reais não existe ainda. O dashboard retorna `active_alerts_count = 0` e esta limitação está documentada.

Alertas reais ficam para Épico 5.

## Testes Criados

### test_dashboard_summary.py (25 testes)
- Cálculo de KPIs (total, on_time, late, critical, warning, unknown)
- Cálculo de exceções
- Falhas de importação
- Active alerts count (zero quando não existe módulo)
- Top transportadoras por eficiência
- Top exceções priorizadas
- Filtros (período, mês/ano, cliente, UF, transportadora, criticality, sla_status, is_late, exception_type)
- Ignorar filtros vazios
- Payload estável (generated_at, filters_applied)
- Evitar divisão por zero
- Lidar com base vazia
- Não duplicar regra de SLA

### test_dashboard_api.py (5 testes)
- GET /api/v1/dashboard/summary retorna 200
- Endpoint retorna KPIs
- Endpoint aplica query params
- Endpoint não conflita com rotas existentes
- Payload é estável para frontend

## Evidência de Red → Green → Refactor

1. **Red**: Testes criados antes da implementação
2. **Green**: Implementação do service, schemas e router
3. **Refactor**: Ajustes para lidar com modelos existentes (ImportHistory, Shipment sem relationship carrier)

## Comandos Executados

### Validações Python (raiz)
- python scripts/check_secrets.py --repo-root . ✅
- python scripts/check_secrets.py --repo-root . --self-test ✅
- python scripts/validate_migrations.py ✅
- python scripts/validate_docs.py ✅
- python scripts/beta_validate.py ✅

### Testes Backend (apps/api)
- python -m pytest tests/test_dashboard_summary.py -v ✅ (25/25 passed)
- python -m pytest tests/test_dashboard_api.py -v ✅ (5/5 passed)
- python -m pytest tests/test_exceptions_panel_sla.py -v ✅ (30/30 passed)
- python -m pytest tests/test_exceptions_panel_api.py -v ✅ (5/5 passed)
- python -m pytest tests/test_carrier_efficiency_report.py -v ✅ (26/26 passed)
- python -m pytest tests/test_sla_calculation.py -v ✅ (14/14 passed)
- python -m pytest tests/test_sla_rules.py -v ✅ (27/27 passed)
- python -m pytest tests/test_sla_api.py -v -rs ✅ (5/5 passed)

### Validações Frontend (apps/web)
- npm run lint ✅
- npm run test ✅
- npm run build ✅

## Resultados

- ✅ Secrets check: OK
- ✅ Migrations: OK
- ✅ Docs: OK
- ✅ Beta validation: OK
- ✅ Backend tests dashboard: 30/30 passed
- ✅ Backend tests críticos: 107/107 passed
- ✅ Frontend lint: OK
- ✅ Frontend test: OK
- ✅ Frontend build: OK

## Limitações

- Sem alertas/e-mail (módulo não existe)
- Sem relatório diário (já existe endpoint separado)
- Sem dashboard geral (frontend fica para BETA-016B)
- Sem E2E por Playwright não configurado
- `active_alerts_count` sempre 0 (módulo de alertas não existe)
- `resolved_count` e `no_update_count` sempre 0 (campos não existem no modelo)

## O Que Fica Para BETA-016B

- Dashboard frontend
- Cards de KPI
- Filtros globais visuais
- Integração visual com eficiência e exceções

## O Que Fica Para Épicos Posteriores

- Alertas/e-mail (Épico 5)
- Relatório diário (Épico 6)
- Auditoria completa (Épico 7)

## Confirmação de Governança

- ✅ Sem merge em main
- ✅ Sem auto-merge
- ✅ Sem force push
- ✅ Sem comando destrutivo
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
