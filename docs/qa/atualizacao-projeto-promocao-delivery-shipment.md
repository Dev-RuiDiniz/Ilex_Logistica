# Atualização do Projeto - Promoção Delivery → Shipment

## Data/Hora
2026-06-05 18:00

## Resumo executivo
Implementação completa da funcionalidade de promoção manual de Delivery para Shipment, incluindo backend (LOG-021) e frontend (LOG-022/LOG-023), com documentação de handoff (LOG-024).

## PRs criados

### PR #1 - Fase Operacional LOG-016 a LOG-018
- **Status**: OPEN
- **Branch**: feature/relatorio-diario → main
- **Conteúdo**: Fase Operacional LOG-016 a LOG-018 (painel de excecoes, tratativas, relatorio diario)
- **Validações**: Backend pytest passou, ruff passou, frontend lint/test/build passou

### PR #2 - Backend Promoção Delivery → Shipment (LOG-019 a LOG-021)
- **Status**: OPEN
- **Branch**: feature/promocao-delivery-shipment → feature/relatorio-diario
- **Conteúdo**: 
  - LOG-019: Revisão arquitetural Shipment vs Delivery
  - LOG-020: Especificação Delivery → Shipment
  - LOG-021: Endpoint backend de promoção manual
- **Validações**: Backend 113/113 passando, ruff All checks passed

### PR #3 - Frontend Promoção Delivery → Shipment (LOG-022 a LOG-024)
- **Status**: OPEN (criado manualmente)
- **Branch**: feature/selecao-transportadora-promocao → feature/promocao-delivery-shipment
- **Conteúdo**:
  - LOG-022: Frontend da promoção manual Delivery → Shipment
  - LOG-023: Select de transportadora no formulário de promoção
  - LOG-024: Handoff Web
- **Validações**: Frontend 60/60 passando, lint passou, build passou, backend regressivo 113/113 passando

## Branches criadas

### feature/promocao-delivery-shipment
- **Base**: feature/relatorio-diario
- **Commits**:
  - a17de8e docs(qa): registra revisao arquitetural Shipment vs Delivery
  - 348a279 docs(qa): especifica promocao Delivery para Shipment
  - 5ff315e feat(imports): adiciona promocao manual de Delivery para Shipment
- **Status**: Pushada, PR #2 criado

### feature/promocao-delivery-shipment-web
- **Base**: feature/promocao-delivery-shipment
- **Commits**:
  - 69a9a0f feat(imports): adiciona frontend para promocao de Delivery para Shipment
- **Status**: Local, não pushada

### feature/selecao-transportadora-promocao
- **Base**: feature/promocao-delivery-shipment-web
- **Commits**:
  - eeb3eed feat(imports): adiciona selecao de transportadora na promocao
  - 45bc48b docs(qa): registra handoff web da promocao Delivery para Shipment
- **Status**: Pushada, PR #3 criado manualmente

## Arquivos alterados

### Backend (LOG-021)
- apps/api/app/modules/carriers/models.py
- apps/api/app/modules/imports/router.py
- apps/api/app/modules/imports/schemas.py
- apps/api/app/modules/imports/service.py
- apps/api/tests/test_promote_delivery.py (novo)
- docs/qa/log-021-promocao-delivery-shipment.md (novo)

### Frontend (LOG-022)
- apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx
- apps/web/src/lib/api.test.ts
- apps/web/src/lib/api.ts
- apps/web/src/lib/types.ts
- docs/qa/log-022-promocao-delivery-shipment-web.md (novo)

### Frontend (LOG-023)
- apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx
- docs/qa/log-023-selecao-transportadora-promocao.md (novo)

### Documentação (LOG-024)
- docs/qa/log-024-handoff-web-promocao-delivery-shipment.md (novo)

## Validações realizadas

### Backend
- pytest: 113/113 passando
- ruff: All checks passed

### Frontend
- npm run lint: Passou
- npm run test: 60/60 passando
- npm run build: Sucesso

## Ordem de merge recomendada

1. **PR #1 primeiro**: feature/relatorio-diario → main
2. **PR #2 depois**: feature/promocao-delivery-shipment → feature/relatorio-diario
3. **PR #3 por último**: feature/selecao-transportadora-promocao → feature/promocao-delivery-shipment

## Governança mantida

- Nenhum merge realizado
- Nenhum rebase realizado
- Nenhum push --force realizado
- Nenhuma migration criada
- Main não alterada
- Merge exclusivo do supervisor humano

## Riscos e pendências

### Riscos
- PRs empilhados (PR #2 sobre PR #1, PR #3 sobre PR #2)
- LOG-A04 Docker/WSL2 segue pendente
- Select não filtra apenas carriers ativos
- Se carriers não carregarem, promoção fica bloqueada

### Pendências
- Aguardar merge dos PRs #1, #2 e #3
- LOG-A04 Docker/WSL2 precisa ser resolvido

## Próximos passos

1. Aguardar review e merge do PR #1
2. Aguardar review e merge do PR #2
3. Aguardar review e merge do PR #3
4. Resolver LOG-A04 Docker/WSL2
