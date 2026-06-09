# BETA-011C - Correção de Bloqueadores de Build/Test Frontend Preexistentes

## Escopo

Correção de bloqueadores frontend identificados no BETA-011B que impediam `npm run build` e deixavam `npm run test` com falhas. Esta tarefa é focada em estabilização, sem implementação de feature funcional nova.

## Base Usada

**Branch Base:** origin/feature/beta-011b-shipment-fiscal-financial-frontend (BETA-011B)

**Branch Empilhada:** feature/beta-011c-fix-frontend-build-test-blockers

**Razão:** Esta branch empilhada corrige os erros preexistentes que impediam o build e test do frontend, permitindo que o BETA-011B seja integrado com sucesso.

## Erros Encontrados

### Erro 1: `inactivateUser` não existe

**Arquivo:** `apps/web/src/app/(private)/users/page.tsx`

**Mensagem de Erro:**
```
Export inactivateUser doesn't exist in target module
The export inactivateUser was not found in module [project]/src/lib/api.ts
Did you mean to import inactivateCarrier?
```

**Causa Raiz:**
- A página de usuários importava e usava `inactivateUser`, mas essa função não existia no client HTTP
- A função correta para inativar usuários é usar `updateUser` com o parâmetro `is_active: false`

**Correção Aplicada:**
- Substituído `await inactivateUser(session.accessToken, item.id)` por `await updateUser(session.accessToken, item.id, { is_active: false })`
- Removido `inactivateUser` do import (já não estava presente após correção anterior)

### Erro 2: `promoteDeliveryToShipment` não existe

**Arquivo:** `apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx`

**Mensagem de Erro:**
```
Export promoteDeliveryToShipment doesn't exist in target module
The export promoteDeliveryToShipment was not found in module [project]/src/lib/api.ts
Did you mean to import promoteDelivery?
```

**Causa Raiz:**
- A página de detalhe de delivery importava e usava `promoteDeliveryToShipment`, mas a função correta no client HTTP é `promoteDelivery`
- Nome incorreto da função na importação e no uso

**Correção Aplicada:**
- Substituído `promoteDeliveryToShipment` por `promoteDelivery` no import
- Substituído `await promoteDeliveryToShipment(session.accessToken, item.id, payload)` por `await promoteDelivery(session.accessToken, item.id, payload)`

### Erro 3: Falhas em `api.test.ts`

**Arquivo:** `apps/web/src/lib/api.test.ts`

**Mensagens de Erro:**
```
FAIL src/lib/api.test.ts > api exports e assinaturas > promoteDeliveryToShipment esta exportado (LOG-022)
AssertionError: expected 'undefined' to be 'function'

FAIL src/lib/api.test.ts > api exports e assinaturas > promoteDeliveryToShipment recebe token, deliveryId e payload (LOG-022)
TypeError: Cannot read properties of undefined (reading 'length')
```

**Causa Raiz:**
- O teste importava e verificava `promoteDeliveryToShipment`, mas a função correta no client HTTP é `promoteDelivery`
- Testes desatualizados após renomeação da função no client HTTP

**Correção Aplicada:**
- Substituído `promoteDeliveryToShipment` por `promoteDelivery` no import
- Atualizado nome do teste de "promoteDeliveryToShipment esta exportado (LOG-022)" para "promoteDelivery esta exportado (LOG-022)"
- Atualizado assertion de `expect(typeof promoteDeliveryToShipment).toBe("function")` para `expect(typeof promoteDelivery).toBe("function")`
- Atualizado nome do teste de "promoteDeliveryToShipment recebe token, deliveryId e payload (LOG-022)" para "promoteDelivery recebe token, deliveryId e payload (LOG-022)"
- Atualizado assertion de `expect(promoteDeliveryToShipment.length).toBe(3)` para `expect(promoteDelivery.length).toBe(3)`

## Arquivos Modificados

### Frontend

1. `apps/web/src/app/(private)/users/page.tsx`
   - Substituído chamada a `inactivateUser` por `updateUser` com `is_active: false`

2. `apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx`
   - Substituído `promoteDeliveryToShipment` por `promoteDelivery` no import
   - Substituído chamada a `promoteDeliveryToShipment` por `promoteDelivery`

3. `apps/web/src/lib/api.test.ts`
   - Substituído `promoteDeliveryToShipment` por `promoteDelivery` no import
   - Atualizado 2 testes para usar `promoteDelivery` em vez de `promoteDeliveryToShipment`

## Testes Afetados

- ✅ `src/lib/api.test.ts` - 21 testes passaram (anteriormente 19 passed, 2 failed)
- ✅ Todos os testes frontend passaram (60/60)
- ✅ Build frontend passou
- ✅ Lint frontend passou

## Confirmação de Que Não Houve Feature Nova

- ✅ Nenhuma funcionalidade nova foi implementada
- ✅ Apenas correção de nomes de funções já existentes
- ✅ Ajuste de imports para usar os nomes corretos
- ✅ Atualização de testes para refletir os nomes corretos
- ✅ Nenhuma alteração no backend
- ✅ Nenhuma alteração na lógica de negócio
- ✅ Nenhuma alteração na UI

## Confirmação de Que BETA-011B Continua Íntegro

- ✅ Build frontend passou (anteriormente falhava)
- ✅ Testes frontend passaram (60/60, anteriormente 58/60)
- ✅ Lint frontend passou
- ✅ As alterações do BETA-011B (campos fiscais/financeiros e filtros) continuam funcionando
- ✅ Nenhuma alteração foi feita nos arquivos do BETA-011B

## Comandos Executados

### Testes Específicos
```bash
npm run test -- api.test
```
**Resultado:** ✅ 21 passed (anteriormente 19 passed, 2 failed)

```bash
npm run test
```
**Resultado:** ✅ 60 passed (anteriormente 58 passed, 2 failed)

### Build Frontend
```bash
npm run build
```
**Resultado:** ✅ Compiled successfully (anteriormente falhava)

### Lint Frontend
```bash
npm run lint
```
**Resultado:** ✅ Passou (com warning não relacionado)

## Resultados

- ✅ `npm run test` passa sem falhas (60/60)
- ✅ `npm run build` passa
- ✅ `npm run lint` passa, aceitando apenas warnings não bloqueantes já documentados
- ✅ `api.test.ts` passa (21/21)
- ✅ Erros de `inactivateUser` e `promoteDeliveryToShipment` corrigidos com contrato real
- ✅ Testes do BETA-011B continuam passando
- ✅ Nenhum teste foi removido para mascarar falha
- ✅ Nenhum skip indevido foi adicionado
- ✅ Nenhuma feature nova foi implementada

## O Que Permanece para BETA-012

1. **Importação CSV/XLSX:** Importar campos fiscais/financeiros de arquivos
2. **Preview/confirmação:** Preview e confirmação de importação
3. **Layout Braspress:** Layout específico para Braspress

## Confirmação de Governança

- ✅ Nenhum merge foi feito em main
- ✅ Nenhum rebase foi feito
- ✅ Nenhum git push --force foi usado
- ✅ Nenhum comando destrutivo foi usado
- ✅ Branch criada a partir de origin/feature/beta-011b-shipment-fiscal-financial-frontend
- ✅ Draft PR (sem merge automático)
- ✅ Commits em pt-BR com Conventional Commits e ID beta
- ✅ Sem feature funcional nova
- ✅ Sem importação Excel/XLSX
- ✅ Sem SLA
- ✅ Sem eficiência por transportadora
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
- ✅ Correções baseadas em contrato real do API client
- ✅ Testes atualizados para refletir contrato real

## Assinatura

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ✅ Concluído (BETA-011C - Correção de Bloqueadores de Build/Test Frontend Preexistentes)
