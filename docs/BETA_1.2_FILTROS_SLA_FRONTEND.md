# BETA-1.2: Filtros por Criticidade no Frontend

**Status:** Concluído  
**Data:** 2026-06-23  
**Épico:** 1 - SLA, atraso e criticidade

---

## Especificação SDD

### Objetivo
Implementar filtros `sla_status` e `is_late` na tela de envios (shipments) do frontend, permitindo filtragem visual por status de SLA e indicador de atraso.

### Frontend

**Componente:** Seção de filtros em `shipments/page.tsx`

**Dropdown sla_status:** Select com opções:
- Todos (vazio)
- Crítico (critical)
- Warning (warning)
- Normal (normal)
- Desconhecido (unknown)

**Toggle is_late:** Select com opções:
- Todos (vazio)
- Sim (true)
- Não (false)

**Estado:** React state `slaStatusFilter` e `isLateFilter`

**API:** Chamada `listShipments` com parâmetros `sla_status` e `is_late` (já existente em `api.ts`)

### Critérios de Aceite

- [x] Dropdown de sla_status exibe todas as opções
- [x] Toggle is_late funciona corretamente
- [x] Filtros são aplicados ao clicar "Aplicar Filtros"
- [x] Filtros combinados funcionam (sla_status + is_late)
- [x] Loading state durante busca com filtros
- [x] Empty state quando sem resultados
- [x] Limpar Filtros reset sla_status e is_late

---

## Implementação

### Arquivos Modificados

1. **apps/web/src/app/(private)/shipments/page.tsx**
   - Adicionado estado `slaStatusFilter` e `isLateFilter`
   - Adicionados parâmetros `sla_status` e `is_late` na chamada `listShipments`
   - Adicionados dropdowns na seção "Filtros manuais"
   - Adicionados ao `onClearFilters` para reset
   - Adicionados ao array de dependências do `useCallback`

2. **apps/web/src/app/(private)/shipments/shipments-sla-filters.test.tsx**
   - Substituídos 2 stubs de teste (`is_late=true` e `is_late=false`) por testes reais
   - Corrigido teste `Deve aplicar filtro por sla_status` que usava `getByText("Todos")` ambíguo
   - Adicionados 6 novos testes:
     - Renderização do dropdown com todas as opções
     - Filtro combinado sla_status + is_late
     - Limpar filtros SLA
     - Loading state com filtros SLA
     - Empty state com filtros SLA

### Integração com Backend

- `types.ts` já tinha `sla_status` e `is_late` em `ShipmentListParams` ✅
- `api.ts` já enviava `sla_status` e `is_late` como query params ✅
- Backend (Tarefa 1.1) já aceita e processa esses filtros ✅

---

## Critérios TDD

### Frontend Tests

**Testes implementados (8 novos/substituídos):**
1. `Deve renderizar dropdown de SLA Status com todas as opções` — verifica opções do select
2. `Deve aplicar filtro por sla_status=critical` — seleciona e verifica chamada à API
3. `Deve aplicar filtro por is_late=true` — seleciona e verifica chamada à API
4. `Deve aplicar filtro por is_late=false` — seleciona e verifica chamada à API
5. `Deve combinar filtros sla_status e is_late` — seleciona ambos e verifica chamada
6. `Deve limpar filtros SLA ao clicar em Limpar Filtros` — aplica e limpa, verifica undefined
7. `Deve exibir loading state com filtros SLA` — verifica "Carregando..."
8. `Deve exibir empty state com filtros SLA` — verifica "Nenhum envio encontrado."

**Resultado:** 32/32 testes passando no arquivo de testes SLA

---

## Validação

**Frontend:**
```bash
cd apps/web
npx vitest run "src/app/(private)/shipments/shipments-sla-filters.test.tsx"
# Resultado: 32 passed

npm test
# Resultado: 396 passed (42 test files)

npm run build
# Resultado: Compiled successfully
```

---

## Como Usar

### Filtro SLA Status

1. Na tela de Envios, localize o dropdown "SLA Status" na seção de filtros
2. Selecione uma opção: Crítico, Warning, Normal, Desconhecido
3. Clique em "Aplicar Filtros"
4. A lista será filtrada pelo status de SLA selecionado

### Filtro Atrasado?

1. Na tela de Envios, localize o dropdown "Atrasado?" na seção de filtros
2. Selecione "Sim" para ver apenas envios atrasados ou "Não" para envios no prazo
3. Clique em "Aplicar Filtros"

### Filtros Combinados

Ambos os filtros podem ser usados simultaneamente. Por exemplo:
- SLA Status = "Crítico" + Atrasado? = "Sim" → apenas envios críticos e atrasados

### Limpar Filtros

Clique em "Limpar Filtros" para resetar todos os filtros, incluindo SLA Status e Atrasado?

---

## Próximos Passos

1. **Tarefa 1.3:** Implementar tela de gestão de regras SLA (CRUD completo)
