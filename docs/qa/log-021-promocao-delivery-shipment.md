# LOG-021: Promoção manual Delivery → Shipment

## Resumo executivo

* **Endpoint implementado**: `POST /api/v1/imports/deliveries/{delivery_id}/promote`
* **Funcionalidade**: Promoção manual de Delivery existente para Shipment
* **Arquitetura**: Delivery permanece como entidade de staging/auditoria, Shipment permanece como entidade operacional
* **Status**: Implementação completa, testes passando, sem migration necessária

## Migration Gate

### Viabilidade sem migration
* **Sim**, foi viável implementar sem migration
* **Confirmação**: Nenhuma migration foi criada
* **Justificativa**: A promoção é uma operação de cópia de dados de Delivery para Shipment, sem alteração de schema existente

### Regra de idempotência
* **Base**: `tracking_code` único na tabela `shipments`
* **Implementação**: Verificação de duplicidade de `tracking_code` antes de criar Shipment
* **Comportamento**: Retorna HTTP 409 Conflict se `tracking_code` já existir

### Limitações por não haver FK Delivery → Shipment
* **Sem vínculo técnico**: Não há foreign key de Delivery para Shipment
* **Sem rastreabilidade automática**: Não é possível consultar todos os Shipments derivados de um Delivery via SQL
* **Sem integridade referencial**: Não há garantia de integridade referencial no banco
* **Mitigação**: A auditoria pode ser feita via campo `invoice_number` que mapeia para `nf` do Delivery

## Contrato final do endpoint

### Endpoint
```
POST /api/v1/imports/deliveries/{delivery_id}/promote
```

### Payload (PromoteDeliveryRequest)
```json
{
  "tracking_code": "string (obrigatório)",
  "carrier_id": "integer (obrigatório)",
  "estimated_delivery": "datetime (obrigatório)",
  "recipient_name": "string (obrigatório)",
  "recipient_phone": "string (obrigatório)",
  "origin_address": "string (obrigatório)",
  "destination_address": "string (obrigatório)",
  "shipment_status": "string (opcional, default: 'pending')"
}
```

### Response (PromoteDeliveryResponse)
```json
{
  "id": "integer",
  "tracking_code": "string",
  "carrier_id": "integer",
  "status": "string",
  "estimated_delivery": "datetime",
  "recipient_name": "string",
  "recipient_phone": "string",
  "origin_address": "string",
  "destination_address": "string",
  "amount": "float | null",
  "invoice_number": "string | null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Permissões
* **Autenticação**: Exigida (retorna 401 se não autenticado)
* **Autorização**: Qualquer usuário autenticado pode promover (sem verificação de permissão específica)

### Erros

| Código | Mensagem | Causa |
|--------|----------|-------|
| 401 | Não autenticado | Usuário não autenticado |
| 404 | "entrega nao encontrada" | Delivery inexistente |
| 404 | "carrier nao encontrado" | Carrier inexistente |
| 409 | "tracking_code ja existe" | Duplicidade de tracking_code |
| 422 | Validação Pydantic | Payload inválido (campo obrigatório ausente) |

## TDD Red → Green

### Testes criados (test_promote_delivery.py)
1. `test_promote_delivery_cria_shipment_com_payload_completo` - Criação bem-sucedida
2. `test_promote_delivery_inexistente_retorna_404` - Delivery inexistente
3. `test_promote_delivery_rejeita_payload_sem_campo_obrigatorio` - Validação de payload
4. `test_promote_delivery_rejeita_carrier_inexistente` - Carrier inexistente
5. `test_promote_delivery_impede_duplicidade_por_tracking_code` - Idempotência
6. `test_promote_delivery_preserva_delivery_original` - Preservação de Delivery
7. `test_promote_delivery_exige_autenticacao` - Autenticação
8. `test_promote_delivery_resposta_nao_expoe_stack_trace` - Segurança

### Falhas iniciais
* **404 Not Found**: Carrier não estava sendo criado nos testes
* **NameError**: `shipment_status` não definido em `persist_import_history`
* **Erro de status code**: `status.HTTP_` não estava importado corretamente

### Correções aplicadas
1. Criação de Carrier antes de promover Delivery nos testes
2. Correção de `status=shipment_status` para `status=status` em `persist_import_history`
3. Substituição global de `status.HTTP_` por `http_status.HTTP_` em service.py
4. Correção de `_parse_date` para rejeitar data ausente
5. Melhoria da mensagem de duplicidade para incluir número da NF

## Recovery Gate

### Erro "old_string not found"
* **Causa**: Múltiplas tentativas de edição com strings não encontradas devido a formatação incorreta
* **Como foi destravado**: Reescrita completa do arquivo service.py com formatação correta
* **Causa real do 404**: Carrier não estava sendo criado nos testes antes de promover Delivery
* **Correção aplicada**: Adicionar criação de Carrier nos testes antes de chamar o endpoint de promoção

## Regression Gate

### Correções em service.py
1. **Import correto**: `from fastapi import status as http_status`
2. **Substituição global**: `status.HTTP_` → `http_status.HTTP_` (22 ocorrências)
3. **persist_import_history**: `status=status` (parâmetro correto)
4. **_parse_date**: Retorna `date` obrigatório, rejeita valor ausente
5. **Mensagem de duplicidade**: Inclui "duplicidade" e número da NF

### Risco de impacto no importador
* **Alto**: service.py é usado por todo o importador
* **Mitigação**: Execução completa de test_imports.py (51/51 passando)

### Validação de test_imports.py
* **Resultado**: 51/51 testes passando
* **Cobertura**: Upload CSV/XLSX, validação, persistência, listagem, detalhes

### Validação de test_promote_delivery.py
* **Resultado**: 8/8 testes passando
* **Cobertura**: Promoção, validação, idempotência, autenticação, segurança

### Pytest completo
* **Total**: 113 testes
* **Resultado**: 113/113 passando
* **Tempo**: 28.23s

### Ruff
* **Resultado**: All checks passed
* **Ação**: Removido service_backup.py (arquivo de backup corrompido)

### Frontend lint/test/build
* **Lint**: Passou
* **Test**: 58/58 passando
* **Build**: Sucesso

## Arquivos alterados

### Backend
1. `apps/api/app/modules/imports/service.py` - Correções de status code, _parse_date, mensagem de duplicidade, função promote_delivery_to_shipment
2. `apps/api/app/modules/imports/router.py` - Endpoint POST /deliveries/{delivery_id}/promote
3. `apps/api/app/modules/imports/schemas.py` - Schemas PromoteDeliveryRequest e PromoteDeliveryResponse
4. `apps/api/app/modules/carriers/models.py` - Alteração menor (1 linha)
5. `apps/api/tests/test_promote_delivery.py` - NOVO: 8 testes para promoção Delivery → Shipment

### Frontend
* **Nenhuma alteração** (conforme governança)

### Documentação
* `docs/qa/log-021-promocao-delivery-shipment.md` - NOVO: Documentação completa do LOG-021

## Governança

* ✓ Sem push
* ✓ Sem PR
* ✓ Sem merge
* ✓ Sem rebase
* ✓ Sem migration
* ✓ Sem commit (ainda)
* ✓ Sem alteração frontend

## Estado final do Git

### Branch
* `feature/promocao-delivery-shipment`

### Arquivos modificados
```
 apps/api/app/modules/carriers/models.py |   2 +-
 apps/api/app/modules/imports/router.py  |  27 +++-
 apps/api/app/modules/imports/schemas.py |  28 ++++
 apps/api/app/modules/imports/service.py | 244 ++++++++++++++++++++++----------
 4 files changed, 227 insertions(+), 74 deletions)
```

### Arquivos novos
```
 apps/api/tests/test_promote_delivery.py
 docs/qa/log-021-promocao-delivery-shipment.md
```

### Migrations
* **Nenhuma migration criada**

## Riscos e pendências

### Riscos
1. **Sem FK Delivery → Shipment**: Não há vínculo técnico entre as entidades
2. **Sem rastreabilidade automática**: Não é possível consultar todos os Shipments derivados de um Delivery via SQL
3. **Impacto em service.py**: Correções afetam todo o importador (mitigado por testes completos)

### Pendências
* **Nenhuma pendência técnica**

## Próximo prompt recomendado

**Commit local** - Todas as validações passaram, código está pronto para commit local com mensagem descritiva das alterações do LOG-021.
