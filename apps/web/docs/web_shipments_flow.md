# Fluxo Web - Importação e Listagem de Shipments

## Sprint 2 Trilha B - Frontend Admin

## Visão Geral

Este documento descreve o fluxo completo de importação e listagem de envios (shipments) no painel administrativo da Ilex Logística.

## Rotas

- `/shipments` - Listagem de envios com filtros, busca e ordenação
- `/shipments/import` - Importação de envios via CSV

## Fluxo de Importação de Shipments

### 1. Upload CSV

**Rota:** `/shipments/import`

**Estados:** `idle` → `uploading` → `validated` → `importing` → `completed` / `failed`

**Funcionalidades:**
- Seleção de arquivo CSV (validação por MIME type e extensão .csv)
- Exibição do nome do arquivo selecionado
- Botão "Fazer Upload" para iniciar processamento
- Loading spinner durante upload
- Mensagens de erro específicas

**Validação de arquivo:**
- MIME types aceitos: `text/csv`, `application/vnd.ms-excel`
- Extensão: `.csv` (case insensitive)
- Se inválido: exibe mensagem de erro

**API:**
- `POST /api/v1/shipments/upload`
- `Content-Type: multipart/form-data`
- Campo: `file`

**Resposta (UploadResponse):**
```typescript
{
  import_id: number | null,
  status: "validated" | "failed",
  total_rows: number,
  valid_rows: number,
  invalid_rows: number,
  errors: CSVRowError[]
}
```

### 2. Validação e Exibição de Erros

**Estado:** `validated` ou `failed`

**Resumo de Validação:**
- Total de linhas processadas
- Linhas válidas (verde)
- Linhas inválidas (vermelho)

**Tabela de Erros por Linha:**
- Colunas: Linha, Campo, Mensagem, Valor
- Scroll vertical (max-height: 256px)
- Header sticky
- Exibida apenas quando há erros

**Estrutura de erro (CSVRowError):**
```typescript
{
  row_number: number,
  field: string,
  message: string,
  value?: string
}
```

**Mensagens de erro:**
- Se validação falhou: "Validação falhou. Verifique os erros abaixo."
- Se falha na validação: "Falha na validação do arquivo CSV."
- Se falha no upload: "Falha ao fazer upload do arquivo CSV." (com Error.message)

### 3. Confirmação de Importação

**Estado:** `validated` → `importing` → `completed` / `failed`

**Condições:**
- `status === "validated"`
- `valid_rows > 0`
- Usuário com permissão `canEditShipments` (admin, logistica, gestor)

**Botão "Confirmar Importação":**
- Desabilitado se usuário sem permissão
- Desabilitado durante processamento
- Inicia estado `importing`

**API:**
- `POST /api/v1/shipments/import`
- `Content-Type: application/json`
- Body: `{ import_id: number, confirm: true }`

**Resposta (ImportConfirmResponse):**
```typescript
{
  import_id: number,
  status: "completed" | "failed",
  total_rows: number,
  valid_rows: number,
  invalid_rows: number,
  imported_count: number,
  rejected_count: number,
  errors: CSVRowError[]
}
```

### 4. Tela de Conclusão

**Estado:** `completed`

**Resumo de Importação:**
- Total de linhas
- Importados (verde)
- Rejeitados (vermelho)

**Botões:**
- "Nova Importação" - Reseta para estado `idle`

**Mensagens de erro:**
- Se importação falhou: "Importação falhou. Verifique os erros abaixo."
- Se falha na confirmação: "Falha ao confirmar importação."

## Fluxo de Listagem de Shipments

### 1. Listagem Básica

**Rota:** `/shipments`

**Tabela de Envios:**
- Colunas: Tracking, Carrier ID, Status, Entrega Estimada, Nota Fiscal, Doc. Fiscal, Valor, Vencimento, Atraso (dias), Criticidade
- Paginação: 20 itens por página
- Loading state
- Empty state quando sem resultados
- Error state com mensagem

**Formatação:**
- Moeda: `Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" })`
- Data: `toLocaleDateString("pt-BR")`
- Valores nulos: "-"

**Badges de Criticidade:**
- Normal: bg-green-100 text-green-800
- Baixa: bg-yellow-100 text-yellow-800
- Média: bg-orange-100 text-orange-800
- Alta: bg-red-100 text-red-800

**API:**
- `GET /api/v1/shipments`
- Query params: page, page_size, status, carrier_id, tracking_code, invoice_number, fiscal_document, criticality, estimated_delivery_from, estimated_delivery_to, due_date_from, due_date_to, sort_by, sort_order

**Resposta (ShipmentListResponse):**
```typescript
{
  items: Shipment[],
  total: number,
  page: number,
  page_size: number,
  total_pages: number
}
```

### 2. Busca Global

**Seletor de Tipo de Busca:**
- Automático (heurística) - padrão
- Código de rastreio
- Nota fiscal

**Heurística Automática:**
- Se valor é numérico → busca por `invoice_number`
- Senão → busca por `tracking_code`

**Função utilitária:** `buildSearchParams(searchType, searchQuery)`

**Comportamento:**
- Não aplica ambos `tracking_code` e `invoice_number` simultaneamente
- Placeholder dinâmico baseado no tipo selecionado

### 3. Filtros Avançados

**Filtros Disponíveis:**
- Status: pending, in_transit, delivered, failed
- Carrier ID: input numérico
- Criticality: normal, baixa, media, alta
- Entrega estimada: de/até (date picker)
- Vencimento: de/até (date picker)

**Filtro Temporal por Mês/Ano:**
- Checkbox para ativar/desativar
- Seletor de target: Entrega estimada ou Vencimento
- Select de mês (Janeiro a Dezembro)
- Select de ano (2024 a 2028)
- Usa função `monthYearToDateRange(month, year)` para conversão
- Converte para `estimated_delivery_from/to` ou `due_date_from/to`
- Desabilita filtros manuais de data quando ativo

**Função utilitária:** `monthYearToDateRange(month, year)`
- Retorna `{ from: string, to: string }` em formato ISO (YYYY-MM-DD)
- Calcula primeiro e último dia do mês
- Lida com ano bissexto

### 4. Ordenação

**Campos Ordenáveis:**
- created_at - Data de criação
- estimated_delivery - Entrega estimada
- due_date - Vencimento
- amount - Valor
- criticality - Criticidade

**Ordem:**
- asc (Ascendente) / desc (Descendente)
- Botão toggle para alternar
- Reload automático ao mudar ordenação

**Padrão:** created_at desc

### 5. Controles de Ação

**Botões:**
- "Buscar" - Executa busca com parâmetros atuais
- "Aplicar Filtros" - Aplica filtros e reseta página para 1
- "Limpar Filtros" - Reseta todos os filtros e ordenação
- "Anterior" / "Próxima" - Paginação

**Disabled States:**
- Todos os botões desabilitados durante `loading`
- Paginação desabilitada na primeira/última página

## RBAC (Controle de Acesso)

### Permissões

**canEditShipments(role):**
- admin: true
- logistica: true
- gestor: true
- auditoria: false

**canViewShipments(role):**
- admin: true
- logistica: true
- gestor: true
- auditoria: true

### Comportamento

**Importação (/shipments/import):**
- Usuários sem permissão: exibe "Perfil com permissão somente leitura"
- Input de arquivo desabilitado
- Botões de ação desabilitados

**Listagem (/shipments):**
- Usuários sem permissão: exibe "Perfil sem permissão para visualizar envios"
- Tabela não carrega dados

## Limitações Conhecidas

### 1. Nome da Transportadora
- A API retorna apenas `carrier_id` (ID numérico)
- Não há endpoint para buscar nome da transportadora
- Tabela exibe o ID numérico

### 2. Filtros de Cliente/UF
- A API não suporta filtros de cliente ou UF
- Não implementados na UI
- Limitação documentada em banner na página

### 3. Anos Disponíveis
- Filtro temporal por mês/ano limitado a anos 2024-2028
- Configurável na UI

### 4. Rota de Detalhe
- Não implementada (fora do escopo S2-B)
- Botão "Ver Envios" removido após conclusão da importação

### 5. Ações de CRUD
- Dethe, update, delete não implementados (fora do escopo)
- Eventos e audit trail não implementados (fora do escopo)

## Erros e Tratamento

### Erros de API
- Captura de `Error.message` em todos os catch blocks
- Mensagens contextuais por operação (upload, import, listagem)
- Exibição em alertas vermelhos

### Erros de Validação
- Exibidos em tabela detalhada
- Informam linha, campo, mensagem e valor
- Usuário pode corrigir CSV e reenviar

### Erros de Rede
- Mensagem genérica: "Falha na API"
- Estado `failed` com opção de tentar novamente

## Estados de Loading

**Importação:**
- `uploading` - Spinner "Fazendo upload do arquivo..."
- `importing` - Spinner "Processando importação..."

**Listagem:**
- `loading` - Texto "Carregando..." na tabela

## Responsividade

**Layout:**
- Desktop: Grid de 3 colunas para filtros
- Mobile: Grid de 1 coluna para filtros
- Header flexível para busca (col/row)

## Arquivos Relacionados

**Frontend:**
- `src/app/(private)/shipments/page.tsx` - Listagem
- `src/app/(private)/shipments/import/page.tsx` - Importação
- `src/lib/api.ts` - Client HTTP (listShipments, uploadShipmentsCsv, confirmShipmentsImport)
- `src/lib/types.ts` - Tipos TypeScript
- `src/lib/permissions.ts` - RBAC
- `src/lib/shipment-utils.ts` - Utilitários (monthYearToDateRange, buildSearchParams)
- `src/components/app-shell.tsx` - Layout e navegação

**Backend (API):**
- `POST /api/v1/shipments/upload` - Upload CSV
- `POST /api/v1/shipments/import` - Confirmar importação
- `GET /api/v1/shipments` - Listagem
