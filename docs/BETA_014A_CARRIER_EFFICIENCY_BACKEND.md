# BETA-014A: Eficiência por Transportadora Backend

## Escopo

Implementar o backend do Épico 4 — Eficiência por transportadora — com endpoint/service de agregação, filtros, rankings e testes automatizados. Este PR é backend-only e inicia a Sprint Beta 2.

## Base Usada

- Branch: origin/feature/beta-013b-sla-frontend-badges-filters-rules
- Confirmação de backend-only

## Endpoint Criado

`GET /api/v1/shipments/analytics/carrier-efficiency`

## Métricas Calculadas

Por transportadora:

- `carrier_id`: ID da transportadora
- `carrier_name`: Nome da transportadora
- `total_invoices`: Total de NFs (baseado em invoice_number)
- `total_shipments`: Total de shipments
- `on_time_count`: Entregas no prazo
- `on_time_percentage`: Percentual de entregas no prazo
- `late_count`: Entregas atrasadas
- `late_percentage`: Percentual de entregas atrasadas
- `critical_count`: Entregas críticas (criticality == "alta")
- `lost_count`: Extraviadas (sempre 0, status não existe no domínio)
- `lost_percentage`: Percentual de extraviadas (sempre 0)
- `total_freight_value`: Valor total do frete
- `total_invoice_value`: Valor total das NFs
- `average_freight_percentage`: Percentual médio do frete
- `average_freight_value`: Valor médio do frete
- `ranking_by_efficiency`: Ranking por eficiência
- `ranking_by_cost`: Ranking por custo
- `ranking_by_volume`: Ranking por volume

## Filtros Suportados

- `estimated_delivery_from`: Data de entrega estimada (de)
- `estimated_delivery_to`: Data de entrega estimada (até)
- `month`: Mês
- `year`: Ano
- `customer_name`: Nome do cliente
- `destination_uf`: UF de destino
- `carrier_id`: ID da transportadora
- `status`: Status do shipment
- `criticality`: Criticidade
- `sla_status`: Status SLA (on_time, warning, late, critical, unknown)
- `is_late`: Está atrasada (boolean)

## Critérios de Ranking

**Ranking por eficiência:**
- Maior `on_time_percentage` primeiro
- Empate por maior volume
- Ordem determinística

**Ranking por custo:**
- Menor `average_freight_percentage` primeiro
- Ordem determinística

**Ranking por volume:**
- Maior `total_shipments` primeiro
- Ordem determinística

## Decisão sobre Extraviadas

**Status existentes no domínio:**
- `pending`, `in_transit`, `delivered`, `failed`

**Status de extraviada:**
- Não existe status de extraviada/lost/missing no domínio
- `lost_count` sempre retorna 0
- `lost_percentage` sempre retorna 0
- Status operacional de extravio ainda não está modelado
- Não inventar dado falso

## Tratamento de Divisão por Zero

- Transportadora sem dados não aparece na lista
- Percentuais retornam 0 quando total_shipments == 0
- average_freight_percentage retorna 0 quando total_invoice_value == 0
- average_freight_value retorna 0 quando total_shipments == 0

## Estratégia de SLA/On-Demand

O service reaproveita o helper/service do BETA-013A para determinar SLA/atraso:

- `calculate_shipment_sla(db, shipment_id)` chamado para cada shipment
- Não duplica regras de due date, delay_days, sla_status, is_late, criticality
- Filtros SLA (sla_status, is_late) aplicados on-demand após cálculo

## Limitações

- Status de extraviada não existe no domínio
- Performance pode ser afetada em grandes volumes (cálculo on-demand por shipment)
- Filtros SLA aplicados em memória após consulta SQL

## Escopo Backend-Only

- Nenhum código frontend novo
- Nenhum painel visual
- Nenhuma integração com dashboard
- Foco exclusivo em endpoint/service/backend

## O que fica para BETA-014B

- Painel frontend de eficiência
- Integração visual com dashboard
- Formatação BRL/percentual
- Estados loading/erro/vazio
- Gráficos e visualizações

## Testes Criados

**Service tests (test_carrier_efficiency_report.py):**
- 26 testes reais (nenhum skeleton)
- Agrupamento e totais
- SLA e atraso
- Extraviadas
- Financeiro
- Rankings
- Filtros
- Transportadora sem dados
- Payload estável

**API tests (test_carrier_efficiency_api.py):**
- 4 testes reais
- Endpoint retorna 200 com autenticação
- Endpoint retorna payload esperado
- Endpoint aplica query params
- Endpoint não conflita com rota dinâmica

**Total: 30 testes passando**

## Evidência de Red → Green → Refactor

**Fase Red:**
- 26 testes skeleton criados

**Fase Green:**
- Service calculate_carrier_efficiency implementado
- Schemas CarrierEfficiencyMetrics e CarrierEfficiencyResponse criados
- Endpoint GET /api/v1/shipments/analytics/carrier-efficiency criado
- 26 testes reais implementados
- 4 testes API implementados

**Fase Refactor:**
- Documentação criada
- Validações pendentes

## Comandos Executados

```bash
cd apps/api
python -m pytest tests/test_carrier_efficiency_report.py -v
# Resultado: 26 passed

python -m pytest tests/test_carrier_efficiency_api.py -v
# Resultado: 4 passed

python -m pytest tests/test_sla_calculation.py tests/test_sla_rules.py tests/test_sla_api.py tests/test_shipments_advanced_filters.py -v
# Resultado: 65 passed
```

## Resultados

- Testes de eficiência: 30 passed (26 service + 4 API)
- Testes SLA Backend: 65 passed
- Nenhum skeleton test restante
- Nenhum skip obrigatório

## Confirmação de Governança

- ✅ Sem merge em main
- ✅ Sem auto-merge
- ✅ Sem force push
- ✅ Sem comando destrutivo
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
- ✅ Backend-only
- ✅ Nenhum dado real de cliente
