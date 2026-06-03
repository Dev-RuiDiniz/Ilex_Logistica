# LOG-011 — Listagem de entregas (Backend/API)

## Data/Hora
2026-06-03

## Branch Utilizada
- **Branch**: `feature/listagem-entregas`
- **Base**: `feature/persistencia-entregas-importacao` (hash: `069b691`)
- **Empilhada sobre**: LOG-010 (persistência de entregas e histórico de importação)

## Commits Base
- `bd0b22f` — LOG-007: estabiliza importador csv e excel
- `19587ec` — LOG-008: valida colunas obrigatórias antes do processamento
- `069b691` — LOG-010: persiste entregas e histórico de importação

## Contexto

Implementar backend/API para listagem de entregas persistidas pelo importador CSV/Excel (LOG-007/LOG-008/LOG-010). Esta entrega fecha apenas a fatia Backend/API do LOG-011. A fatia Web (interface) segue pendente.

---

## Arquitetura Encontrada

### Modelos Existente
- `Delivery` (tabela `deliveries`) — módulo `imports` — campos: `nf`, `transportadora`, `data_coleta`, `valor_frete`, `percentual_frete`, `created_at`
- `Shipment` (tabela `shipments`) — módulo `shipments` — modelo distinto, com listagem completa (paginação, filtros, ordenação)

### Lacuna Identificada
- Não há relacionamento entre `Delivery` e `Shipment`. São tabelas distintas.
- `Delivery` é usado pelo importador CSV/Excel (LOG-007/LOG-008/LOG-010).
- `Shipment` é usado pelo módulo `shipments` com listagem completa.
- **Endpoint de listagem de `Delivery` não existia**. Apenas `persist_deliveries()` persistia no banco.

### Padrão de Paginação Existente
- `ShipmentListResponse` usa `page`, `page_size`, `total`, `items`.
- Filtros: `status`, `carrier_id`, `criticality`, `tracking_code`, `estimated_delivery_from`, `estimated_delivery_to`.
- Ordenação: `created_at desc`, `id desc`.

---

## Implementação Backend/API

### Endpoint Criado
- `GET /api/v1/imports/deliveries`
- Router: `app/modules/imports/router.py`
- Parâmetros:
  - `page` (Query, default=1, ge=1)
  - `page_size` (Query, default=20, ge=1, le=100)
  - `nf` (Query, opcional)
  - `transportadora` (Query, opcional)
  - `data_coleta` (Query, opcional, formato ISO YYYY-MM-DD)

### Schemas Criados
- `DeliveryListItem` — campos: `id`, `nf`, `transportadora`, `data_coleta`, `valor_frete`, `percentual_frete`, `created_at`
- `DeliveryListResponse` — campos: `items`, `total`, `page`, `page_size`

### Filtros Implementados
- `nf` — filtro exato por nota fiscal
- `transportadora` — filtro exato por transportadora
- `data_coleta` — filtro exato por data de coleta (formato ISO)

### Paginação Implementada
- Padrão: `page` e `page_size`
- Validação: `page >= 1`, `page_size` entre 1 e 100
- Offset: `(page - 1) * page_size`
- Total count antes da paginação

### Ordenação Implementada
- `created_at desc` (mais recentes primeiro)
- `id desc` (desempate)

---

## Testes Red Criados

10 testes adicionados em `tests/test_imports.py`:

1. `test_listar_entregas_vazia_retorna_lista_vazia` — lista vazia sem dados
2. `test_listar_entregas_apos_importacao_retorna_dados` — lista dados após importação
3. `test_listar_entregas_paginacao_page_size` — paginação com 25 itens
4. `test_listar_entregas_ordenacao_previsivel` — ordenação previsível
5. `test_listar_entregas_filtro_nf` — filtro por nf
6. `test_listar_entregas_filtro_transportadora` — filtro por transportadora
7. `test_listar_entregas_filtro_data_coleta` — filtro por data_coleta
8. `test_listar_entregas_combinacao_filtros` — combinação de filtros
9. `test_listar_entregas_parametros_invalidos_paginacao` — validação de parâmetros
10. `test_listar_entregas_resposta_nao_expoe_stack_trace` — segurança de resposta

---

## Implementação Green

### Arquivos Modificados
- `app/modules/imports/router.py` — adicionado endpoint `list_deliveries_endpoint`
- `app/modules/imports/schemas.py` — adicionados `DeliveryListItem` e `DeliveryListResponse`
- `app/modules/imports/service.py` — adicionada função `list_deliveries`
- `tests/test_imports.py` — adicionados 10 testes do LOG-011

### Comandos Executados
```bash
cd apps/api
.venv\Scripts\Activate.ps1
pytest tests -k "listar_entregas" -v
pytest tests -v
ruff check .
```

---

## Resultado dos Testes

### Testes Específicos LOG-011
```
tests/test_imports.py::test_listar_entregas_vazia_retorna_lista_vazia PASSED
tests/test_imports.py::test_listar_entregas_apos_importacao_retorna_dados PASSED
tests/test_imports.py::test_listar_entregas_paginacao_page_size PASSED
tests/test_imports.py::test_listar_entregas_ordenacao_previsivel PASSED
tests/test_imports.py::test_listar_entregas_filtro_nf PASSED
tests/test_imports.py::test_listar_entregas_filtro_transportadora PASSED
tests/test_imports.py::test_listar_entregas_filtro_data_coleta PASSED
tests/test_imports.py::test_listar_entregas_combinacao_filtros PASSED
tests/test_imports.py::test_listar_entregas_parametros_invalidos_paginacao PASSED
tests/test_imports.py::test_listar_entregas_resposta_nao_expoe_stack_trace PASSED
```
**Resultado**: 10/10 passados ✅

### Pytest Completo
```
102 passed, 1 warning in 22.90s
```
**Resultado**: 102/102 passados ✅

### Ruff Check
```
All checks passed!
```
**Resultado**: Sem erros ✅

---

## Riscos

- **Baixo risco**: implementação mínima seguindo padrão existente (`shipments`)
- **Sem migração de banco**: `Delivery` já existe com todos os campos necessários
- **Sem alteração em outros módulos**: mudança isolada em `imports`

---

## Pendências

- **LOG-011 Web**: interface para listagem de entregas (fora do escopo desta entrega)
- **LOG-012**: detalhe da entrega (fora do escopo)
- **LOG-029/LOG-031**: filtros avançados (busca parcial, faixas de data, ordenação customizada) — fora do escopo

---

## Limite Claro

- ✅ **LOG-011 Backend/API concluído**: endpoint, schemas, filtros básicos, paginação, ordenação, testes
- ⏳ **LOG-011 Web pendente**: interface para consumir o endpoint
- ❌ **LOG-012 fora do escopo**: detalhe da entrega
- ❌ **LOG-029/LOG-031 fora do escopo**: filtros avançados

---

## Governança

- **Nenhum push realizado**
- **Nenhum PR criado**
- **Nenhum merge realizado**
- **Nenhum rebase realizado**
- **Nenhum commit criado** (aguardando autorização de Rafael)
- **Branch principal não alterada**
- **Histórico não sobrescrito**
