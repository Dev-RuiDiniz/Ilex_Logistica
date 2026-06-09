# BETA-013B: Frontend SLA - Badges, Filtros e Tela de Regras

## Escopo

Implementar o frontend do Épico 1 — SLA, atraso e criticidade — consumindo o backend criado no BETA-013A.

## Base Usada

- Branch: origin/feature/beta-013a-sla-delay-criticality-backend
- Contrato de API verificado em docs/BETA_013B_API_CONTRACT_VERIFIED.md

## Confirmação de Frontend-Only

- Nenhum código backend novo
- Apenas ajuste de contrato (tipos TypeScript) se necessário
- Foco exclusivo em UI/UX

## Progresso

### Fase TDD Red (Concluída) ✅

- Tipos TypeScript para SLA (Shipment, ShipmentListParams, SlaRule, etc.)
- Helpers de apresentação (formatSlaStatusLabel, getSlaStatusBadgeColor, etc.)
- API client functions (listSlaRules, createSlaRule, updateSlaRule, recalculateSla)
- Testes skeleton para componentes (Red)

### Fase TDD Green (Concluída) ✅

- Componente SlaBadge (6 testes passando)
- Componente SlaFilters
- Integração na listagem de shipments
- Colunas SLA na tabela (Status SLA, Data Limite SLA)
- Filtros SLA na UI (status e atrasada)

### Fase TDD Refactor (Concluída) ✅

- Tela de regras SLA (10 testes passando)
- Seção SLA no detalhe da entrega (6 testes passando)
- Reprocessamento SLA na UI
- API client tests completos (6 testes passando)

## Componentes Criados/Alterados

### Tipos TypeScript
- apps/web/src/lib/types.ts: Adiciona campos SLA em Shipment (sla_due_date, sla_status, is_late, sla_rule_id)
- apps/web/src/lib/types.ts: Adiciona filtros SLA em ShipmentListParams (sla_status, is_late)
- apps/web/src/lib/types.ts: Adiciona tipos SlaRule, SlaRuleCreate, SlaRuleUpdate, SlaRecalculateResponse

### Helpers de Apresentação
- apps/web/src/lib/sla-helpers.ts: Helpers para formatar status SLA, criticidade, atraso, data
- apps/web/src/lib/sla-helpers.ts: Badges coloridos para status SLA e criticidade
- apps/web/src/lib/sla-helpers.test.ts: 35 testes passando

### API Client
- apps/web/src/lib/api.ts: Adiciona filtros sla_status e is_late em listShipments
- apps/web/src/lib/api.ts: Adiciona funções SLA (listSlaRules, createSlaRule, updateSlaRule, recalculateSla, recalculateShipmentSla)
- apps/web/src/lib/sla-api.test.ts: 6 testes passando

### Componentes UI
- apps/web/src/components/SlaBadge.tsx: Badge SLA
- apps/web/src/components/SlaBadge.test.tsx: 6 testes passando
- apps/web/src/components/SlaFilters.tsx: Filtros SLA

### Páginas
- apps/web/src/app/(private)/shipments/page.tsx: Integração SLA na listagem
- apps/web/src/app/(private)/shipments/[id]/page.tsx: Seção SLA no detalhe
- apps/web/src/app/(private)/settings/sla/page.tsx: Tela de regras SLA

## Badges e Labels Implementados

- No prazo (on_time) - verde
- Atenção (warning) - amarelo
- Atrasada (late) - laranja
- Crítica (critical) - vermelho
- Sem SLA (unknown) - cinza

## Filtros Visuais Implementados

- Status SLA: on_time, warning, late, critical, unknown
- Atrasada: sim/não/todas
- Combinação com filtros existentes preservada

## Tela de Regras SLA

- Listar regras SLA
- Exibir estado vazio
- Criar regra
- Editar regra (ativar/inativar)
- Exibir regra global/default
- Exibir regra por transportadora
- Exibir regra por transportadora + UF
- Validar campos obrigatórios
- Validar transit_days positivo
- Validar UF com 2 letras quando informada
- Exibir loading
- Exibir erro de API
- Reprocessamento SLA com contadores

## Detalhe da Entrega

- Seção "SLA e Criticidade"
- Prazo SLA
- Status SLA
- Atraso em dias
- Criticidade
- Regra aplicada, se backend retornar
- Estado "Sem SLA" quando dados insuficientes
- Estado "-" para campo indisponível

## Reprocessamento SLA

- Botão "Reprocessar SLA" na tela de regras
- Chama endpoint real do BETA-013A
- Mostra loading
- Mostra erro
- Mostra resultado com contadores:
  - processed_count
  - updated_count
  - skipped_count
  - error_count

## Testes Criados

- sla-helpers.test.ts: 35 testes passando
- sla-api.test.ts: 6 testes passando
- shipments-sla-badges.test.tsx: 8 testes passando
- shipments-sla-filters.test.tsx: 9 testes passando
- SlaBadge.test.tsx: 6 testes passando
- sla-rules-page.test.tsx: 10 testes passando
- delivery-sla-detail.test.tsx: 6 testes passando

## Evidência de Red → Green → Refactor

- Fase Red: Tipos, helpers e testes skeleton
- Fase Green: Componentes e integração na listagem
- Fase Refactor: Tela de regras e detalhe

## Comandos Executados

```bash
cd apps/web
npm run test
# Resultado: 143 passed

npm run lint
# Resultado: 0 errors, 1 warning

npm run build
# Resultado: Compiled successfully
```

## Resultados

- Testes Frontend: 143 passed
- Testes SLA: 80 passed (helpers + badges + api + rules + detail)
- Build: ✅
- Lint: ✅

## Limitações

- Filtros SLA aplicados em memória após paginação (estratégia on-demand do backend)
- Performance pode ser afetada em grandes volumes
- Playwright não configurado nesta branch (limitação conhecida)

## E2E

- Playwright não configurado nesta branch (limitação conhecida)

## O que fica para BETA-014

- Eficiência por transportadora

## O que fica para Épico 9

- RBAC granular avançado (controle granular)

## Confirmação de Governança

- ✅ Sem merge em main
- ✅ Sem auto-merge
- ✅ Sem force push
- ✅ Sem comando destrutivo
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
