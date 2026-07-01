# ROADMAP BETA — Funcionalidades Pendentes

**Versão:** 1.0  
**Data:** 2026-06-23  
**Status:** Roadmap com SDD (Specification-Driven Development) e TDD (Test-Driven Development)  
**Base:** AUDITORIA.md (Estado Real do Projeto)

---

## Legenda

- 📋 **SDD** - Especificação detalhada disponível
- 🧪 **TDD** - Critérios de teste definidos
- ⏳ **Em Progresso** - Funcionalidade parcialmente implementada
- ❌ **Pendente** - Funcionalidade não iniciada

---

## Metodologia SDD + TDD

### SDD (Specification-Driven Development)
Antes de implementar qualquer funcionalidade:
1. **Definir especificação clara** - Entradas, saídas, comportamentos esperados
2. **Documentar regras de negócio** - Casos de uso, edge cases, validações
3. **Definir critérios de aceite** - O que caracteriza a funcionalidade como completa
4. **Criar/Atualizar documentação** - BETA_*.md com detalhes técnicos

### TDD (Test-Driven Development)
Para toda funcionalidade:
1. **Escrever teste que falha (RED)** - Teste unitário ou de integração
2. **Implementar código mínimo (GREEN)** - Apenas o suficiente para passar
3. **Refatorar se necessário (REFACTOR)** - Melhorar qualidade sem mudar comportamento
4. **Backend:** pytest com fixtures apropriados
5. **Frontend:** Vitest + @testing-library/react
6. **E2E:** Playwright para fluxos críticos

---

## Resumo por Épico (Pendências)

| Épico | Status Atual | % Completo | Tarefas Pendentes | Prioridade | Progresso |
|-------|--------------|------------|-------------------|------------|-----------|
| 1 - SLA, atraso e criticidade | Parcial | 80% | 1 tarefa | Alta | [x] 2/3 |
| 3 - Campos fiscais/financeiros | Parcial | 93% | 5 tarefas | Alta | [ ] 0/5 |
| 4 - Eficiência por transportadora | Parcial | 50% | 4 tarefas | Alta | [ ] 0/4 |
| 6 - Relatório diário automático | Parcial | 50% | 4 tarefas | Alta | [ ] 0/4 |
| 8 - Integrações assistidas | Parcial | 44% | 5 tarefas | Média | [ ] 0/5 |
| Tratativas Operacionais | ❌ Pendente | 0% | 4 tarefas | Média | [ ] 0/4 |

**Total:** 23 tarefas pendentes

---

## Épico 1 — SLA, Atraso e Criticidade (30% Pendente)

**Status Atual:** 70% completo  
**Objetivo:** Completar filtros por criticidade, tela de gestão de regras SLA e testes frontend  
**Progresso:** [x] 2/3 tarefas concluídas

### [x] Tarefa 1.1: Filtros por Criticidade no Backend

#### Especificação SDD

**Backend**
- **Endpoint:** GET /shipments com parâmetros de filtro
- **Parâmetros de filtro:**
  - `sla_status`: enum ['critical', 'warning', 'normal', 'unknown']
  - `is_late`: boolean
- **Query SQLAlchemy:** Filtrar por `sla_status` e `is_late` no modelo Shipment
- **Validação:** Valores inválidos devem retornar 422
- **Paginação:** Manter paginação existente (page, page_size)
- **Ordenação:** Manter ordenação existente (default: created_at desc)

**Critérios de Aceite**
- Endpoint aceita filtros `sla_status` e `is_late` individualmente
- Endpoint aceita filtros combinados (sla_status + is_late)
- Valores inválidos retornam erro 422 com mensagem clara
- Filtros funcionam com paginação existente
- Performance: query com filtros deve executar em <500ms para 1000 registros

#### Critérios TDD

**Backend Tests**
- Teste de filtro por `sla_status` (critical)
- Teste de filtro por `sla_status` (warning)
- Teste de filtro por `sla_status` (normal)
- Teste de filtro por `sla_status` (unknown)
- Teste de filtro por `is_late` (true)
- Teste de filtro por `is_late` (false)
- Teste de filtro combinado (sla_status + is_late)
- Teste de valor inválido em `sla_status` (422)
- Teste de filtro sem resultados (empty list)
- Teste de performance com 1000 registros

**Frontend Tests**
- Teste de renderização de dropdown de filtro sla_status
- Teste de seleção de filtro sla_status
- Teste de seleção de filtro is_late
- Teste de filtro combinado
- Teste de limpeza de filtros

---

### [x] Tarefa 1.2: Filtros por Criticidade no Frontend

#### Especificação SDD

**Frontend**
- **Componente:** Sidebar de filtros em shipments/page.tsx
- **Dropdown sla_status:** Select com opções (Todos, Crítico, Warning, Normal, Desconhecido)
- **Toggle is_late:** Checkbox ou toggle switch
- **Estado:** React state para filtros (sla_status, is_late)
- **API:** Chamada GET /shipments com parâmetros de filtro
- **URL:** Query params na URL para compartilhamento de filtros
- **Badges:** Contador de resultados por filtro

**Critérios de Aceite**
- Dropdown de sla_status exibe todas as opções
- Toggle is_late funciona corretamente
- Filtros são aplicados ao mudar seleção
- URL é atualizada com query params
- Badges mostram contagem de resultados
- Loading state durante busca com filtros
- Empty state quando sem resultados

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de dropdown sla_status
- Teste de seleção de opção sla_status
- Teste de toggle is_late
- Teste de atualização de URL com query params
- Teste de loading state com filtros
- Teste de empty state com filtros
- Teste de reset de filtros
- Teste de persistência de filtros na URL

---

### [ ] Tarefa 1.3: Tela de Gestão de Regras SLA

#### Especificação SDD

**Backend**
- **Endpoint:** GET /sla-rules (listagem)
- **Endpoint:** POST /sla-rules (criação)
- **Endpoint:** PUT /sla-rules/{id} (atualização)
- **Endpoint:** DELETE /sla-rules/{id} (exclusão)
- **Model SlaRule:** carrier_id, max_days, warning_threshold_days, critical_threshold_days
- **Validação:** max_days > warning_threshold_days > critical_threshold_days
- **RBAC:** Permissão `sla:write` obrigatória para POST/PUT/DELETE

**Frontend**
- **Rota:** /settings/sla
- **Tabela:** Listagem de regras SLA com carrier, max_days, thresholds
- **Formulário de criação:** Modal com campos (carrier, max_days, warning_threshold, critical_threshold)
- **Formulário de edição:** Modal pré-preenchido com dados existentes
- **Botão de exclusão:** Com confirmação
- **Validação frontend:** max_days > warning_threshold > critical_threshold
- **Feedback:** Toast de sucesso/erro

**Critérios de Aceite**
- Listagem de regras SLA exibe todas as regras
- Criação de regra funciona com validação
- Edição de regra funciona com validação
- Exclusão de regra funciona com confirmação
- Validação frontend impede thresholds inválidos
- RBAC impede acesso sem permissão sla:write
- Feedback visual em todas as operações

#### Critérios TDD

**Backend Tests**
- Teste de GET /sla-rules (listagem)
- Teste de POST /sla-rules (criação válida)
- Teste de POST /sla-rules (thresholds inválidos - 422)
- Teste de PUT /sla-rules/{id} (atualização válida)
- Teste de PUT /sla-rules/{id} (thresholds inválidos - 422)
- Teste de DELETE /sla-rules/{id} (exclusão)
- Teste de RBAC (sem permissão sla:write - 403)

**Frontend Tests**
- Teste de renderização de tabela de regras
- Teste de abertura de modal de criação
- Teste de submissão de formulário de criação
- Teste de validação de thresholds no formulário
- Teste de abertura de modal de edição
- Teste de submissão de formulário de edição
- Teste de exclusão com confirmação
- Teste de tratamento de erro 403

**E2E Tests**
- Teste de fluxo completo de criação de regra
- Teste de fluxo completo de edição de regra
- Teste de fluxo completo de exclusão de regra

---

## Épico 3 — Campos Fiscais/Financeiros (7% Pendente)

**Status Atual:** 93% completo  
**Objetivo:** Completar filtros por campos fiscais, busca global e frontend  
**Progresso:** [ ] 0/5 tarefas concluídas

### [ ] Tarefa 3.1: Filtros por Campos Fiscais no Backend

#### Especificação SDD

**Backend**
- **Endpoint:** GET /shipments com parâmetros de filtro
- **Parâmetros de filtro:**
  - `invoice_number`: string (busca parcial, case insensitive)
  - `invoice_value_min`: decimal (range mínimo)
  - `invoice_value_max`: decimal (range máximo)
  - `cfop`: string (busca exata)
- **Query SQLAlchemy:** Filtrar por campos fiscais no modelo Shipment
- **Validação:** invoice_value_min <= invoice_value_max
- **Índices:** Garantir índices em campos fiscais para performance

**Critérios de Aceite**
- Filtro por invoice_number funciona (busca parcial)
- Filtro por range de invoice_value funciona
- Filtro por cfop funciona (busca exata)
- Validação de range (min <= max)
- Performance: query com filtros fiscais <500ms para 1000 registros

#### Critérios TDD

**Backend Tests**
- Teste de filtro por invoice_number (parcial)
- Teste de filtro por invoice_number (case insensitive)
- Teste de filtro por invoice_value (range)
- Teste de filtro por cfop (exato)
- Teste de validação de range (min > max - 422)
- Teste de filtro sem resultados
- Teste de performance com 1000 registros

---

### [ ] Tarefa 3.2: Busca Global

#### Especificação SDD

**Backend**
- **Endpoint:** GET /shipments com parâmetro `search`
- **Campos pesquisados:** tracking_number, invoice_number, recipient_name
- **Busca:** Parcial, case insensitive, ILIKE no PostgreSQL
- **Prioridade:** tracking_number > invoice_number > recipient_name
- **Paginação:** Manter paginação existente

**Frontend**
- **Componente:** Barra de busca no header ou sidebar
- **Debounce:** 300ms após digitação
- **Autocomplete:** Sugestões de tracking_number (opcional)
- **Ícone:** Lupa para busca
- **Placeholder:** "Buscar por tracking, NF ou destinatário"

**Critérios de Aceite**
- Busca por tracking_number funciona
- Busca por invoice_number funciona
- Busca por recipient_name funciona
- Busca é case insensitive
- Debounce funciona (não faz busca a cada caractere)
- Placeholder está correto
- Loading state durante busca

#### Critérios TDD

**Backend Tests**
- Teste de busca por tracking_number
- Teste de busca por invoice_number
- Teste de busca por recipient_name
- Teste de busca case insensitive
- Teste de busca sem resultados
- Teste de performance com 1000 registros

**Frontend Tests**
- Teste de renderização de barra de busca
- Teste de debounce (300ms)
- Teste de busca por tracking_number
- Teste de busca por invoice_number
- Teste de loading state durante busca
- Teste de limpeza de busca

---

### [ ] Tarefa 3.3: Tabela Frontend com Campos Fiscais

#### Especificação SDD

**Frontend**
- **Tabela shipments/page.tsx:** Adicionar colunas fiscais
- **Colunas:** invoice_number, invoice_value, cfop
- **Formatação:** invoice_value em BRL (R$ 1.234,56)
- **Colunas condicionais:** Toggle para mostrar/esconder colunas fiscais
- **Ordenação:** Permitir ordenação por invoice_value
- **Responsividade:** Colunas fiscais ocultas em mobile

**Critérios de Aceite**
- Colunas fiscais são exibidas na tabela
- invoice_value é formatado em BRL
- Toggle mostra/esconde colunas fiscais
- Ordenação por invoice_value funciona
- Colunas fiscais ocultas em mobile

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de colunas fiscais
- Teste de formatação de invoice_value em BRL
- Teste de toggle de colunas fiscais
- Teste de ordenação por invoice_value
- Teste de responsividade (mobile)

---

### [ ] Tarefa 3.4: Detalhe de Shipment com Campos Fiscais

#### Especificação SDD

**Frontend**
- **Tela de detalhe:** /shipments/{id}
- **Seção fiscal:** Card com campos fiscais
- **Campos:** invoice_number, invoice_value, nf_key, cfop
- **Formatação:** invoice_value em BRL, nf_key como link (se disponível)
- **Validação:** Exibir "Não informado" para campos null

**Critérios de Aceite**
- Seção fiscal exibe todos os campos
- invoice_value formatado em BRL
- nf_key exibido como link (se disponível)
- "Não informado" para campos null

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de seção fiscal
- Teste de formatação de invoice_value
- Teste de link de nf_key
- Teste de "Não informado" para null

---

### [ ] Tarefa 3.5: Filtros Avançados no Frontend

#### Especificação SDD

**Frontend**
- **Sidebar:** Adicionar filtros fiscais
- **Filtros:** invoice_number, invoice_value (range), cfop
- **Busca global:** Barra de busca integrada
- **Toggle:** Mostrar/esconder filtros avançados
- **Badges:** Contador de resultados por filtro

**Critérios de Aceite**
- Filtros fiscais são exibidos na sidebar
- Busca global funciona
- Toggle mostra/esconde filtros
- Badges mostram contagem
- Filtros funcionam em conjunto

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de filtros fiscais
- Teste de aplicação de filtro invoice_number
- Teste de aplicação de filtro invoice_value range
- Teste de aplicação de filtro cfop
- Teste de toggle de filtros
- Teste de badges de contagem

---

## Épico 4 — Eficiência por Transportadora (50% Pendente)

**Status Atual:** 50% completo  
**Objetivo:** Implementar endpoint de agregação, ranking, tela frontend e gráficos  
**Progresso:** [ ] 0/4 tarefas concluídas

### [ ] Tarefa 4.1: Endpoint de Agregação de Eficiência

#### Especificação SDD

**Backend**
- **Endpoint:** GET /carriers/{id}/efficiency
- **Parâmetros opcionais:** date_from, date_to (ISO 8601)
- **Métricas calculadas:**
  - on_time_count: COUNT WHERE status = delivered AND delay_days <= 0
  - late_count: COUNT WHERE status = delivered AND delay_days > 0
  - lost_count: COUNT WHERE status = lost
  - total_count: COUNT WHERE status IN (delivered, lost)
- **Percentuais:**
  - on_time_rate = on_time_count / total_count
  - late_rate = late_count / total_count
  - lost_rate = lost_count / total_count
- **Response JSON:** { carrier_id, carrier_name, metrics, percentuais, period }
- **Validação:** date_from <= date_to
- **RBAC:** Permissão `carriers:read` obrigatória

**Critérios de Aceite**
- Endpoint retorna métricas corretas
- Percentuais são calculados corretamente
- Filtros por período funcionam
- Validação de período funciona
- RBAC impede acesso sem permissão
- Performance: query <1s para 10.000 registros

#### Critérios TDD

**Backend Tests**
- Teste de agregação de eficiência (sem filtros)
- Teste de cálculo de percentuais
- Teste de filtro por período (date_from, date_to)
- Teste de validação de período (date_from > date_to - 422)
- Teste de RBAC (sem permissão carriers:read - 403)
- Teste de carrier sem shipments (zero counts)
- Teste de performance com 10.000 registros

---

### [ ] Tarefa 4.2: Ranking de Transportadoras

#### Especificação SDD

**Backend**
- **Endpoint:** GET /carriers/ranking
- **Parâmetros opcionais:** date_from, date_to, limit (default: 10)
- **Agregação:** Group by carrier_id com window functions
- **Ordenação:** on_time_rate DESC, total_count DESC
- **Response JSON:** Array de { carrier_id, carrier_name, metrics, percentuais, rank }
- **Caching:** Redis cache por 5 minutos (opcional)

**Critérios de Aceite**
- Endpoint retorna ranking ordenado por on_time_rate
- Limite funciona (default: 10)
- Filtros por período funcionam
- Ordenação secundária por total_count
- Cache funciona (se implementado)

#### Critérios TDD

**Backend Tests**
- Teste de ranking (sem filtros)
- Teste de ordenação por on_time_rate
- Teste de ordenação secundária por total_count
- Teste de limite (limit=5)
- Teste de filtro por período
- Teste de cache (se implementado)

---

### [ ] Tarefa 4.3: Tela Frontend de Ranking

#### Especificação SDD

**Frontend**
- **Rota:** /shipments/analytics/carrier-efficiency
- **Tabela:** Colunas (rank, carrier, on_time_rate, late_rate, lost_rate, total)
- **Badges:** Cores por performance (verde >90%, amarelo 70-90%, vermelho <70%)
- **Filtros:** Date picker para período
- **Exportação:** Botão para exportar CSV
- **Drill-down:** Clique em carrier para ver shipments específicos

**Critérios de Aceite**
- Tabela exibe ranking corretamente
- Badges de performance funcionam
- Filtros por período funcionam
- Exportação CSV funciona
- Drill-down para carrier funciona

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de tabela de ranking
- Teste de badges de performance
- Teste de filtros por período
- Teste de exportação CSV
- Teste de drill-down para carrier

**E2E Tests**
- Teste de fluxo completo de ranking
- Teste de filtro por período
- Teste de drill-down para carrier

---

### [ ] Tarefa 4.4: Gráficos de Eficiência

#### Especificação SDD

**Frontend**
- **Biblioteca:** Recharts (já instalada)
- **Gráfico 1:** Bar chart comparativo (carrier vs on_time_rate)
- **Gráfico 2:** Pie chart de distribuição (on_time, late, lost)
- **Gráfico 3:** Line chart de tendência (eficiência por mês)
- **Interatividade:** Tooltip com detalhes, legendas
- **Responsividade:** Gráficos adaptam-se a viewport

**Critérios de Aceite**
- Bar chart exibe comparação entre carriers
- Pie chart exibe distribuição
- Line chart exibe tendência
- Tooltips funcionam
- Gráficos são responsivos

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de bar chart
- Teste de renderização de pie chart
- Teste de renderização de line chart
- Teste de tooltips
- Teste de responsividade

---

## Épico 6 — Relatório Diário Automático (50% Pendente)

**Status Atual:** 50% completo  
**Objetivo:** Completar geração manual, KPIs consolidados, envio por e-mail e agendamento  
**Progresso:** [ ] 0/4 tarefas concluídas

### [ ] Tarefa 6.1: Geração Manual de Relatório

#### Especificação SDD

**Backend**
- **Endpoint:** POST /reports/daily
- **Parâmetro opcional:** date (ISO 8601, default: hoje)
- **KPIs calculados:**
  - total_shipments: COUNT WHERE created_at = date
  - on_time_count: COUNT WHERE status = delivered AND delay_days <= 0
  - late_count: COUNT WHERE status = delivered AND delay_days > 0
  - lost_count: COUNT WHERE status = lost
  - alert_count: COUNT WHERE created_at = date AND resolved_at IS NULL
- **Resumo por transportadora:** Group by carrier_id com contagens
- **Response JSON:** { report_id, date, kpis, carrier_summary, generated_at, generated_by }
- **RBAC:** Permissão `reports:write` obrigatória

**Critérios de Aceite**
- Endpoint gera relatório com KPIs corretos
- Parâmetro date opcional funciona (default: hoje)
- Resumo por transportadora funciona
- RBAC impede acesso sem permissão
- Relatório é salvo em DailyReport

#### Critérios TDD

**Backend Tests**
- Teste de geração de relatório (sem data - default hoje)
- Teste de geração de relatório (com data específica)
- Teste de cálculo de KPIs
- Teste de resumo por transportadora
- Teste de RBAC (sem permissão reports:write - 403)
- Teste de duplicação (mesma data = novo relatório)

---

### [ ] Tarefa 6.2: Tela Frontend de Relatórios

#### Especificação SDD

**Frontend**
- **Rota:** /reports/daily
- **Lista:** Table com (date, generated_by, kpis, actions)
- **Detalhe:** Modal com KPIs detalhados e resumo por carrier
- **Filtros:** Date picker para período
- **Botão gerar:** Botão para gerar relatório manualmente
- **Exportação:** Botão para exportar CSV/JSON

**Critérios de Aceite**
- Lista exibe relatórios gerados
- Detalhe exibe KPIs e resumo por carrier
- Filtros por período funcionam
- Botão gerar funciona
- Exportação CSV/JSON funciona

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de lista de relatórios
- Teste de abertura de modal de detalhe
- Teste de filtros por período
- Teste de botão gerar
- Teste de exportação CSV
- Teste de exportação JSON

**E2E Tests**
- Teste de fluxo completo de geração
- Teste de visualização de detalhe
- Teste de exportação

---

### [ ] Tarefa 6.3: Envio Automático por E-mail

#### Especificação SDD

**Backend**
- **Service:** EmailService com SMTP configuration
- **Template:** HTML template para relatório diário
- **Endpoint:** POST /reports/{id}/send
- **Parâmetros:** recipients (array de e-mails), subject (opcional)
- **Anexo:** PDF ou CSV do relatório
- **Queue:** Background task (Celery ou similar)
- **RBAC:** Permissão `reports:write` obrigatória

**Critérios de Aceite**
- E-mail é enviado com template HTML
- Anexo (PDF/CSV) é incluído
- Múltiplos recipients funcionam
- Subject customizado funciona
- Background task funciona
- RBAC impede acesso sem permissão

#### Critérios TDD

**Backend Tests**
- Teste de envio de e-mail (SMTP mock)
- Teste de template HTML
- Teste de anexo PDF/CSV
- Teste de múltiplos recipients
- Teste de background task
- Teste de RBAC (sem permissão reports:write - 403)

---

### [ ] Tarefa 6.4: Agendamento de Geração Diária

#### Especificação SDD

**Backend**
- **Scheduler:** APScheduler ou Celery Beat
- **Cron:** 0 8 * * * (8:00 AM diário)
- **Configuração:** Tabela ScheduledReport com (enabled, time, recipients)
- **Logging:** Registro de execuções (sucesso/falha)
- **Retry:** 3 tentativas em caso de falha

**Critérios de Aceite**
- Scheduler executa diariamente às 8:00 AM
- Relatório é gerado automaticamente
- E-mail é enviado para recipients configurados
- Execuções são logadas
- Retry funciona em caso de falha

#### Critérios TDD

**Backend Tests**
- Teste de scheduler (mock de tempo)
- Teste de geração automática
- Teste de envio automático
- Teste de logging de execuções
- Teste de retry em falha

---

## Épico 8 — Integrações Assistidas (56% Pendente)

**Status Atual:** 44% completo  
**Objetivo:** Completar parser Braspress, conectores de API e UI de configuração  
**Progresso:** [ ] 0/5 tarefas concluídas

### [ ] Tarefa 8.1: Parser Braspress Completo

#### Especificação SDD

**Backend**
- **Parser:** BraspressParser com layout específico
- **Colunas Braspress:** NF, Peso, Volumes, Destinatário, Endereço, etc.
- **Mapeamento:** Colunas Braspress → campos do modelo Shipment
- **Validação:** Regras específicas Braspress (NF obrigatória, peso > 0)
- **Detecção automática:** Identificar layout Braspress por headers
- **Error handling:** Erros específicos por coluna Braspress

**Critérios de Aceite**
- Parser Braspress funciona com arquivo real
- Mapeamento de colunas está correto
- Validação específica funciona
- Detecção automática funciona
- Erros são específicos por coluna

#### Critérios TDD

**Backend Tests**
- Teste de parser Braspress (arquivo real)
- Teste de mapeamento de colunas
- Teste de validação específica
- Teste de detecção automática
- Teste de error handling
- Teste de edge cases (colunas faltando, valores inválidos)

---

### [ ] Tarefa 8.2: Contrato Base de Conector

#### Especificação SDD

**Backend**
- **Interface abstrata:** BaseConnector com métodos (parse, map, validate)
- **Métodos:**
  - parse(file): Retorna dict com dados brutos
  - map(raw_data): Retorna dict com campos do modelo
  - validate(mapped_data): Retorna (valid, errors)
- **Implementação:** BraspressConnector herda de BaseConnector
- **Extensibilidade:** Fácil adicionar novos conectores (Jadlog, etc.)

**Critérios de Aceite**
- BaseConnector define interface
- BraspressConnector implementa interface
- Métodos parse, map, validate funcionam
- Fácil adicionar novos conectores

#### Critérios TDD

**Backend Tests**
- Teste de interface BaseConnector
- Teste de implementação BraspressConnector
- Teste de método parse
- Teste de método map
- Teste de método validate
- Teste de extensibilidade (mock de novo conector)

---

### [ ] Tarefa 8.3: Mapper Específico Braspress

#### Especificação SDD

**Backend**
- **Mapper:** BraspressMapper com mapeamento específico
- **Mapeamento:** NF → invoice_number, Peso → weight, Volumes → volume, etc.
- **Transformações:** Formatação de datas, números, etc.
- **Validação:** Valores obrigatórios Braspress
- **Configuração:** Mapeamento configurável via YAML/JSON

**Critérios de Aceite**
- Mapper Braspress funciona corretamente
- Transformações são aplicadas
- Validação funciona
- Mapeamento é configurável

#### Critérios TDD

**Backend Tests**
- Teste de mapeamento de colunas
- Teste de transformações
- Teste de validação
- Teste de configuração via YAML/JSON

---

### [ ] Tarefa 8.4: UI de Configuração de Conectores

#### Especificação SDD

**Frontend**
- **Rota:** /settings/integrations
- **Lista:** Table com conectores disponíveis (Braspress, Jadlog, etc.)
- **Formulário:** Modal para configurar API keys, endpoints
- **Teste de conexão:** Botão para validar configuração
- **Status:** Badge (Conectado, Desconectado, Erro)
- **RBAC:** Permissão `integrations:write` obrigatória

**Critérios de Aceite**
- Lista exibe conectores disponíveis
- Formulário de configuração funciona
- Teste de conexão funciona
- Status é atualizado corretamente
- RBAC impede acesso sem permissão

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de lista de conectores
- Teste de abertura de modal de configuração
- Teste de submissão de formulário
- Teste de teste de conexão
- Teste de atualização de status
- Teste de tratamento de erro 403

**E2E Tests**
- Teste de fluxo completo de configuração
- Teste de teste de conexão

---

### [ ] Tarefa 8.5: Conectores de API de Transportadoras

#### Especificação SDD

**Backend**
- **Conector Jadlog:** API Jadlog para rastreamento
- **Conector Braspress:** API Braspress para rastreamento
- **Métodos:** track_shipment(tracking_number), get_shipment_details
- **Autenticação:** API key / OAuth
- **Rate limiting:** Respeitar limites da API
- **Cache:** Cache de respostas por 5 minutos

**Critérios de Aceite**
- Conector Jadlog funciona
- Conector Braspress funciona
- Autenticação funciona
- Rate limiting é respeitado
- Cache funciona

#### Critérios TDD

**Backend Tests**
- Teste de conector Jadlog (mock de API)
- Teste de conector Braspress (mock de API)
- Teste de autenticação
- Teste de rate limiting
- Teste de cache

---

## Tela de Tratativas Operacionais (Nova Funcionalidade)

**Status Atual:** 0% completo  
**Objetivo:** Implementar tela de registro de tratativas por envio  
**Progresso:** [ ] 0/4 tarefas concluídas

### [ ] Tarefa T1: Model de Tratativas

#### Especificação SDD

**Backend**
- **Model ShipmentTreatment:** id, shipment_id, user_id, treatment_type, notes, status, created_at, resolved_at
- **Tipos de tratativa:** enum ['contact_carrier', 'contact_recipient', 'internal_review', 'other']
- **Status:** enum ['open', 'in_progress', 'resolved', 'cancelled']
- **Relacionamentos:** Shipment (many-to-one), User (many-to-one)
- **Migration:** Criar tabela shipment_treatments

**Critérios de Aceite**
- Model ShipmentTreatment é criado
- Relacionamentos funcionam
- Enums são válidos
- Migration é reversível

#### Critérios TDD

**Backend Tests**
- Teste de criação de ShipmentTreatment
- Teste de relacionamento com Shipment
- Teste de relacionamento com User
- Teste de enums
- Teste de migration (upgrade/downgrade)

---

### [ ] Tarefa T2: Endpoints de Tratativas

#### Especificação SDD

**Backend**
- **Endpoint:** GET /shipments/{id}/treatments (listagem)
- **Endpoint:** POST /shipments/{id}/treatments (criação)
- **Endpoint:** PUT /treatments/{id} (atualização)
- **Endpoint:** DELETE /treatments/{id} (exclusão)
- **RBAC:** Permissão `treatments:write` obrigatória para POST/PUT/DELETE

**Critérios de Aceite**
- GET retorna tratativas de um shipment
- POST cria tratativa
- PUT atualiza tratativa
- DELETE exclui tratativa
- RBAC impede acesso sem permissão

#### Critérios TDD

**Backend Tests**
- Teste de GET /shipments/{id}/treatments
- Teste de POST /shipments/{id}/treatments
- Teste de PUT /treatments/{id}
- Teste de DELETE /treatments/{id}
- Teste de RBAC (sem permissão treatments:write - 403)

---

### [ ] Tarefa T3: Tela Frontend de Tratativas

#### Especificação SDD

**Frontend**
- **Rota:** /shipments/{id}/treatments
- **Lista:** Timeline de tratativas (ordem cronológica)
- **Formulário:** Modal para criar tratativa
- **Campos:** treatment_type (select), notes (textarea), status (select)
- **Badge:** Status da tratativa com cores
- **Filtros:** Por status e tipo

**Critérios de Aceite**
- Timeline exibe tratativas em ordem cronológica
- Formulário de criação funciona
- Badge de status funciona
- Filtros funcionam
- Empty state quando sem tratativas

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de timeline
- Teste de abertura de modal de criação
- Teste de submissão de formulário
- Teste de badge de status
- Teste de filtros
- Teste de empty state

**E2E Tests**
- Teste de fluxo completo de criação
- Teste de atualização de status

---

### [ ] Tarefa T4: Integração com Detalhe de Shipment

#### Especificação SDD

**Frontend**
- **Tela de detalhe:** /shipments/{id}
- **Seção tratativas:** Card com timeline de tratativas
- **Botão:** "Adicionar tratativa" abre modal
- **Link:** "Ver todas" vai para /shipments/{id}/treatments
- **Badge:** Contador de tratativas abertas

**Critérios de Aceite**
- Seção tratativas exibe timeline resumida
- Botão "Adicionar tratativa" funciona
- Link "Ver todas" funciona
- Badge de contador funciona

#### Critérios TDD

**Frontend Tests**
- Teste de renderização de seção tratativas
- Teste de botão "Adicionar tratativa"
- Teste de link "Ver todas"
- Teste de badge de contador

---

## Prioridades e Estimativas

### Prioridade Alta (Bloqueadores para Beta Completo)

**Épico 1 - SLA e Criticidade (3 tarefas)**
- Estimativa: 3-4 dias
- Impacto: Melhora significativa na usabilidade de SLA

**Épico 4 - Eficiência por Transportadora (4 tarefas)**
- Estimativa: 5-7 dias
- Impacto: KPI crítico para gestão de transportadoras

**Épico 6 - Relatório Diário (4 tarefas)**
- Estimativa: 4-5 dias
- Impacto: Automação de relatórios operacionais

**Total Prioridade Alta:** 12-16 dias

### Prioridade Média (Importantes mas não Bloqueadores)

**Épico 3 - Campos Fiscais/Financeiros (5 tarefas)**
- Estimativa: 4-5 dias
- Impacto: Melhora na usabilidade de campos fiscais

**Épico 8 - Integrações Externas (5 tarefas)**
- Estimativa: 7-10 dias
- Impacto: Preparação para integrações reais

**Tela de Tratativas Operacionais (4 tarefas)**
- Estimativa: 4-5 dias
- Impacto: Melhora na gestão de exceções

**Total Prioridade Média:** 15-20 dias

### Prioridade Baixa (Pós-Beta)

- Melhorias de cobertura de testes
- Integração com e-mail/SMS
- Geração agendada de relatórios
- Exportação de logs
- Rate limit e refresh tokens

**Total Prioridade Baixa:** 10-15 dias

---

## Resumo de Estimativas

| Prioridade | Tarefas | Estimativa (dias) |
|------------|---------|-------------------|
| Alta | 12 | 12-16 |
| Média | 14 | 15-20 |
| Baixa | ~10 | 10-15 |
| **Total** | **36** | **37-51** |

**Tempo estimado para conclusão:** 6-8 semanas (considerando 1 semana = 5 dias úteis)

---

## Próximos Passos Imediatos

1. **Semana 1-2:** Completar Épico 1 (SLA e Criticidade)
2. **Semana 3-4:** Completar Épico 4 (Eficiência por Transportadora)
3. **Semana 5:** Completar Épico 6 (Relatório Diário)
4. **Semana 6-7:** Completar Épico 3 (Campos Fiscais/Financeiros)
5. **Semana 8:** Completar Épico 8 (Integrações Externas) e Tela de Tratativas

---

## Conclusão

Este roadmap apresenta 25 tarefas pendentes distribuídas em 6 épicos, com especificações SDD detalhadas e critérios TDD definidos para cada funcionalidade. O foco é completar as funcionalidades core (Épicos 1, 4, 6) nas primeiras 4 semanas, seguido por melhorias de usabilidade (Épicos 3, 8) e novas funcionalidades (Tratativas).

A metodologia SDD + TDD garante que cada funcionalidade seja especificada antes da implementação e testada antes de ser considerada completa, reduzindo riscos e garantindo qualidade.

---

**Assinatura:** Equipe Ilex Logística  
**Data:** 2026-06-23  
**Versão:** 1.0 (SDD + TDD)
