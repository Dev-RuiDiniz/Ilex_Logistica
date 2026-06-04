# LOG-012: Detalhe de Entrega

## Objetivo
Estabilizar a view de detalhe de entrega, permitindo visualizar dados operacionais, histórico e tratamentos de uma entrega específica.

## Implementação

### Backend

#### 1. Schema (`apps/api/app/modules/imports/schemas.py`)
- Adicionado `DeliveryDetailResponse` schema para estruturar a resposta do endpoint de detalhe
- Inclui todos os campos do modelo `Delivery` com formatação adequada

#### 2. Service (`apps/api/app/modules/imports/service.py`)
- Adicionada função `get_delivery_detail(db, delivery_id)` para buscar uma entrega por ID
- Retorna `DeliveryDetailResponse` ou `None` se não encontrado
- Usa `db.query(Delivery).filter(Delivery.id == delivery_id).first()`

#### 3. Router (`apps/api/app/modules/imports/router.py`)
- Adicionado endpoint `GET /imports/deliveries/{delivery_id}`
- Usa `get_delivery_detail` service function
- Retorna 404 se a entrega não for encontrada
- Requer autenticação via `get_current_user`

### Frontend

#### 1. Types (`apps/web/src/lib/types.ts`)
- Adicionado tipo `DeliveryDetail` com todos os campos da entrega
- Campos: id, nf, transportadora, data_coleta, valor_frete, percentual_frete, created_at

#### 2. API Client (`apps/web/src/lib/api.ts`)
- Adicionada função `getDeliveryDetail(token, deliveryId)` para buscar detalhes da entrega
- Faz requisição `GET /imports/deliveries/{deliveryId}` com autenticação

#### 3. Detail Page (`apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx`)
- Criada página de detalhe de entrega
- Exibe informações: NF, Transportadora, Data de Coleta, Valor Frete, Percentual Frete, Criado em
- Usa `useAuth` para obter token de autenticação
- Usa `getDeliveryDetail` para buscar dados
- Formata valores monetários e datas em português brasileiro

#### 4. List Page Update (`apps/web/src/app/(private)/shipments/deliveries/page.tsx`)
- Adicionado link na coluna NF da tabela para navegar para a página de detalhe
- Usa `Link` do Next.js para navegação client-side
- Link leva para `/shipments/deliveries/{id}`

## QA

### Frontend
- `npm run lint`: Passou
- `npm run build`: Passou
- `npm run test`: 39 testes passaram
- Rota `/shipments/deliveries/[id]` gerada com sucesso (Dynamic)

### Backend
- `pytest`: 105 testes passaram (incluindo 3 novos testes para LOG-012)
  - `test_get_delivery_detail_entrega_existente_retorna_200`: Verifica que GET detalhe de entrega existente retorna 200
  - `test_get_delivery_detail_entrega_inexistente_retorna_404`: Verifica que GET entrega inexistente retorna 404
  - `test_get_delivery_detail_resposta_nao_expoe_stack_trace`: Verifica que resposta de erro não expõe stack trace
- `ruff check .`: Passou

## Status
✅ Implementação concluída
✅ Frontend validado (lint + build + test)
✅ Backend validado (pytest + ruff)
✅ Testes automatizados criados para o endpoint de detalhe

## Correções Realizadas
- Corrigido uso depreciado `status.HTTP_404` para `404` no router (Starlette deprecation)
- Corrigido erro de sintaxe em teste (`assert 'File "' not in str(body)`)

## Regression Gate — cobertura frontend

### Motivo do gate
Foi detectado que o arquivo `apps/web/src/lib/api.test.ts` foi removido acidentalmente durante a limpeza de arquivos temporários, causando uma queda de 56 testes para 39 testes no frontend. Este arquivo havia sido incluído anteriormente no LOG-011 Web para validar `listDeliveries`.

### Impacto da remoção de api.test.ts
A remoção causou a perda de 17 testes que validavam:
- Exportações de funções de API (apiLogin, listCarriers, createCarrier, etc.)
- Assinaturas das funções (número de parâmetros)
- Especificamente para LOG-011: validação de que `listDeliveries` estava exportado com assinatura correta

### Decisão tomada
**Caso A — api.test.ts foi removido sem necessidade**: Arquivo restaurado a partir do commit 8657ed9 e testes mínimos de getDeliveryDetail adicionados no mesmo arquivo.

### Testes preservados do LOG-011
- ✅ `listDeliveries continua exportado`
- ✅ `listDeliveries mantém assinatura esperada`
- ✅ Todos os 17 testes originais do LOG-011 foram preservados

### Testes adicionados para LOG-012
- ✅ `getDeliveryDetail está exportado`
- ✅ `getDeliveryDetail aceita token e deliveryId`

### Resultado final de npm run test
- **Antes (com api.test.ts removido):** 39 testes passaram
- **Depois (após restauração):** 58 testes passaram (19 testes em api.test.ts + 39 testes nos outros arquivos)
- ✅ Suíte frontend restaurada para 56+ testes (cobertura LOG-011 + LOG-012)

### Resultado final de npm run lint
- ✅ Passou sem erros

### Resultado final de npm run build
- ✅ Sucesso (Next.js build compilado)

### Resultado final de pytest
- ✅ 105 testes passaram (incluindo 3 novos testes para LOG-012)
- ✅ 1 warning (StarletteDeprecationWarning sobre httpx)

### Resultado final de ruff
- ✅ All checks passed

### Conclusão sobre ausência de regressão
✅ **Nenhuma regressão detectada**
- Cobertura do LOG-011 foi totalmente preservada
- Cobertura do LOG-012 foi adicionada sem conflitos
- api.test.ts foi restaurado e estendido com testes mínimos para getDeliveryDetail
- Todos os testes backend e frontend estão passando
- Lint e build estão limpos
