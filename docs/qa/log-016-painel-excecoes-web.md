# LOG-016 — Painel de Exceções Web — Validação e Estabilização

## Data/Hora
2026-06-04

## Branch
- **Branch**: feature/painel-excecoes-web
- **Branch base**: feature/painel-excecoes-backend
- **Commit base**: acbb6de docs(qa): registra discovery gate do painel de excecoes

## Dependência do LOG-016 Backend/API
- **LOG-016 Backend/API**: Validado como já existente no módulo shipments
- **Endpoint**: GET /api/v1/shipments/exceptions
- **Regra de exceção**: Shipment.delay_days > 0 OR Shipment.criticality != "normal"
- **Ordenação padrão**: delay_days DESC
- **Filtros disponíveis**: status, criticality, estimated_delivery_from, estimated_delivery_to, due_date_from, due_date_to

## Arquitetura Frontend Encontrada

### Tela Existente
- **Arquivo**: apps/web/src/app/(private)/exceptions/page.tsx
- **Status**: ✅ Já implementada
- **Endpoint consumido**: /api/v1/shipments/exceptions (via listExceptionShipments)
- **Autenticação**: Sim, usa useAuth/session.accessToken

### API Client
- **Arquivo**: apps/web/src/lib/api.ts
- **Função**: listExceptionShipments (linha 145-161)
- **Endpoint**: /shipments/exceptions
- **Parâmetros**: page, page_size, status, criticality, estimated_delivery_from, estimated_delivery_to, due_date_from, due_date_to, sort_by, sort_order
- **Tipo de retorno**: ExceptionShipmentListResponse

### Tipos
- **Arquivo**: apps/web/src/lib/types.ts
- **Tipo Shipment**: Inclui delay_days e criticality (linhas 39-40)
- **Tipo ExceptionShipmentListResponse**: ShipmentListResponse (linha 101)
- **Tipo ShipmentListParams**: Inclui todos os filtros disponíveis no backend (linhas 76-91)

### Campos Exibidos na Tela
- **Tracking**: tracking_code (com link para /shipments/{id})
- **Status**: status
- **Atraso**: delay_days
- **Criticidade**: criticality

### Filtros Implementados
- **Criticality**: Select com opções (Todas, Baixa, Média, Alta)
- **Status**: Não implementado na UI (disponível no backend)
- **Datas**: Não implementado na UI (disponível no backend)

### Estados de UI
- **Loading**: "Carregando..." (spinner ou texto)
- **Vazio**: "Sem exceções no momento."
- **Erro**: "Não foi possível carregar exceções." (com fundo vermelho)
- **Sucesso**: Lista de exceções em tabela

### Ordenação
- **Padrão**: delay_days DESC (hardcoded na chamada da API)
- **UI**: Não permite alterar ordenação

## Testes/Checklist Criados

### Checklist de Validação (Manual)
Como o projeto não permite teste de componente sem refatoração grande, foi criado checklist reprodutível:

1. **Endpoint consumido**: ✅ /api/v1/shipments/exceptions
2. **Autenticação**: ✅ Usa session.accessToken
3. **Tipos corretos**: ✅ Shipment inclui delay_days e criticality
4. **Filtro por criticality**: ✅ Implementado na UI
5. **Filtro por status**: ⏸️ Não implementado na UI (disponível no backend)
6. **Filtro por datas**: ⏸️ Não implementado na UI (disponível no backend)
7. **Estado loading**: ✅ Implementado
8. **Estado vazio**: ✅ Implementado
9. **Estado erro**: ✅ Implementado
10. **Estado sucesso**: ✅ Implementado
11. **Ordenação**: ✅ delay_days DESC (hardcoded)
12. **Link para detalhe**: ✅ /shipments/{id}
13. **Não expõe stack trace**: ✅ Mensagem de erro genérica

## Implementação Green Aplicada
**Nenhuma alteração funcional necessária**

A tela já está implementada corretamente:
- Consome o endpoint correto /api/v1/shipments/exceptions
- Usa tipos corretos (Shipment com delay_days e criticality)
- Implementa filtro por criticality
- Implementa estados de UI (loading, vazio, erro, sucesso)
- Ordenação padrão correta (delay_days DESC)
- Link para detalhe do shipment

**Justificativa de não alteração funcional:**
- A tela já está alinhada com o backend
- Não há lacunas críticas
- Filtros adicionais (status, datas) podem ser implementados no futuro se necessário
- Não há bugs comprovados

## Validações

### npm run lint
- **Resultado**: ✅ All checks passed

### npm run test
- **Resultado**: ✅ 58 passed (8 test files)

### npm run build
- **Resultado**: ✅ Compiled successfully (12 routes geradas)

## Smoke Manual
**Bloqueado por autenticação/browser**

Como não é possível validar manualmente via navegador, o smoke manual não foi executado. A validação foi feita por inspeção de código e checklist reprodutível.

## Arquivos Inspecionados
- apps/web/src/app/(private)/exceptions/page.tsx
- apps/web/src/lib/api.ts
- apps/web/src/lib/types.ts

## Arquivos Alterados
- **Nenhum arquivo funcional alterado**
- Apenas documentação criada: docs/qa/log-016-painel-excecoes-web.md

## Comandos Executados
```bash
cd C:\Users\LENOVO\Ilex_Logistica
git checkout feature/painel-excecoes-backend
git checkout -b feature/painel-excecoes-web
cd apps/web
npm run lint  # All checks passed
npm run test  # 58 passed (8 test files)
npm run build  # Compiled successfully (12 routes geradas)
```

## Riscos
- **Risco de validação manual**: Smoke manual não foi executado por limitação de ambiente
- **Risco de filtros não implementados**: Filtros de status e datas não estão na UI (disponíveis no backend)

## Pendências
- Smoke manual não executado (limitação de ambiente)
- Filtros de status e datas podem ser implementados no futuro se necessário

## Limite Claro entre LOG-016 e LOG-017
- **LOG-016**: Painel de exceções (consulta) — ✅ Validado como já existente
- **LOG-017**: Tratativas (ação sobre exceções) — Observação: O módulo shipments já possui ShipmentTreatment e endpoint /shipments/{id}/treatments

## Conclusão
✅ **LOG-016 Web validado como já existente**
- Tela /exceptions já implementada
- Consome endpoint correto /api/v1/shipments/exceptions
- Usa tipos corretos (Shipment com delay_days e criticality)
- Implementa filtro por criticality
- Implementa estados de UI (loading, vazio, erro, sucesso)
- Ordenação padrão correta (delay_days DESC)
- Nenhuma alteração funcional necessária
- Nenhum código funcional foi alterado
