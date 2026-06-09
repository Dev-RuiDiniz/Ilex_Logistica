# BETA-014B — Painel Frontend de Eficiência por Transportadora

## Escopo

Implementação do frontend do Épico 4 — Eficiência por transportadora — consumindo o backend criado no BETA-014A. Este PR exibe KPIs por transportadora, rankings, filtros visuais e estados de loading/erro/vazio/sucesso.

## Base Técnica

- **Branch:** feature/beta-014b-carrier-efficiency-frontend
- **Base:** origin/feature/beta-014a-carrier-efficiency-backend
- **Tipo:** Frontend-only
- ⚠️ Ajuste mínimo em SlaBadge.tsx para compatibilidade de build

## Contrato de API Verificado

### Endpoint

**Método:** GET
**URL:** /api/v1/shipments/analytics/carrier-efficiency

### Query Params Aceitos

- estimated_delivery_from: string | None (ISO 8601)
- estimated_delivery_to: string | None (ISO 8601)
- month: int | None
- year: int | None
- customer_name: string | None
- destination_uf: string | None
- carrier_id: int | None
- status: string | None
- criticality: string | None
- sla_status: string | None
- is_late: boolean | None

### Formato de Resposta

```typescript
{
  carriers: [
    {
      carrier_id: number;
      carrier_name: string | null;
      total_invoices: number;
      total_shipments: number;
      on_time_count: number;
      on_time_percentage: number;
      late_count: number;
      late_percentage: number;
      critical_count: number;
      lost_count: number;
      lost_percentage: number;
      total_freight_value: number;
      total_invoice_value: number;
      average_freight_percentage: number;
      average_freight_value: number;
      ranking_by_efficiency: number;
      ranking_by_cost: number;
      ranking_by_volume: number;
    }
  ];
  generated_at: string; // ISO 8601
}
```

## Componentes Criados

### 1. Tipos TypeScript

**Arquivo:** apps/web/src/lib/types.ts

- `CarrierEfficiencyMetrics`: Métricas por transportadora
- `CarrierEfficiencyResponse`: Resposta da API
- `CarrierEfficiencyFilters`: Filtros de consulta

### 2. API Client

**Arquivo:** apps/web/src/lib/api.ts

- `getCarrierEfficiency(token, filters)`: Função para buscar dados de eficiência
- Tratamento de erros de API
- Construção de query params
- Omissão de filtros vazios

### 3. Página de Eficiência

**Arquivo:** apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/page.tsx

- Estado de loading
- Estado de erro
- Estado vazio
- Tabela de transportadoras
- Exibição de métricas:
  - Transportadora
  - Total de NFs
  - Total de entregas
  - No prazo (percentual)
  - Atrasadas (percentual)
  - Frete total (BRL)
  - Frete médio (percentual)
  - Ranking por eficiência
  - Ranking por custo
  - Ranking por volume

### 4. Testes

**Arquivo:** apps/web/src/lib/carrier-efficiency-api.test.ts

- 6 testes para API client
- Testes de endpoint, filtros, resposta, erro, omissão de filtros vazios, serialização boolean

**Arquivo:** apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page.test.tsx

- 5 testes para página
- Testes de loading, vazio, erro e tabela

**Arquivo:** apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page-filters.test.tsx

- 8 testes para interação de filtros
- Testes de interação de filtros

### 5. Testes de Interação de Filtros

**Arquivo:** apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page-filters.test.tsx

- Deve chamar a API inicial sem filtros vazios
- Deve alterar filtro de mês e refazer a consulta
- Deve alterar filtro de UF e refazer a consulta
- Deve alterar filtro de transportadora e refazer a consulta
- Deve alterar filtro de criticality e refazer a consulta
- Deve alterar filtro de sla_status e refazer a consulta
- Deve alterar filtro de is_late e refazer a consulta
- Deve limpar filtros e refazer a consulta sem query params

## Métricas Exibidas

- **Transportadora:** Nome da transportadora (ou "-" se null)
- **Total de NFs:** Número total de notas fiscais
- **Total de entregas:** Número total de shipments
- **No prazo:** Percentual de entregas no prazo
- **Atrasadas:** Percentual de entregas atrasadas
- **Frete total:** Valor total do frete em BRL
- **Frete médio:** Percentual médio do frete
- **Ranking por eficiência:** Posição no ranking de eficiência (1 = melhor)
- **Ranking por custo:** Posição no ranking de custo (1 = melhor)
- **Ranking por volume:** Posição no ranking de volume (1 = melhor)

## Rankings

Rankings já calculados pelo backend, não recalcular no frontend:

- **Eficiência:** Maior on_time_percentage primeiro, empate por maior volume
- **Custo:** Menor average_freight_percentage primeiro
- **Volume:** Maior total_shipments primeiro

## Filtros Visuais

Filtros implementados na UI:

- Mês (número)
- Ano (número)
- Cliente (texto)
- UF (texto, max 2 caracteres)
- Transportadora ID (número)
- Status (texto)
- Criticidade (select: normal, baixa, média, alta)
- Status SLA (select: on_time, warning, late, critical, unknown)
- Atrasada (select: todas, sim, não)

Funcionalidades:
- Filtros alteram a consulta ao endpoint
- Filtros funcionam isolados e combinados
- Botão "Limpar Filtros" reseta o estado e refaz a consulta
- Filtros vazios são omitidos da query string
- Estado vazio exibido quando filtros não retornam dados

## Estados de UX

- **Loading:** Exibe "Carregando..."
- **Erro:** Exibe mensagem de erro
- **Vazio:** Exibe "Sem dados"
- **Sucesso:** Exibe tabela com dados

## Formatação

- BRL para frete (R$ 1000.00)
- Percentual com duas casas (80%)
- Números inteiros para contadores (10)
- "-" para dado indisponível (carrier_name null)

## Limitações

- Sem componentes de UI avançados (cards, gráficos)
- Sem integração com dashboard geral
- Sem E2E (Playwright não configurado)

## TDD

- **Red:** Testes criados antes da implementação
- **Green:** Implementação feita para passar nos testes
- **Refactor:** Código simplificado e testes ajustados

## Próximos Passos

- BETA-015: Alertas e notificações
- BETA-016: Relatório diário (dependendo da decisão posterior)

## Confirmação de Frontend-Only

- ✅ Nenhum código backend novo
- ✅ Nenhum endpoint novo
- ✅ Nenhum service novo
- ✅ Foco exclusivo em UI/frontend
- ⚠️ Ajuste mínimo em SlaBadge.tsx para compatibilidade de build

## Confirmação de Governança

- ✅ Sem merge em main
- ✅ Sem auto-merge
- ✅ Sem force push
- ✅ Sem comando destrutivo
- ✅ Sem credenciais reais
- ✅ Sem artefatos gerados
- ✅ Sem dados reais de cliente
