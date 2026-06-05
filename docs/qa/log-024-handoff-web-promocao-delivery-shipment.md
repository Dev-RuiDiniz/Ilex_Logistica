# LOG-024 — Handoff Web Promoção Delivery → Shipment

## 1. Resumo executivo

LOG-022 e LOG-023 concluídos. Interface de promoção implementada com select de transportadora. Backend não alterado neste bloco. Nenhuma migration criada. Bloco Web pronto para PR ao final do turno.

## 2. Branch e commits

### Branch atual
feature/selecao-transportadora-promocao

### Branch base
feature/promocao-delivery-shipment-web

### Commit base
5ff315e feat(imports): adiciona promocao manual de Delivery para Shipment

### Commits do bloco Web
- 69a9a0f feat(imports): adiciona frontend para promocao de Delivery para Shipment (LOG-022)
- eeb3eed feat(imports): adiciona selecao de transportadora na promocao (LOG-023)

## 3. Escopo entregue

### LOG-022 — Frontend da promoção manual Delivery → Shipment
- Tipos PromoteDeliveryRequest e PromoteDeliveryResponse criados
- Função API promoteDeliveryToShipment(token, deliveryId, payload) criada
- Testes de assinatura adicionados (2 testes)
- Formulário "Promover para Shipment" na página de detalhe de Delivery
- Estados loading/erro/sucesso implementados
- Feedback do Shipment criado após sucesso
- Mensagens de erro seguras, sem stack trace
- Delivery original permanece preservado

### LOG-023 — Seleção de transportadora no formulário de promoção
- Input manual de carrier_id substituído por select de transportadoras
- Reutilização da função existente listCarriers(token, includeInactive)
- Reutilização do tipo Carrier existente
- Carriers carregados ao abrir o formulário
- Select exibe carrier.name e envia carrier.id no payload
- Estados adicionados: carriers, carriersLoading, carriersError
- Estados existentes de loading/erro/sucesso preservados
- Fallback seguro se carriers não carregarem

## 4. Validações

### Frontend
- npm run lint: Passou
- npm run test: 60/60 passando
- npm run build: Sucesso

### Backend regressivo
- pytest: 113/113 passando
- ruff: All checks passed

## 5. Smoke checklist manual

1. Login com usuário autorizado
2. Abrir listagem de deliveries
3. Abrir detalhe de uma Delivery
4. Abrir seção Promover para Shipment
5. Confirmar que carriers carregam
6. Selecionar transportadora
7. Preencher campos obrigatórios (tracking_code, estimated_delivery, recipient_name, recipient_phone, origin_address, destination_address)
8. Submeter promoção
9. Confirmar mensagem de sucesso
10. Confirmar dados do Shipment criado (ID, tracking_code, status)
11. Testar erro com tracking_code duplicado
12. Testar erro sem campo obrigatório
13. Confirmar que Delivery original permanece visível

## 6. Riscos

- PR empilhado sobre PR #2
- PR #2 empilhado sobre PR #1
- Sem validação manual browser completa, se não executada
- Se carriers não carregarem, promoção fica bloqueada
- Apenas backend valida duplicidade de tracking_code
- LOG-A04 Docker/WSL2 segue pendente
- Select não filtra apenas carriers ativos (listCarriers retorna todos)

## 7. Estratégia de PR ao final do turno

### PR do bloco Web
- Base: feature/promocao-delivery-shipment
- Head: feature/selecao-transportadora-promocao
- Título sugerido: feat(imports): frontend promocao Delivery para Shipment (LOG-022/023)

### Ordem recomendada de merge
1. PR #1 primeiro (fase operacional LOG-016 a LOG-018)
2. PR #2 depois (trilha LOG-019 a LOG-021)
3. PR Web LOG-022/023 depois (bloco Web de promoção)

## 8. Governança

- Nenhum push até autorização
- Nenhum PR até final do turno
- Nenhum merge
- Nenhum rebase
- Nenhuma migration
- Nenhum backend alterado neste bloco
- Merge exclusivo do supervisor humano

## 9. Arquivos alterados no bloco Web

### LOG-022
- apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx (modificado)
- apps/web/src/lib/api.test.ts (modificado)
- apps/web/src/lib/api.ts (modificado)
- apps/web/src/lib/types.ts (modificado)
- docs/qa/log-022-promocao-delivery-shipment-web.md (novo)

### LOG-023
- apps/web/src/app/(private)/shipments/deliveries/[id]/page.tsx (modificado)
- docs/qa/log-023-selecao-transportadora-promocao.md (novo)

## 10. Pendências

- Nenhuma pendência técnica
- Aguardar orientação de Rafael para criação de PR ao final do turno
