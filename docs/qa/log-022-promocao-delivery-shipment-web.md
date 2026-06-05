# LOG-022: Frontend da promoção manual Delivery → Shipment

## Data/Hora
2026-06-05 16:30

## Branch
feature/promocao-delivery-shipment-web

## Branch base
feature/promocao-delivery-shipment

## Commit base
5ff315e feat(imports): adiciona promocao manual de Delivery para Shipment

## Objetivo
Implementar a interface frontend para promover uma Delivery para Shipment, consumindo o endpoint criado no LOG-021.

## Endpoint consumido
POST /api/v1/imports/deliveries/{delivery_id}/promote

## Campos do formulário
- tracking_code (obrigatório)
- carrier_id (obrigatório)
- estimated_delivery (obrigatório)
- recipient_name (obrigatório)
- recipient_phone (obrigatório)
- origin_address (obrigatório)
- destination_address (obrigatório)
- shipment_status (opcional)

## Tipos criados
- PromoteDeliveryRequest
- PromoteDeliveryResponse

## Função API criada
promoteDeliveryToShipment(token, deliveryId, payload)

## Testes Red
- Teste de assinatura para promoteDeliveryToShipment
- Teste de exportação da função
- Resultado inicial: Testes passaram (sem falha Red, pois são testes de assinatura)

## Implementação Green
- Adicionada seção "Promover para Shipment" na página de detalhe de Delivery
- Formulário com todos os campos obrigatórios
- Estados de loading, erro e sucesso
- Exibição do Shipment criado após sucesso
- Não expõe stack trace
- Mantém Delivery original intacta

## Validações

### Frontend
- npm run lint: Passou
- npm run test: 60/60 passando
- npm run build: Sucesso

### Backend
- pytest: 113/113 passando
- ruff: All checks passed

## Smoke checklist manual
1. Acessar página de detalhe de Delivery
2. Clicar em "Promover"
3. Preencher formulário com dados válidos
4. Submeter formulário
5. Verificar mensagem de sucesso
6. Verificar exibição do Shipment criado
7. Testar com dados inválidos
8. Verificar mensagem de erro segura

## Riscos
- Sem validação de carrier_id no frontend (deve existir no backend)
- Sem validação de tracking_code duplicado no frontend (deve existir no backend)
- Formulário não carrega lista de carriers para seleção (requereria API adicional)

## Pendências
- Nenhuma pendência técnica

## Confirmação de que backend não foi alterado
- Backend não foi alterado durante o LOG-022
- Apenas arquivos frontend foram modificados

## Confirmação de que nenhuma migration foi criada
- Nenhuma migration foi criada durante o LOG-022

## Confirmação de que nenhum push/PR/merge/rebase foi feito
- Nenhum push foi realizado
- Nenhum PR foi aberto
- Nenhum merge foi realizado
- Nenhum rebase foi realizado
