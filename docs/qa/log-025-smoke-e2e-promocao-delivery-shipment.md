# LOG-025 — Smoke Gate E2E da promoção Delivery → Shipment

## Data/Hora
2026-06-06 02:40

## Branch
feature/selecao-transportadora-promocao

## Commit
0c0ffe3 docs(qa): registra atualizacao do projeto promocao Delivery para Shipment

## PR relacionado
PR #3: https://github.com/Dev-RuiDiniz/Ilex_Logistica/pull/3

## Objetivo
Executar Smoke Gate E2E da promoção manual Delivery → Shipment, validando o fluxo completo localmente.

## Baseline automatizado

### Backend
- pytest: 113/113 passando
- ruff: All checks passed

### Frontend
- npm run lint: Passou
- npm run test: 60/60 passando
- npm run build: Sucesso

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
- Status: Iniciado com sucesso
- Login: http://localhost:3000/login (acessível)
- Detalhe de Delivery: /shipments/deliveries/{delivery_id} (acessível)

## Endpoints testados

### 1. Login
- Endpoint: POST /api/v1/auth/login
- Status: NOT EXECUTED
- Motivo: Requer usuário válido com credenciais conhecidas
- Observação: Não foi possível testar sem usuário smoke pré-criado

### 2. Listagem de deliveries
- Endpoint: GET /api/v1/imports/deliveries
- Status: PASS
- Resultado: 200 OK
- Observação: Retornou lista de deliveries incluindo Delivery ID 3 (NF-SMOKE-003)

### 3. Detalhe de Delivery
- Endpoint: GET /api/v1/imports/deliveries/{delivery_id}
- Status: PASS
- Resultado: 200 OK
- Delivery ID: 3
- Dados: NF-SMOKE-003, Transportadora Smoke, 2026-01-17, 150.75, 11.0%

### 4. Listagem de carriers
- Endpoint: GET /api/v1/carriers
- Status: NOT EXECUTED
- Motivo: Requer autenticação
- Erro: {"detail":"Not authenticated"}

### 5. Promoção
- Endpoint: POST /api/v1/imports/deliveries/{delivery_id}/promote
- Status: NOT EXECUTED
- Motivo: Requer autenticação
- Observação: Não foi possível testar sem token válido

### 6. Validação de Shipment
- Endpoint: GET /api/v1/shipments/{shipment_id}
- Status: NOT EXECUTED
- Motivo: Depende do sucesso da promoção

## Smoke checklist

### Checklist LOG-025

1. Abrir login: NOT EXECUTED (requer validação manual)
2. Login com usuário autorizado: NOT EXECUTED (requer usuário válido)
3. Abrir listagem de deliveries: NOT EXECUTED (requer validação manual)
4. Acessar detalhe de uma Delivery: NOT EXECUTED (requer validação manual)
5. Confirmar dados da Delivery: NOT EXECUTED (requer validação manual)
6. Abrir seção "Promover para Shipment": NOT EXECUTED (requer validação manual)
7. Confirmar que o select de transportadora carrega: NOT EXECUTED (requer validação manual)
8. Selecionar transportadora: NOT EXECUTED (requer validação manual)
9. Preencher campos obrigatórios: NOT EXECUTED (requer validação manual)
10. Submeter promoção: NOT EXECUTED (requer validação manual)
11. Confirmar mensagem de sucesso: NOT EXECUTED (requer validação manual)
12. Confirmar dados do Shipment criado: NOT EXECUTED (requer validação manual)
13. Testar erro com tracking_code duplicado: NOT EXECUTED (requer validação manual)
14. Testar erro com campo obrigatório vazio: NOT EXECUTED (requer validação manual)
15. Confirmar que Delivery original permanece acessível: NOT EXECUTED (requer validação manual)
16. Confirmar que não aparece stack trace na UI: NOT EXECUTED (requer validação manual)

## Resultados PASS/FAIL/BLOCKED

### PASS
- Backend operacional
- Frontend operacional
- Listagem de deliveries via API
- Detalhe de Delivery via API
- Baseline automatizado completo

### NOT EXECUTED
- Login/autenticação (requer usuário válido)
- Listagem de carriers (requer autenticação)
- Promoção (requer autenticação)
- Validação de Shipment (depende da promoção)
- Smoke checklist manual (requer validação manual)

### FAIL
- Nenhum

### BLOCKED
- Autenticação (bloqueia endpoints protegidos)
- Validação manual UI (bloqueia smoke completo)

## Limitações

1. **Autenticação**: Não foi possível testar endpoints protegidos sem usuário smoke pré-criado com credenciais conhecidas
2. **Validação manual UI**: O agente não consegue validar via navegador diretamente, requer validação manual de Rafael
3. **Smoke incompleto**: O smoke gate foi parcialmente executado devido às limitações acima

## Riscos

1. **Endpoints protegidos não testados**: Carriers e promoção não foram testados via API
2. **Fluxo completo não validado**: O fluxo completo de promoção não foi validado end-to-end
3. **UI não validada**: A interface de promoção não foi validada manualmente

## Pendências

1. Criar usuário smoke com credenciais conhecidas para testes automatizados
2. Executar validação manual de Rafael para smoke checklist UI
3. Validar endpoints protegidos com autenticação válida
4. Completar smoke gate E2E com fluxo completo

## Confirmação de governança

- Nenhum merge foi feito
- Nenhum rebase foi feito
- Nenhuma migration foi criada
- Nenhuma alteração funcional foi feita
- Nenhum push foi feito

## Confirmação de alteração funcional

- Nenhuma alteração funcional foi feita durante o smoke gate
- Apenas documentação foi criada

## Próximos passos

1. Solicitar validação manual de Rafael para smoke checklist UI
2. Criar usuário smoke para testes automatizados futuros
3. Completar smoke gate E2E com autenticação válida
4. Aguardar review/merge do PR #3
