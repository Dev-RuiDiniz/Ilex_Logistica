# BETA-012B: Frontend de Upload, Preview, Erros por Linha e Confirmação de Importação

## Status
**Status:** Implementado  
**Branch:** `feature/beta-012b-import-upload-preview-confirm-frontend`  
**Base Branch:** `origin/feature/beta-012a-import-csv-xlsx-backend-preview-confirm`  
**Tipo:** Frontend-only (backend já implementado no BETA-012A)

## Objetivo

Implementar frontend para upload, preview, exibição de erros por linha e confirmação de importação CSV/XLSX, integrando com os endpoints do BETA-012A.

## Escopo Implementado

### 1. Atualização de Tipos TypeScript (types.ts)

**Arquivo:** `apps/web/src/lib/types.ts`

**Novos tipos adicionados:**
- `RowValidationError`: Tipo de erro com severity e is_blocking
- `ValidatedRowData`: Dados normalizados de linha validada
- `ImportPreviewV2Response`: Resposta do endpoint de preview
- `ImportConfirmResponse`: Atualizado com duplicates_count e created_shipments

**Tipos mantidos para compatibilidade:**
- `CSVRowError`: Tipo legado para compatibilidade
- `UploadResponse`: Tipo legado para compatibilidade
- `ImportConfirmRequest`: Requisição de confirmação

### 2. Atualização do API Client (api.ts)

**Arquivo:** `apps/web/src/lib/api.ts`

**Nova função adicionada:**
```typescript
export async function previewShipmentImport(token: string, file: File): Promise<ImportPreviewV2Response>
```
- Usa POST `/api/v1/imports/preview`
- Envia arquivo como multipart/form-data
- Retorna ImportPreviewV2Response com resumo, preview_items, errors, warnings

**Função atualizada:**
```typescript
export async function confirmShipmentsImport(token: string, importId: number): Promise<ImportConfirmResponse>
```
- Atualizado para usar POST `/api/v1/imports/confirm` (antigo: `/shipments/import`)
- Payload: `{ import_id: importId, confirm: true }`
- Retorna ImportConfirmResponse com created_shipments

**Funções mantidas para compatibilidade:**
- `uploadShipmentsCsv`: Mantido para compatibilidade com código legado
- Outras funções existentes sem alterações

### 3. Extração de Helpers de Formatação (shipment-utils.ts)

**Arquivo:** `apps/web/src/lib/shipment-utils.ts`

**Novas funções exportadas:**
```typescript
export function formatCurrencyBRL(value: number | null): string
export function formatPercentage(value: number | null): string
export function formatDateBR(dateString: string | null): string
export function formatUnavailable(value: string | number | null): string
```

**Benefícios:**
- Reutilização entre componentes
- Consistência de formatação
- Centralização de lógica de formatação brasileira

### 4. Atualização da Tela de Importação (page.tsx)

**Arquivo:** `apps/web/src/app/(private)/shipments/import/page.tsx`

**Estados implementados:**
- `idle`: Estado inicial, aguardando seleção de arquivo
- `file_selected`: Arquivo selecionado, aguardando validação
- `preview_loading`: Carregando preview
- `preview_success`: Preview concluído com sucesso
- `preview_with_errors`: Preview concluído com erros bloqueantes
- `confirm_loading`: Processando confirmação
- `confirm_success`: Importação concluída com sucesso
- `confirm_error`: Importação falhou
- `api_error`: Erro na API

**Funcionalidades implementadas:**

#### Upload de Arquivo
- Aceita CSV e XLSX
- Validação por MIME type e extensão
- Exibição de nome do arquivo selecionado
- Mensagem de erro para extensões inválidas

#### Preview
- Chama endpoint `/api/v1/imports/preview`
- Exibe resumo: total_rows, valid_rows, invalid_rows, duplicate_rows
- Exibe tabela de preview com primeiras linhas
- Campos fiscais/financeiros: NF, cliente, UF, data coleta, valor NF, valor frete
- Usa helpers de formatação: formatCurrencyBRL, formatDateBR, formatUnavailable

#### Erros por Linha
- Exibe tabela com: linha, campo, mensagem, valor, severidade
- Badge de severidade (erro/aviso)
- Diferenciação visual entre erros e avisos

#### Warnings Separados
- Seção separada para warnings
- Tabela com: linha, campo, mensagem, valor
- Não bloqueia confirmação

#### Bloqueio de Confirmação
- Verifica `is_blocking` nos erros
- Desabilita botão confirmar quando há erro bloqueante
- Mensagem explicativa quando bloqueado
- Habilita botão quando todas as linhas são válidas

#### Confirmação
- Chama endpoint `/api/v1/imports/confirm` com import_id
- Impede duplo clique (loading state)
- Exibe resultado final: status, imported_count, rejected_count, duplicate_count
- Exibe lista de IDs de shipments criados (created_shipments)

#### Reset
- Permite cancelar e voltar ao estado inicial
- Limpa todos os estados e dados

### 5. Testes TDD (page.test.tsx)

**Arquivo:** `apps/web/src/app/(private)/shipments/import/page.test.tsx`

**Cenários testados:**

#### Upload de Arquivo
- ✅ Deve aceitar upload CSV
- ✅ Deve aceitar upload XLSX
- ✅ Deve rejeitar extensão inválida
- ✅ Deve exibir nome do arquivo selecionado

#### Preview
- ✅ Deve chamar endpoint de preview ao validar
- ✅ Deve exibir resumo da prévia
- ✅ Deve exibir tabela de preview
- ✅ Deve exibir erros por linha
- ✅ Deve exibir warnings separadamente
- ✅ Deve bloquear botão confirmar quando houver erro bloqueante
- ✅ Deve habilitar botão confirmar quando todas as linhas forem válidas
- ✅ Deve exibir erro quando preview falhar

#### Confirmação
- ✅ Deve chamar endpoint de confirmação com import_id
- ✅ Deve exibir resultado de importação concluída
- ✅ Deve impedir duplo clique na confirmação
- ✅ Deve exibir erro quando confirmação falhar

#### Reset
- ✅ Deve permitir cancelar e voltar ao estado inicial

**Total:** 15 testes

### 6. Testes API (api.test.ts)

**Arquivo:** `apps/web/src/lib/api.test.ts`

**Novos testes adicionados:**
- ✅ previewShipmentImport está exportado (BETA-012B)
- ✅ previewShipmentImport recebe token e file (BETA-012B)

**Total:** 2 testes adicionados

## Integração com Backend BETA-012A

### Preview Endpoint
```
POST /api/v1/imports/preview
Content-Type: multipart/form-data

Request:
- file: File (CSV ou XLSX)

Response: ImportPreviewV2Response
{
  import_id: number
  filename: string
  file_type: string
  file_hash: string
  total_rows: number
  valid_rows: number
  invalid_rows: number
  duplicate_rows: number
  preview_items: ValidatedRowData[]
  errors: RowValidationError[]
  warnings: RowValidationError[]
}
```

### Confirm Endpoint
```
POST /api/v1/imports/confirm
Content-Type: application/json

Request:
{
  import_id: number
  confirm: boolean
}

Response: ImportConfirmResponse
{
  import_id: number
  status: "completed" | "failed"
  total_rows: number
  valid_rows: number
  invalid_rows: number
  imported_count: number
  rejected_count: number
  duplicates_count: number
  created_shipments: number[]
  errors: CSVRowError[]
}
```

## Campos Fiscais/Financeiros Exibidos

### Preview Table
- **Linha**: Número da linha no arquivo
- **NF**: invoice_number
- **Cliente**: customer_name
- **UF**: destination_uf
- **Data Coleta**: collection_departure_date (formatado DD/MM/YYYY)
- **Valor NF**: invoice_value (formatado R$ 1.234,56)
- **Valor Frete**: freight_value (formatado R$ 1.234,56)

## Validações de Arquivo

### Extensões Aceitas
- `.csv` (text/csv, application/vnd.ms-excel)
- `.xlsx` (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel.sheet.macroEnabled.12)

### Validação
- MIME type e extensão
- Mensagem de erro para extensões inválidas
- Permissão de edição (canEditShipments)

## Estados de Importação

### Fluxo Normal
1. `idle` → Selecionar arquivo → `file_selected`
2. `file_selected` → Validar → `preview_loading`
3. `preview_loading` → Sucesso → `preview_success`
4. `preview_success` → Confirmar → `confirm_loading`
5. `confirm_loading` → Sucesso → `confirm_success`

### Fluxo com Erros
1. `idle` → Selecionar arquivo → `file_selected`
2. `file_selected` → Validar → `preview_loading`
3. `preview_loading` → Erros bloqueantes → `preview_with_errors`
4. `preview_with_errors` → Corrigir arquivo → `idle`

### Fluxo de Erro de API
1. `preview_loading` → Erro de API → `api_error`
2. `api_error` → Tentar novamente → `idle`
3. `confirm_loading` → Erro de API → `confirm_error`
4. `confirm_error` → Tentar novamente → `idle`

## Compatibilidade

### Backward Compatibility
- Tipos legados mantidos (CSVRowError, UploadResponse)
- Função legado mantida (uploadShipmentsCsv)
- Endpoint legado não removido (mas não usado no novo fluxo)

### Forward Compatibility
- Novos tipos preparados para expansão
- Novos endpoints seguem padrão REST
- Estados preparados para novos cenários

## Regras Implementadas

### Regras de Negócio
- ✅ Bloquear confirmação quando há erro bloqueante (is_blocking=true)
- ✅ Permitir confirmação quando há warnings não bloqueantes
- ✅ Exibir warnings separados de erros
- ✅ Impedir duplo clique na confirmação
- ✅ Exibir resultado final com contadores e IDs criados

### Regras de UI/UX
- ✅ Estados claros de loading
- ✅ Mensagens de erro descritivas
- ✅ Tabelas com scroll para muitos itens
- ✅ Badges visuais para severidade
- ✅ Botões desabilitados adequadamente
- ✅ Reset para nova importação

### Regras de Formatação
- ✅ Moeda brasileira (R$ 1.234,56)
- ✅ Data brasileira (DD/MM/YYYY)
- ✅ Percentual (12,34%)
- ✅ Valores indisponíveis (-)

## Testes

### Cobertura
- page.test.tsx: 15 testes
- api.test.ts: 2 testes adicionais
- Total: 17 testes

### Execução
```bash
cd apps/web
npm test
```

## Validações Pós-Implementação

### Lint
```bash
cd apps/web
npm run lint
```

### Test
```bash
cd apps/web
npm test
```

### Build
```bash
cd apps/web
npm run build
```

### Secrets Check
```bash
python scripts/check_secrets.py --repo-root .
```

### Docs Validation
```bash
python scripts/validate_docs.py
```

## Documentação Atualizada

### Criada
- ✅ docs/BETA_012B_IMPORT_UPLOAD_PREVIEW_CONFIRM_FRONTEND.md

### Atualizada
- docs/BETA_NEXT_ACTIONS.md (pendente)
- docs/BETA_FUNCTIONAL_EPIC_AUDIT.md (pendente)
- docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md (se necessário)

## Próximos Passos

### Não Implementado (Fora do Escopo)
- SLA de importação
- Eficiência por transportadora
- Alertas/relatório diário
- Layout Braspress completo

### Futuras Melhorias
- Progresso em tempo real da importação
- Download de template de importação
- Histórico de importações na UI
- Filtros avançados na tabela de preview
- Exportação de erros para CSV

## Conclusão

BETA-012B implementou com sucesso o frontend de upload, preview, erros por linha e confirmação de importação, integrando perfeitamente com o backend BETA-012A. A implementação segue princípios TDD, mantém compatibilidade com código legado, e proporciona uma experiência de usuário clara e robusta para importação de dados fiscais/financeiros de shipments.
