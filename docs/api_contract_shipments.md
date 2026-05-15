# API Contract - Shipments Module

## Overview
Este documento descreve o contrato da API para o módulo de Shipments (Envios) da Sprint 2 Trilha A.

## Base URL
```
/api/v1/shipments
```

## Authentication
Todos os endpoints requerem autenticação via JWT Bearer token no header `Authorization`.

---

## POST /api/v1/shipments/upload

### Descrição
Faz upload de um arquivo CSV para validação prévia. O arquivo é validado mas os dados não são persistidos no banco.

### Request

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Body (multipart/form-data):**
- `file`: Arquivo CSV (obrigatório)

**CSV Columns Required:**
- `tracking_code` (string, obrigatório): Código de rastreamento
- `carrier_name` (string, obrigatório): Nome da transportadora
- `estimated_delivery` (datetime, obrigatório): Data estimada de entrega (ISO 8601)
- `recipient_name` (string, obrigatório): Nome do destinatário
- `recipient_phone` (string, obrigatório): Telefone do destinatário
- `origin_address` (string, obrigatório): Endereço de origem
- `destination_address` (string, obrigatório): Endereço de destino

**CSV Columns Optional:**
- `invoice_number` (string, opcional): Número da nota fiscal
- `invoice_key` (string, opcional): Chave da nota fiscal
- `fiscal_document` (string, opcional): Documento fiscal
- `amount` (decimal, opcional): Valor monetário
- `due_date` (datetime, opcional): Data de vencimento (ISO 8601)

### Response

**Status Code:** 201 Created

**Body:**
```json
{
  "import_id": 1,
  "status": "validated",
  "total_rows": 10,
  "valid_rows": 8,
  "invalid_rows": 2,
  "errors": [
    {
      "row_number": 3,
      "field": "carrier_name",
      "message": "transportadora nao encontrada",
      "value": "Transportadora Inexistente"
    }
  ]
}
```

**Status Values:**
- `validated`: Arquivo validado com sucesso
- `failed`: Erro ao processar arquivo

**Error Codes:**
- `400`: Arquivo não é CSV ou erro ao ler arquivo
- `401`: Token de autenticação inválido ou ausente

---

## POST /api/v1/shipments/import

### Descrição
Confirma e processa a importação de um arquivo CSV previamente validado. Persiste os dados válidos no banco de dados.

### Request

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Body:**
```json
{
  "import_id": 1,
  "confirm": true
}
```

### Response

**Status Code:** 200 OK

**Body:**
```json
{
  "import_id": 1,
  "status": "completed",
  "total_rows": 10,
  "valid_rows": 8,
  "invalid_rows": 2,
  "imported_count": 6,
  "rejected_count": 2,
  "errors": [
    {
      "row_number": 3,
      "field": "tracking_code",
      "message": "tracking_code ja existe no banco",
      "value": "TRK001"
    }
  ]
}
```

**Status Values:**
- `completed`: Importação concluída com sucesso
- `failed`: Erro ao processar importação

**Rejeições:**
- Duplicidade de `tracking_code` no banco de dados
- Duplicidade de `tracking_code` no arquivo CSV
- Transportadora não encontrada

**Error Codes:**
- `400`: `confirm` não é true, import_id não existe, importação já processada, ou erro ao processar
- `401`: Token de autenticação inválido ou ausente

---

## GET /api/v1/shipments

### Descrição
Lista shipments com paginação, ordenação e filtros.

### Request

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `page` (integer, default=1, min=1): Número da página
- `page_size` (integer, default=20, min=1, max=100): Itens por página
- `status` (string, opcional): Filtra por status (ex: pending, delivered)
- `carrier_id` (integer, opcional): Filtra por ID da transportadora
- `tracking_code` (string, opcional): Filtra por código de rastreamento (busca parcial, case-insensitive)
- `invoice_number` (string, opcional): Filtra por número da nota fiscal (busca parcial, case-insensitive)
- `fiscal_document` (string, opcional): Filtra por documento fiscal (busca parcial, case-insensitive)
- `criticality` (string, opcional): Filtra por criticidade (normal, baixa, media, alta)
- `estimated_delivery_from` (string, opcional): Data estimada de entrega inicial (ISO 8601)
- `estimated_delivery_to` (string, opcional): Data estimada de entrega final (ISO 8601)
- `due_date_from` (string, opcional): Data de vencimento inicial (ISO 8601)
- `due_date_to` (string, opcional): Data de vencimento final (ISO 8601)
- `sort_by` (string, default=created_at): Campo para ordenação
- `sort_order` (string, default=desc): Ordem de ordenação (asc ou desc)

### Response

**Status Code:** 200 OK

**Body:**
```json
{
  "items": [
    {
      "id": 1,
      "tracking_code": "TRK001",
      "carrier_id": 1,
      "status": "pending",
      "estimated_delivery": "2026-06-01T00:00:00",
      "recipient_name": "João Silva",
      "recipient_phone": "11999999999",
      "origin_address": "Rua A SP",
      "destination_address": "Rua B RJ",
      "invoice_number": "NF001",
      "invoice_key": "KEY123",
      "fiscal_document": "CNPJ123",
      "amount": 100.50,
      "due_date": "2026-07-01T00:00:00",
      "delay_days": 0,
      "criticality": "normal",
      "created_at": "2026-05-15T00:00:00",
      "updated_at": "2026-05-15T00:00:00"
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 20
}
```

**Error Codes:**
- `401`: Token de autenticação inválido ou ausente

---

## Campos Fiscais/Financeiros

Os campos fiscais/financeiros são opcionais e podem ser incluídos no CSV:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `invoice_number` | string | Número da nota fiscal (max 50 caracteres) |
| `invoice_key` | string | Chave da nota fiscal (max 100 caracteres) |
| `fiscal_document` | string | Documento fiscal (CNPJ/CPF, max 50 caracteres) |
| `amount` | decimal | Valor monetário (precisão 10, escala 2) |
| `due_date` | datetime | Data de vencimento (ISO 8601) |

## Motor de Atraso/Criticidade

O sistema calcula automaticamente `delay_days` e `criticality` com base em `due_date`:

**Cálculo de delay_days:**
- `delay_days = max(0, data_atual - due_date)` em dias
- Se `due_date` não informado, `delay_days = 0`

**Classificação de criticality:**
| delay_days | criticality |
|------------|-------------|
| 0 | normal |
| 1-7 | baixa |
| 8-30 | media |
| >30 | alta |

## Validações

**Upload CSV:**
- Arquivo deve ser CSV
- Colunas obrigatórias devem estar presentes
- Campos obrigatórios não podem estar vazios
- `estimated_delivery` deve estar em formato ISO 8601
- Transportadora deve existir no banco de dados
- `amount` deve ser um valor numérico válido (se informado)
- `due_date` deve estar em formato ISO 8601 (se informado)

**Importação:**
- `import_id` deve existir
- Importação deve estar em status `validated`
- `confirm` deve ser `true`
- `tracking_code` não pode existir no banco de dados
- `tracking_code` não pode ser duplicado no arquivo CSV

## Compatibilidade

O sistema mantém compatibilidade com uploads antigos:
- Campos fiscais/financeiros são opcionais no CSV
- Uploads sem esses campos funcionam normalmente
- `delay_days` e `criticality` são calculados com valores padrão (0 e "normal")
