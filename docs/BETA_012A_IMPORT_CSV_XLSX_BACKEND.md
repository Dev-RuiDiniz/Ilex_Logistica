# BETA-012A: Importação CSV/XLSX Backend com Preview, Validação Linha a Linha e Confirmação

## Status
**Status:** Implementado  
**Branch:** `feature/beta-012a-import-csv-xlsx-backend-preview-confirm`  
**Base Branch:** `origin/feature/beta-011c-fix-frontend-build-test-blockers`  
**Tipo:** Backend-only (sem frontend)

## Objetivo

Implementar sistema de importação CSV/XLSX com preview, validação linha a linha, detecção de duplicidade e confirmação para importação de dados fiscais/financeiros de shipments.

## Escopo Implementado

### 1. Parser CSV/XLSX Melhorado
- ✅ Aceitar CSV e XLSX
- ✅ Validar colunas obrigatórias
- ✅ Normalizar nomes de colunas via mapper
- ✅ Converter datas brasileiras (DD/MM/YYYY, DD-MM-YYYY, ISO)
- ✅ Converter valores monetários brasileiros (1.234,56, 1234,56, R$ 1.234,56)
- ✅ Tratar linhas vazias
- ✅ Reportar erro por linha

**Arquivos:**
- `apps/api/app/modules/imports/service_v2.py` - Parser melhorado com suporte a formatos brasileiros
- `apps/api/app/modules/imports/mapper.py` - Mapeamento de colunas

### 2. Layout Mapper para Campos Fiscais/Financeiros
- ✅ Mapear campos: tracking_code, carrier_id, invoice_number, invoice_value, freight_value, collection_departure_date, customer_name, destination_uf
- ✅ Preservar compatibilidade com layout atual
- ✅ Preparar para layout Braspress futuro

**Arquivos:**
- `apps/api/app/modules/imports/mapper.py` - Layout mapper com variações de nomes de colunas

**Mapeamentos Suportados:**
- `tracking_code`: tracking_code, trackingcode, tracking, rastreio, codigo_rastreio, etc.
- `carrier_id`: carrier_id, carrierid, transportadora_id, id_transportadora, etc.
- `invoice_number`: invoice_number, nf, nota_fiscal, numero_nf, etc.
- `invoice_value`: invoice_value, valor_nf, valor_nota_fiscal, valor_mercadoria, etc.
- `freight_value`: freight_value, valor_frete, frete, vlr_frete, etc.
- `collection_departure_date`: collection_departure_date, data_coleta, data_de_coleta, dt_coleta, etc.
- `customer_name`: customer_name, cliente, nome_cliente, destinatario, etc.
- `destination_uf`: destination_uf, uf, uf_destino, estado, etc.

### 3. Validação Linha a Linha
- ✅ Retornar número da linha, dados normalizados, erros, warnings
- ✅ Validar rastreio, transportadora, NF, UF, valores monetários, datas
- ✅ Detectar duplicidade no arquivo (tracking_code + carrier_id, invoice_number + carrier_id)
- ✅ Detectar duplicidade contra banco

**Arquivos:**
- `apps/api/app/modules/imports/service_v2.py` - Funções de validação

**Validações Implementadas:**
- `tracking_code`: obrigatório, não vazio
- `carrier_id`: obrigatório, inteiro positivo
- `invoice_number`: obrigatório, não vazio
- `invoice_value`: obrigatório, formato brasileiro, positivo
- `freight_value`: obrigatório, formato brasileiro, não negativo
- `collection_departure_date`: obrigatório, formato brasileiro
- `customer_name`: obrigatório, não vazio
- `destination_uf`: obrigatório, 2 caracteres (sigla do estado)

### 4. Preview Sem Persistir
- ✅ Endpoint/service de preview
- ✅ Retornar resumo: total_rows, valid_rows, invalid_rows, duplicate_rows, errors, warnings, preview_items
- ✅ Não persistir entregas finais durante preview

**Arquivos:**
- `apps/api/app/modules/imports/service_v2.py` - Função `preview_import()`
- `apps/api/app/modules/imports/router.py` - Endpoint `POST /imports/preview`

**Endpoint:**
```
POST /api/v1/imports/preview
Content-Type: multipart/form-data

Response:
{
  "filename": "import.csv",
  "file_type": "csv",
  "file_hash": "sha256...",
  "total_rows": 100,
  "valid_rows": 95,
  "invalid_rows": 5,
  "duplicate_rows": 2,
  "preview_items": [...],  // Primeiras 10 linhas validadas
  "errors": [...],
  "warnings": [...]
}
```

### 5. Confirmação da Importação
- ✅ Endpoint/service de confirmação
- ✅ Confirmar apenas importação validada
- ✅ Bloquear confirmação quando houver erro bloqueante
- ✅ Persistir entregas válidas com campos fiscais/financeiros
- ✅ Registrar histórico completed/failed
- ✅ Atualizar contadores

**Arquivos:**
- `apps/api/app/modules/imports/service_v2.py` - Função `confirm_import()`
- `apps/api/app/modules/imports/router.py` - Endpoint `POST /imports/confirm` (placeholder - requer gerenciamento de estado)

**Nota:** O endpoint de confirmação atualmente retorna 501 (Not Implemented) pois requer gerenciamento de estado (cache/session) para armazenar o preview entre as chamadas. Em produção, isso seria implementado com Redis ou similar.

### 6. Histórico de Importação
- ✅ Atualizar ImportHistory com campos: source, metadata, imported_by
- ✅ Criar migration se necessário

**Arquivos:**
- `apps/api/migrations/versions/20260610_01_add_import_history_metadata.py` - Migration
- `apps/api/app/modules/imports/models.py` - Model atualizado

**Novos Campos:**
- `source`: str (50) - Origem da importação (ex: "csv_xlsx_import")
- `metadata`: text - JSON com metadados adicionais
- `imported_by`: int - ID do usuário que realizou a importação

### 7. Integração com Shipment
- ✅ Usar campos do BETA-011A: invoice_number, invoice_value, freight_value, freight_percentage, collection_departure_date, customer_name, destination_uf
- ✅ Não recalcular freight_percentage se o model/service já centraliza a regra

**Arquivos:**
- `apps/api/app/modules/shipments/models.py` - Model Shipment com campos fiscais/financeiros (já existente do BETA-011A)
- `apps/api/app/modules/imports/service_v2.py` - Integração na função `confirm_import()`

## Testes Implementados (TDD)

### 1. test_import_csv_validation.py
- ✅ Testes de parsing de datas brasileiras
- ✅ Testes de parsing de valores monetários brasileiros
- ✅ Testes de normalização de nomes de colunas
- ✅ Testes de mapeamento de colunas
- ✅ Testes de validação de linhas (válidas e inválidas)
- ✅ Testes de parsing CSV com colunas mapeadas
- ✅ Testes de preview com CSV válido e inválido

**Total:** 25 testes

### 2. test_import_xlsx_validation.py
- ✅ Testes de parsing XLSX válido
- ✅ Testes de parsing XLSX vazio
- ✅ Testes de parsing XLSX com data brasileira
- ✅ Testes de parsing XLSX com valor monetário brasileiro
- ✅ Testes de parsing XLSX com nomes de colunas em português
- ✅ Testes de preview com XLSX válido e inválido

**Total:** 8 testes

### 3. test_import_preview_confirm.py
- ✅ Testes de resumo de preview
- ✅ Testes de preview com múltiplas linhas
- ✅ Testes de preview com linhas válidas e inválidas mistas
- ✅ Testes de preview com arquivo vazio
- ✅ Testes de limite de 10 itens no preview
- ✅ Testes de números de linha no preview
- ✅ Testes de dados normalizados no preview
- ✅ Testes de detalhes de erro no preview
- ✅ Testes de consistência de hash de arquivo
- ✅ Testes de formatos brasileiros no preview
- ✅ Testes de endpoint de confirmação (não implementado)
- ✅ Testes de preservação de nome de arquivo
- ✅ Testes de detecção de tipo de arquivo
- ✅ Testes de campos obrigatórios
- ✅ Testes de valores negativos/zero

**Total:** 17 testes

### 4. test_import_duplicate_detection.py
- ✅ Testes de detecção de duplicidade por tracking_code no arquivo
- ✅ Testes de detecção de duplicidade por invoice_number no arquivo
- ✅ Testes de ausência de duplicidade
- ✅ Testes de múltiplas duplicidades
- ✅ Testes de ignorar linhas inválidas na detecção
- ✅ Testes de detecção de duplicidade no banco (tracking_code)
- ✅ Testes de detecção de duplicidade no banco (invoice_number)
- ✅ Testes de ausência de duplicidade no banco
- ✅ Testes de lista vazia
- ✅ Testes de contagem de duplicidade no preview
- ✅ Testes de detecção de duplicidade no arquivo via preview
- ✅ Testes de diferentes carriers com mesmo tracking_code
- ✅ Testes de campos faltantes na detecção

**Total:** 13 testes

**Total de Testes:** 63 testes

## Estrutura de Arquivos

### Novos Arquivos
```
apps/api/
├── app/modules/imports/
│   ├── mapper.py                      # Layout mapper para colunas
│   ├── service_v2.py                  # Serviço melhorado com preview/validação
│   ├── models.py                      # Model atualizado com novos campos
│   ├── schemas.py                     # Schemas atualizados com preview/confirm
│   └── router.py                      # Router atualizado com novos endpoints
├── migrations/versions/
│   └── 20260610_01_add_import_history_metadata.py  # Migration para novos campos
└── tests/
    ├── test_import_csv_validation.py  # Testes de validação CSV
    ├── test_import_xlsx_validation.py # Testes de validação XLSX
    ├── test_import_preview_confirm.py # Testes de preview/confirm
    └── test_import_duplicate_detection.py  # Testes de detecção de duplicidade
```

### Arquivos Modificados
- `apps/api/app/modules/imports/models.py` - Adicionados campos source, metadata, imported_by
- `apps/api/app/modules/imports/schemas.py` - Adicionados schemas para preview/confirm
- `apps/api/app/modules/imports/router.py` - Adicionados endpoints preview/confirm

## Regras de Validação

### Campos Obrigatórios
1. **tracking_code**: String não vazia
2. **carrier_id**: Inteiro positivo
3. **invoice_number**: String não vazia
4. **invoice_value**: Valor monetário positivo (formato brasileiro)
5. **freight_value**: Valor monetário não negativo (formato brasileiro)
6. **collection_departure_date**: Data válida (formato brasileiro)
7. **customer_name**: String não vazia
8. **destination_uf**: String de 2 caracteres (sigla do estado)

### Formatos Suportados

#### Data
- Brasileiro: `DD/MM/YYYY`, `DD-MM-YYYY`
- ISO: `YYYY-MM-DD`
- Ano de 2 dígitos: `DD/MM/YY` (assumido como 20YY)

#### Valor Monetário
- Brasileiro com milhar: `1.234,56`
- Brasileiro sem milhar: `1234,56`
- Com prefixo R$: `R$ 1.234,56`
- Ponto decimal: `1234.56`

### Detecção de Duplicidade

#### No Arquivo
- `(tracking_code + carrier_id)` duplicado
- `(invoice_number + carrier_id)` duplicado

#### No Banco de Dados
- `tracking_code` já existe em Shipment
- `invoice_number` já existe em Shipment

## Endpoints

### POST /api/v1/imports/preview
Preview de importação sem persistir dados.

**Request:**
```
POST /api/v1/imports/preview
Content-Type: multipart/form-data

file: <arquivo CSV ou XLSX>
```

**Response:**
```json
{
  "filename": "import.csv",
  "file_type": "csv",
  "file_hash": "abc123...",
  "total_rows": 100,
  "valid_rows": 95,
  "invalid_rows": 5,
  "duplicate_rows": 2,
  "preview_items": [
    {
      "row_number": 2,
      "data": {
        "tracking_code": "BR123456789",
        "carrier_id": 1,
        "invoice_number": "NF12345",
        "invoice_value": 1234.56,
        "freight_value": 123.45,
        "collection_departure_date": "2026-06-15T00:00:00",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP"
      },
      "errors": [],
      "warnings": [],
      "is_valid": true
    }
  ],
  "errors": [
    {
      "row_number": 3,
      "field": "tracking_code",
      "message": "tracking_code obrigatorio",
      "value": "",
      "is_blocking": true
    }
  ],
  "warnings": []
}
```

### POST /api/v1/imports/confirm
Confirmação de importação (requer gerenciamento de estado - atualmente retorna 501).

**Request:**
```json
{
  "file_hash": "abc123...",
  "confirm": true
}
```

**Response:**
```json
{
  "id": 1,
  "filename": "import.csv",
  "file_type": "csv",
  "file_hash": "abc123...",
  "rows_received": 100,
  "duplicates_count": 2,
  "imported_count": 95,
  "rejected_count": 5,
  "status": "completed",
  "source": "csv_xlsx_import",
  "metadata": "{\"valid_rows\": 95, \"invalid_rows\": 5, ...}",
  "imported_by": 1,
  "created_at": "2026-06-10T10:00:00Z"
}
```

## Limitações Conhecidas

1. **Endpoint de Confirmação:** Requer gerenciamento de estado (cache/session) para armazenar o preview entre as chamadas. Atualmente retorna 501.
2. **Estado de Preview:** O preview não é persistido, então a confirmação precisa re-validar os dados ou usar cache.
3. **Performance:** Para arquivos muito grandes (>10.000 linhas), o preview pode ser lento devido à validação linha a linha.
4. **Braspress Layout:** O mapper está preparado para layout Braspress futuro, mas não está totalmente implementado.

## Próximos Passos

1. Implementar gerenciamento de estado (Redis) para endpoint de confirmação
2. Adicionar suporte para layout específico Braspress
3. Implementar processamento assíncrono para arquivos grandes
4. Adicionar mais validações de negócio (ex: validar carrier_id existe)
5. Implementar rollback de importação em caso de erro parcial

## Validações

### Validações de Código
- ✅ `python scripts/check_secrets.py --repo-root .`
- ✅ `python scripts/check_secrets.py --repo-root . --self-test`
- ✅ `python scripts/validate_migrations.py`
- ✅ `python scripts/validate_docs.py`
- ✅ `python scripts/beta_validate.py`

### Validações de Testes
- ✅ `python -m pytest tests/test_import_csv_validation.py -v`
- ✅ `python -m pytest tests/test_import_xlsx_validation.py -v`
- ✅ `python -m pytest tests/test_import_preview_confirm.py -v`
- ✅ `python -m pytest tests/test_import_duplicate_detection.py -v`
- ✅ `python -m pytest tests/test_shipment_fiscal_financial_fields.py -v`
- ✅ `python -m pytest tests/test_shipments_advanced_filters.py -v`
- ✅ `python -m pytest -v`

### Validações de Frontend
- ✅ `npm run lint` (apps/web)
- ✅ `npm run test` (apps/web)
- ✅ `npm run build` (apps/web)

## Documentação Atualizada

- ✅ `docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md` (este arquivo)
- ✅ `docs/BETA_NEXT_ACTIONS.md`
- ✅ `docs/BETA_FUNCTIONAL_EPIC_AUDIT.md`

## Referências

- BETA-011A: Campos fiscais/financeiros no model Shipment
- BETA-011C: Fixes de build/test do frontend
- LOG-007: Importador CSV/Excel
- LOG-008: Validação de colunas
- LOG-010: Persistência de importação
