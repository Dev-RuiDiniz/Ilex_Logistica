# LOG-028 — Smoke autenticado da promoção Delivery → Shipment

## Data/Hora
2026-06-06 01:30

## Branch
feature/smoke-autenticado-promocao

## Branch base
feature/selecao-transportadora-promocao

## PR relacionado
PR #3: https://github.com/Dev-RuiDiniz/Ilex_Logistica/pull/3

## Objetivo
Executar smoke autenticado do fluxo Delivery → Shipment e documentar o resultado real, validando endpoints protegidos que ficaram pendentes no LOG-025.

## Baseline automatizado

### Backend
- pytest: 113/113 passando
- ruff: All checks passed

### Frontend
- npm run lint: Passou
- npm run test: 60/60 passando
- npm run build: Sucesso

## Usuário smoke

### Estado
- Usuário smoke existe: Sim
- Método de criação: Script local (banco local)
- Email: smoke@ilex.com
- Senha: [NÃO REGISTRADA]
- User ID: 2
- Roles: admin, logistica

## Backend local

### Estado
- URL: http://127.0.0.1:8000
- Porta: 8000
- Status: Iniciado com sucesso
- Swagger UI: http://127.0.0.1:8000/docs (200 OK)
- OpenAPI: http://127.0.0.1:8000/openapi.json (200 OK)

## Frontend local

### Estado
- URL: http://localhost:3000
- Porta: 3000
- Status: Não iniciado (smoke UI via navegador BLOCKED)

## Endpoints autenticados testados

### 1. Login
- Endpoint: POST /api/v1/auth/login
- Status: PASS
- Resultado: 200 OK
- Observação: Token de acesso gerado com sucesso
- Token: [NÃO REGISTRADO]

### 2. Listagem de deliveries
- Endpoint: GET /api/v1/imports/deliveries
- Status: PASS
- Resultado: 200 OK
- Total deliveries: 3
- Observação: Autenticação funcionando corretamente

### 3. Detalhe de Delivery
- Endpoint: GET /api/v1/imports/deliveries/{delivery_id}
- Status: PASS
- Resultado: 200 OK
- Delivery ID: 3
- Dados: NF-SMOKE-003, Transportadora Smoke, 2026-01-17, 150.75, 11.0%
- Observação: Autenticação funcionando corretamente

### 4. Listagem de carriers
- Endpoint: GET /api/v1/carriers
- Status: PASS
- Resultado: 200 OK
- Total carriers: 1
- Carrier ID: 1
- Carrier Name: Carrier Smoke
- Observação: Autenticação funcionando corretamente

### 5. Promoção válida
- Endpoint: POST /api/v1/imports/deliveries/{delivery_id}/promote
- Status: PASS
- Resultado: 201 Created
- Delivery ID: 3
- Shipment ID: 1
- Tracking Code: TRACK-SMOKE-001
- Carrier ID: 1
- Payload válido:
  - tracking_code: TRACK-SMOKE-001
  - carrier_id: 1
  - estimated_delivery: 2026-06-10
  - recipient_name: Destinatario Smoke
  - recipient_phone: 11999999999
  - origin_address: Rua Origem, 123
  - destination_address: Rua Destino, 456
- Observação: Promoção autenticada funcionando corretamente

### 6. Validação de Shipment criado
- Endpoint: GET /api/v1/shipments/{shipment_id}
- Status: NOT EXECUTED
- Motivo: Endpoint não implementado ou não testado nesta execução
- Observação: Shipment foi criado com sucesso (ID 1)

### 7. Erro duplicidade de tracking_code
- Endpoint: POST /api/v1/imports/deliveries/{delivery_id}/promote
- Status: PASS
- Resultado: 409 Conflict
- Motivo: Tracking_code TRACK-SMOKE-001 já existe
- Observação: Validação de duplicidade funcionando corretamente

### 8. Erro campo obrigatório
- Endpoint: POST /api/v1/imports/deliveries/{delivery_id}/promote
- Status: PASS
- Resultado: 422 Unprocessable Entity
- Motivo: Campo destination_address ausente
- Observação: Validação de campos obrigatórios funcionando corretamente

## Smoke UI via navegador

### Status
BLOCKED

### Motivo
O agente não consegue validar via navegador diretamente, requer validação manual de Rafael.

### Checklist LOG-028

1. Abrir login: BLOCKED (requer validação manual)
2. Login com usuário autorizado: BLOCKED (requer validação manual)
3. Abrir listagem de deliveries: BLOCKED (requer validação manual)
4. Acessar detalhe de uma Delivery: BLOCKED (requer validação manual)
5. Confirmar dados da Delivery: BLOCKED (requer validação manual)
6. Abrir seção "Promover para Shipment": BLOCKED (requer validação manual)
7. Confirmar que o select de transportadora carrega: BLOCKED (requer validação manual)
8. Selecionar transportadora: BLOCKED (requer validação manual)
9. Preencher campos obrigatórios: BLOCKED (requer validação manual)
10. Submeter promoção: BLOCKED (requer validação manual)
11. Confirmar mensagem de sucesso: BLOCKED (requer validação manual)
12. Confirmar dados do Shipment criado: BLOCKED (requer validação manual)
13. Testar erro com tracking_code duplicado: BLOCKED (requer validação manual)
14. Testar erro com campo obrigatório vazio: BLOCKED (requer validação manual)
15. Confirmar que Delivery original permanece acessível: BLOCKED (requer validação manual)
16. Confirmar que não aparece stack trace na UI: BLOCKED (requer validação manual)

## Resultados PASS/FAIL/BLOCKED

### PASS
- Login autenticado (200)
- Listagem de deliveries autenticada (200)
- Detalhe de Delivery autenticado (200)
- Listagem de carriers autenticada (200)
- Promoção válida autenticada (201)
- Erro duplicidade de tracking_code (409)
- Erro campo obrigatório (422)
- Baseline automatizado completo

### BLOCKED
- Smoke UI via navegador (limitação do agente)

### FAIL
- Nenhum

### NOT EXECUTED
- Validação de Shipment criado (endpoint não testado)

## Evidências resumidas

### Backend autenticado
- Todos os endpoints protegidos testados funcionaram corretamente
- Autenticação JWT funcionando como esperado
- Validação de duplicidade de tracking_code funcionando
- Validação de campos obrigatórios funcionando
- Promoção Delivery → Shipment funcionando

### Dados criados
- Usuário smoke: smoke@ilex.com (ID: 2)
- Carrier smoke: Carrier Smoke (ID: 1)
- Shipment smoke: TRACK-SMOKE-001 (ID: 1)

## Bugs encontrados

Nenhum bug funcional encontrado durante o smoke autenticado.

## Limitações

1. **Smoke UI via navegador**: O agente não consegue validar via navegador diretamente, requer validação manual de Rafael
2. **Endpoint de validação de Shipment**: O endpoint GET /api/v1/shipments/{shipment_id} não foi testado nesta execução
3. **Smoke parcial**: O smoke gate foi parcialmente executado devido à limitação de validação UI

## Riscos

1. **UI não validada**: A interface de promoção não foi validada manualmente via navegador
2. **Fluxo completo UI não validado**: O fluxo completo de promoção via UI não foi validado end-to-end
3. **Endpoint de Shipment não testado**: A validação do Shipment criado não foi feita via API

## Pendências

1. Executar validação manual de Rafael para smoke checklist UI
2. Validar endpoint GET /api/v1/shipments/{shipment_id}
3. Completar smoke gate E2E com validação UI manual

## Confirmação de que nenhum segredo foi registrado

- Nenhuma senha foi registrada neste documento
- Nenhum token foi registrado neste documento
- Apenas IDs e status codes foram registrados

## Confirmação de que nenhuma migration foi criada

- Nenhuma migration foi criada durante o smoke autenticado
- Apenas dados de teste foram criados no banco local

## Confirmação de governança

- Nenhum merge foi feito
- Nenhum rebase foi feito
- Nenhuma alteração funcional foi feita no código
- Apenas documentação foi criada
- Nenhum push foi feito

## Confirmação de alteração funcional

- Nenhuma alteração funcional foi feita durante o smoke autenticado
- Apenas documentação foi criada
- Dados de teste foram criados no banco local (usuário smoke, carrier smoke, shipment smoke)

## Próximos passos

1. Solicitar validação manual de Rafael para smoke checklist UI
2. Validar endpoint GET /api/v1/shipments/{shipment_id}
3. Completar smoke gate E2E com validação UI manual
4. Aguardar review/merge do PR #3
5. Aguardar review/merge deste PR empilhado (LOG-028)
