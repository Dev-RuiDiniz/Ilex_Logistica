# BETA-011A - Backend dos Campos Fiscais/Financeiros e Filtros Avançados

## Escopo

Implementação backend-only do Épico 3 - Campos fiscais, financeiros e filtros do Apêndice 1, seguindo TDD obrigatório.

## Base Usada

**Branch Base:** origin/feature/beta-010-functional-epic-audit (BETA-010)

**Branch Empilhada:** feature/beta-011a-shipment-fiscal-financial-backend

**Razão:** Esta branch empilhada implementa o backend dos campos fiscais/financeiros sobre a auditoria funcional do BETA-010.

## Campos Adicionados/Normalizados

### Novos Campos no Model Shipment

- `freight_value` (Numeric(10, 2)): Valor do frete
- `invoice_value` (Numeric(10, 2)): Valor da nota fiscal
- `freight_percentage` (Numeric(5, 2)): Percentual do frete (calculado automaticamente)
- `collection_departure_date` (DateTime): Data de coleta/saída
- `customer_name` (String(255)): Nome do cliente
- `destination_uf` (String(2)): UF de destino

### Regras de Cálculo

**freight_percentage = freight_value / invoice_value * 100**

- Retorna `None` quando `invoice_value` é zero
- Retorna `None` quando `invoice_value` é `None`
- Retorna `None` quando `freight_value` é `None`
- Cálculo automático via SQLAlchemy event listener (before_insert, before_update)

### Índices Criados

- `ix_shipments_customer_name`: Índice para filtro por cliente
- `ix_shipments_destination_uf`: Índice para filtro por UF
- `ix_shipments_invoice_number`: Índice para busca por NF

**Nota:** `status`, `criticality`, e `estimated_delivery` já possuíam índices no model.

## Filtros Implementados

### Filtros Backend (list_shipments)

- `customer_name`: Filtro por nome do cliente (ilike, case-insensitive)
- `destination_uf`: Filtro por UF de destino (exato)
- `month`: Filtro por mês (extract('month', estimated_delivery))
- `year`: Filtro por ano (extract('year', estimated_delivery))
- `search`: Busca global across multiple fields

### Busca Global

O parâmetro `search` busca nos seguintes campos:
- `tracking_code`: Código de rastreio
- `invoice_number`: Número da nota fiscal
- `customer_name`: Nome do cliente
- `destination_uf`: UF de destino

Usa `or_` com `ilike` para busca case-insensitive em múltiplos campos.

## Testes Criados

### test_shipment_fiscal_financial_fields.py (9 testes)

1. `test_shipment_with_fiscal_financial_fields`: Cria entrega com campos fiscais/financeiros
2. `test_freight_percentage_calculation`: Calcula percentual corretamente
3. `test_freight_percentage_null_when_invoice_value_zero`: Retorna null quando valor da NF é zero
4. `test_freight_percentage_null_when_invoice_value_null`: Retorna null quando valor da NF está ausente
5. `test_freight_percentage_null_when_freight_value_null`: Retorna null quando valor do frete está ausente
6. `test_collection_departure_date_persistence`: Persiste data de coleta/saída
7. `test_fiscal_financial_fields_in_list_schema`: Expõe campos na listagem
8. `test_fiscal_financial_fields_in_detail_schema`: Expõe campos no detalhe
9. `test_backward_compatibility_with_old_shipments`: Mantém compatibilidade com registros antigos

### test_shipments_advanced_filters.py (12 testes)

1. `test_filter_by_customer_name`: Filtra por cliente
2. `test_filter_by_destination_uf`: Filtra por UF
3. `test_filter_by_month`: Filtra por mês
4. `test_filter_by_year`: Filtra por ano
5. `test_return_all_when_temporal_filter_absent`: Retorna todo período sem filtro temporal
6. `test_search_by_invoice_number`: Busca por NF
7. `test_search_by_customer_name`: Busca por cliente
8. `test_search_by_tracking_code`: Busca por rastreio
9. `test_search_by_carrier_name`: Busca por transportadora (carrier_id)
10. `test_combine_filters_without_conflict`: Combina filtros sem conflito
11. `test_return_empty_when_no_match`: Retorna lista vazia quando nenhum registro corresponde
12. `test_respect_existing_authentication_authorization`: Respeita autenticação/autorização existente

## Migration

**Arquivo:** `apps/api/migrations/versions/20260608_01_add_fiscal_financial_fields.py`

**Revision ID:** 20260608_01
**Revises:** 20260515_04

**Upgrade:**
- Adiciona 6 novos campos à tabela `shipments`
- Cria 3 índices para novos campos

**Downgrade:**
- Remove 3 índices
- Remove 6 campos

**Validação:** ✅ Passou em `python scripts/validate_migrations.py`

## Arquivos Modificados

### Backend

1. `apps/api/app/modules/shipments/models.py`
   - Adicionado import `event` do SQLAlchemy
   - Adicionada função `calculate_freight_percentage`
   - Adicionados 6 novos campos ao model `Shipment`
   - Adicionado event listener para cálculo automático de `freight_percentage`

2. `apps/api/app/modules/shipments/schemas.py`
   - Adicionados 6 novos campos a `ShipmentListItem`
   - `ShipmentDetailResponse` herda automaticamente os novos campos

3. `apps/api/app/modules/shipments/service.py`
   - Adicionado import `extract` do SQLAlchemy
   - Adicionado import `calculate_freight_percentage` do models
   - Adicionados 5 novos parâmetros a `list_shipments`
   - Adicionada lógica de filtro para novos parâmetros
   - Adicionados 6 novos campos ao response de `list_shipments`
   - Adicionados 6 novos campos ao response de `list_exception_shipments`
   - Atualizado `process_import` para parsear novos campos
   - Atualizado `process_import` para calcular `freight_percentage`

4. `apps/api/app/modules/shipments/router.py`
   - Adicionados 5 novos Query parameters a `list_shipments_endpoint`
   - Adicionados 5 novos Query parameters a `list_exceptions_endpoint`
   - Passados novos parâmetros para functions de service

### Migrations

5. `apps/api/migrations/versions/20260608_01_add_fiscal_financial_fields.py`
   - Nova migration para campos fiscais/financeiros

### Testes

6. `apps/api/tests/test_shipment_fiscal_financial_fields.py`
   - Novo arquivo com 9 testes TDD

7. `apps/api/tests/test_shipments_advanced_filters.py`
   - Novo arquivo com 12 testes de filtros

## Evidência de Red → Green → Refactor

### Red (Testes Falhando)
- Criados 21 testes antes da implementação
- Testes validam comportamento esperado dos novos campos e filtros

### Green (Implementação)
- Implementados campos no model
- Implementados schemas
- Implementados filtros no service
- Implementados endpoints no router
- Implementada migration
- Implementado event listener para cálculo automático

### Refactor
- Centralizado cálculo de `freight_percentage` em função reutilizável
- Event listener automatiza cálculo antes de insert/update
- Não há duplicação de regra de negócio

## Comandos Executados

### Secret Scan
```bash
python scripts/check_secrets.py --repo-root .
```
**Resultado:** ✅ OK: No potential secrets found

### Self-Test
```bash
python scripts/check_secrets.py --repo-root . --self-test
```
**Resultado:** ✅ Self-test completed successfully (real)

### Validação de Migrations
```bash
python scripts/validate_migrations.py
```
**Resultado:** ✅ OK: Migration validation passed

### Validação Documental
```bash
python scripts/validate_docs.py
```
**Resultado:** ✅ OK: Documentation validation passed

### Validação Beta Agregada
```bash
python scripts/beta_validate.py
```
**Resultado:** ✅ OK: Beta validation passed

### Testes Específicos
```bash
python -m pytest tests/test_shipment_fiscal_financial_fields.py -v
```
**Resultado:** ✅ 9 passed, 1 warning

```bash
python -m pytest tests/test_shipments_advanced_filters.py -v
```
**Resultado:** ✅ 12 passed, 1 warning

### Testes API Completos
```bash
python -m pytest -v
```
**Resultado:** ✅ 134 passed, 1 warning

### Git Status
```bash
git status
```
**Resultado:** ✅ Working tree limpo, sem artefatos gerados

## Resultados

- ✅ Secret scan passou
- ✅ Self-test real passou
- ✅ Migrations passaram
- ✅ Validação documental passou
- ✅ Validação beta agregada passou
- ✅ Testes fiscais/financeiros passaram (9/9)
- ✅ Testes de filtros passaram (12/12)
- ✅ Testes API completos passaram (134/134)
- ✅ Nenhum artefato gerado no git status

## Limitações

### Backend-Only
- Este PR implementa apenas o backend
- Não há implementação frontend neste PR
- Não há implementação de importação Excel/XLSX neste PR
- Não há implementação de SLA neste PR
- Não há implementação de eficiência por transportadora neste PR

### Compatibilidade
- Registros antigos sem os novos campos continuam compatíveis
- Campos novos são nullable
- Não quebra importações existentes
- Não quebra listagem existente
- Não quebra detalhe existente

## O Que Ficou para BETA-011B

1. **Tabela frontend:** Exibir campos fiscais/financeiros na listagem
2. **Detalhe frontend:** Exibir campos fiscais/financeiros no detalhe
3. **Filtros frontend:** Implementar filtros avançados na UI
4. **Formatação BRL/percentual:** Formatar valores monetários e percentuais no frontend

## O Que Ficou para BETA-012

1. **Importação CSV/XLSX:** Importar campos fiscais/financeiros de arquivos
2. **Preview/confirmação:** Preview e confirmação de importação
3. **Layout Braspress:** Layout específico para Braspress

## Confirmação de Governança

- ✅ Nenhum merge foi feito em main
- ✅ Nenhum rebase foi feito
- ✅ Nenhum git push --force foi usado
- ✅ Nenhum comando destrutivo foi usado
- ✅ Branch criada a partir de origin/feature/beta-010-functional-epic-audit
- ✅ Draft PR (sem merge automático)
- ✅ Commits em pt-BR com Conventional Commits e ID beta
- ✅ Backend-only (sem frontend)
- ✅ Sem importação Excel/XLSX
- ✅ Sem SLA
- ✅ Sem eficiência por transportadora
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
- ✅ TDD obrigatório seguido (Red → Green → Refactor)
- ✅ Testes novos criados e passando
- ✅ Validações oficiais Python passando

## Assinatura

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ✅ Concluído (BETA-011A - Backend dos Campos Fiscais/Financeiros e Filtros Avançados)
