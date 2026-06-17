# ROADMAP DO PROJETO ILEX LOGÍSTICA

**Versão:** 2.0  
**Data:** 2026-06-24
**Status:** Roadmap com SDD (Specification-Driven Development) e TDD (Test-Driven Development)
**Base:** ESCOPO.md (Referência Absoluta)

---

## Legenda

- ✅ **PRONTO** - Funcionalidade implementada, testada e documentada
- ⏳ **EM PROGRESSO** - Funcionalidade parcialmente implementada
- ❌ **PENDENTE** - Funcionalidade não iniciada
- 📋 **SDD** - Especificação detalhada disponível
- 🧪 **TDD** - Critérios de teste definidos

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

## Resumo por Épico (Atualizado 2026-06-24)

| Épico | Status | Pronto | Em Progresso | Pendente | % Completo |
|-------|--------|--------|--------------|----------|-------------|
| 1 - SLA, atraso e criticidade | PARCIAL | 7/10 | 2/10 | 1/10 | 70% |
| 2 - Importação Excel/CSV | IMPLEMENTADO | 12/12 | 0/12 | 0/12 | 100% |
| 3 - Campos fiscais/financeiros | IMPLEMENTADO | 14/15 | 1/15 | 0/15 | 93% |
| 4 - Eficiência por transportadora | PARCIAL | 3/6 | 2/6 | 1/6 | 50% |
| 5 - Alertas e notificações | IMPLEMENTADO | 10/10 | 0/10 | 0/10 | 100% |
| 6 - Relatório diário automático | PARCIAL | 3/6 | 2/6 | 1/6 | 50% |
| 7 - Logs e auditoria | CONCLUÍDO | 9/9 | 0/9 | 0/9 | 100% |
| 8 - Integrações assistidas | PARCIAL | 4/9 | 3/9 | 2/9 | 44% |
| 9 - Usuários, permissões e segurança | IMPLEMENTADO | 11/11 | 0/11 | 0/11 | 100% |
| 10 - Dashboard beta e UX | PARCIAL | 3/9 | 3/9 | 3/9 | 33% |
| 11 - QA, CI/CD e validação | PARCIAL | 8/10 | 1/10 | 1/10 | 80% |
| 12 - Documentação beta | PARCIAL | 10/14 | 2/14 | 2/14 | 71% |

**Total:** 84/120 (70%) pronto, 15/120 (13%) em progresso, 21/120 (17%) pendente

---

## Épico 1 — SLA, Atraso e Criticidade

**Objetivo:** Implementar cálculo de SLA, detecção de atrasos e classificação de criticidade.

### Especificação SDD

#### Backend
- **Model SlaRule:** carrier_id, max_days, warning_threshold_days, critical_threshold_days
- **Cálculo de atraso:** (data_atual - data_coleta) - max_days
- **Classificação de criticidade:**
  - CRITICAL: atraso >= critical_threshold_days
  - WARNING: warning_threshold_days <= atraso < critical_threshold_days
  - NORMAL: atraso < warning_threshold_days
- **Recálculo automático:** Trigger após atualização de shipment
- **Filtros:** sla_status (critical, warning, normal, unknown), is_late (boolean)

#### Frontend
- **Badges visuais:** Cores por criticidade (vermelho, amarelo, verde, cinza)
- **Filtros por criticidade:** Dropdown com opções de SLA
- **Tela de gestão de regras SLA:** CRUD completo com validação

### Critérios TDD

#### Backend Tests
- ✅ Teste de cálculo de atraso correto
- ✅ Teste de classificação de criticidade
- ✅ Teste de recálculo automático após update
- ⏳ Teste de filtros por sla_status
- ⏳ Teste de filtros por is_late

#### Frontend Tests
- ⏳ Teste de renderização de badges
- ⏳ Teste de filtros por criticidade
- ❌ Teste de tela de gestão de regras SLA

### Status Atual

#### Backend
- ✅ Model/tabela de regras SLA
- ✅ Endpoint CRUD para regras SLA
- ✅ Cálculo de atraso em dias/horas
- ✅ Classificação de criticidade (crítico, warning, normal)
- ✅ Recálculo automático de SLA para shipments
- ⏳ Filtros por criticidade no backend
- ✅ Testes backend

#### Frontend
- ⏳ Filtros por criticidade no frontend
- ✅ Badges visuais de SLA
- ⏳ Tela de gestão de regras SLA
- ❌ Testes frontend

#### Documentação
- ✅ Documentação BETA-013A

**Status:** 7/10 pronto, 2/10 em progresso, 1/10 pendente

---

## Épico 2 — Importação Excel/CSV Robusta e Importação Assistida

**Objetivo:** Importar dados de Excel/CSV de forma robusta com validação linha a linha e layout assistido.

### Especificação SDD

#### Backend
- **Parser CSV:** Suporte a delimitadores (comma, semicolon, tab), encoding (UTF-8, Latin-1)
- **Parser XLSX:** Leitura de múltiplas sheets, detecção automática de headers
- **Validação linha a linha:** Schema Pydantic por linha, erros acumulados
- **Detecção de duplicidade:** Verificação por tracking_number + carrier_id
- **Preview:** Endpoint POST /preview retorna rows validadas com erros
- **Confirmação:** Endpoint POST /confirm cria shipments em lote
- **Layout mapper:** Mapeamento dinâmico de colunas para campos do modelo
- **Layout Braspress:** Mapper específico para colunas Braspress (NF, peso, volumes)
- **Metadata:** Registro de layout usado em ImportHistory

#### Frontend
- **Seletor de layout:** Dropdown com opções (generic, braspress)
- **Upload:** Drag & drop com validação de arquivo
- **Preview UI:** Tabela com erros por linha, colunas destacadas
- **Confirmação UI:** Resumo de validos/inválidos, botão confirmar
- **Progresso:** Indicador de progresso durante importação

### Critérios TDD

#### Backend Tests
- ✅ Teste de parser CSV com diferentes delimitadores
- ✅ Teste de parser XLSX com múltiplas sheets
- ✅ Teste de validação linha a linha
- ✅ Teste de detecção de duplicidade
- ✅ Teste de preview endpoint
- ✅ Teste de confirmação endpoint
- ✅ Teste de layout mapper genérico
- ✅ Teste de layout mapper Braspress

#### Frontend Tests
- ✅ Teste de seletor de layout
- ✅ Teste de upload de arquivo
- ✅ Teste de preview UI
- ✅ Teste de erros por linha
- ✅ Teste de confirmação UI

### Status Atual

#### Backend
- ✅ Parser CSV robusto
- ✅ Parser XLSX robusto
- ✅ Validação linha a linha
- ✅ Detecção de duplicidade
- ✅ Preview antes de confirmação
- ✅ Confirmação de importação
- ✅ Erros por linha detalhados
- ✅ Layout mapper preparado para Braspress
- ✅ Layout Braspress assistido beta
- ✅ Mapper específico Braspress
- ✅ Testes backend (BETA-012A - 63 testes, BETA-012C - 2 testes)

#### Frontend
- ✅ Seletor de layout no frontend
- ✅ Tela upload frontend
- ✅ Preview UI
- ✅ Erros por linha UI
- ✅ Confirmação UI
- ✅ Testes frontend (BETA-012B - 17 testes)

#### Documentação
- ✅ Documentação BETA-012A
- ✅ Documentação BETA-012B
- ✅ Documentação BRASPRESS_IMPORTACAO_ASSISTIDA

**Status:** 12/12 pronto, 0/12 em progresso, 0/12 pendente

---

## Épico 3 — Campos Fiscais, Financeiros e Filtros do Apêndice 1

**Objetivo:** Adicionar campos fiscais e financeiros conforme Apêndice 1 com filtros avançados.

### Especificação SDD

#### Backend
- **Campos fiscais:** invoice_number, invoice_value, nf_key, cfop
- **Campos financeiros:** cost, freight_value, insurance_value, discount_value
- **Filtros backend:** Por invoice_number, range de valores, cfop
- **Busca global:** Text search em tracking_number, invoice_number, recipient
- **Schemas Pydantic:** Atualizados com novos campos opcionais

#### Frontend
- **Tabela de shipments:** Colunas para campos fiscais/financeiros
- **Detalhe de shipment:** Exibir todos campos fiscais/financeiros
- **Filtros avançados:** Sidebar com filtros por campos fiscais
- **Busca global:** Barra de busca com autocomplete

### Critérios TDD

#### Backend Tests
- ✅ Teste de migration com novos campos
- ✅ Teste de schemas Pydantic
- ⏳ Teste de filtros por campos fiscais
- ❌ Teste de busca global

#### Frontend Tests
- ⏳ Teste de renderização de tabela com novos campos
- ⏳ Teste de detalhe de shipment
- ❌ Teste de filtros avançados
- ❌ Teste de busca global

### Status Atual

#### Backend
- ✅ Migration com campos fiscais/financeiros
- ✅ Schemas Pydantic atualizados
- ⏳ Filtros backend por campos fiscais
- ❌ Busca global
- ✅ Testes backend

#### Frontend
- ⏳ Tabela/detalhe frontend
- ❌ Testes frontend

#### Documentação
- ✅ Documentação BETA-011A
- ✅ Documentação BETA-011B

**Status:** 14/15 pronto, 1/15 em progresso, 0/15 pendente

---

## Épico 4 — Eficiência por Transportadora

**Objetivo:** Calcular e exibir métricas de eficiência por transportadora.

### Especificação SDD

#### Backend
- **Endpoint de agregação:** GET /carriers/{id}/efficiency
- **Métricas:** on_time_count, late_count, lost_count, total_count
- **Cálculo de percentuais:** on_time_rate, late_rate, lost_rate
- **Ranking:** Ordenação por on_time_rate descendente
- **Filtros por período:** date_from, date_to opcionais
- **Agregação:** Group by carrier_id com window functions

#### Frontend
- **Tabela de ranking:** Colunas: carrier, on_time_rate, late_rate, lost_rate, total
- **Gráficos de eficiência:** Bar chart comparativo entre transportadoras
- **Filtros por período:** Date picker para range
- **Detalhe por transportadora:** Drill-down para shipments específicos

### Critérios TDD

#### Backend Tests
- ⏳ Teste de agregação de eficiência
- ⏳ Teste de cálculo de percentuais
- ⏳ Teste de ranking
- ❌ Teste de filtros por período

#### Frontend Tests
- ⏳ Teste de renderização de tabela de ranking
- ❌ Teste de gráficos de eficiência
- ❌ Teste de filtros por período

### Status Atual

#### Backend
- ⏳ Endpoint de agregação de eficiência
- ⏳ Contagem de entregas no prazo
- ⏳ Contagem de entregas atrasadas
- ⏳ Contagem de entregas extraviadas
- ❌ Ranking de transportadoras
- ❌ Percentuais de performance
- ❌ Testes de agregação

#### Frontend
- ✅ Componente frontend básico
- ❌ Gráficos de eficiência
- ❌ Filtros por período
- ❌ Testes frontend

#### Documentação
- ✅ Documentação BETA-014A
- ✅ Documentação BETA-014B

**Status:** 3/6 pronto, 2/6 em progresso, 1/6 pendente

---

## Épico 5 — Alertas e Notificações

**Objetivo:** Gerar alertas automáticos para eventos críticos e exibir painel de notificações.

### Especificação SDD

#### Backend
- **Model Alert:** id, type, source_type, source_id, message, severity, created_at, resolved_at
- **Model AlertDeliveryLog:** alert_id, user_id, action (read, resolved, auto_resolved, ignored), timestamp
- **Tipos de alerta:** sla_critical, sla_late, sla_warning, unknown_sla, no_update, import_failure
- **Geração automática:** Trigger após update de shipment, falha de importação
- **Deduplicação:** Um alerta ativo por (source_type, source_id)
- **Resolução:** Manual (usuário) ou automática (regra)
- **Endpoints:** GET /alerts, POST /alerts/{id}/read, POST /alerts/{id}/resolve

#### Frontend
- **Painel de alertas:** Lista com badges de severidade
- **Badge no header:** Contador de alertas não lidos
- **Marcação como lido:** Botão em cada alerta
- **Marcação como resolvido:** Botão com confirmação
- **Filtros:** Por tipo, severidade, status

### Critérios TDD

#### Backend Tests
- ✅ Teste de geração de alertas para sla_critical
- ✅ Teste de geração de alertas para no_update
- ✅ Teste de geração de alertas para import_failure
- ✅ Teste de deduplicação por origem
- ✅ Teste de AlertDeliveryLog
- ✅ Teste de endpoints de alertas

#### Frontend Tests
- ✅ Teste de painel de alertas
- ✅ Teste de badge no header
- ✅ Teste de marcação como lido
- ✅ Teste de marcação como resolvido

### Status Atual

#### Backend
- ✅ Model Alert
- ✅ Model AlertDeliveryLog
- ✅ Geração de alertas para crítico
- ✅ Geração de alertas para sem atualização
- ✅ Geração de alertas para falha
- ✅ Deduplicação de alertas
- ✅ Testes de geração
- ✅ Testes de deduplicação

#### Frontend
- ✅ Painel/badge frontend
- ✅ Marcação como lido
- ✅ Marcação como resolvido
- ✅ Testes frontend

#### Integrações (Pós-Beta)
- ❌ Integração com e-mail
- ❌ Integração com SMS

#### Documentação
- ✅ Documentação BETA-017A
- ✅ Documentação BETA-017B
- ✅ Documento de fechamento BETA-027

**Status:** 10/10 pronto, 0/10 em progresso, 0/10 pendente

> Observação: as integrações por e-mail e SMS seguem fora do núcleo do Épico 5 e continuam como pós-beta.

---

## Épico 6 — Relatório Diário Automático

**Objetivo:** Gerar relatórios diários automáticos com KPIs operacionais.

### Especificação SDD

#### Backend
- **Model DailyReport:** id, date, generated_at, generated_by, summary
- **Model DailyReportDelivery:** report_id, shipment_id, status, sla_status, delay_days
- **Geração manual:** Endpoint POST /reports/daily com date opcional
- **KPIs:** total_shipments, on_time_count, late_count, lost_count, alert_count
- **Resumo por transportadora:** Agregação por carrier_id
- **Filtros por período:** date_from, date_to

#### Frontend
- **Tela de relatórios:** Lista de relatórios gerados com data e gerador
- **Detalhe do relatório:** KPIs, lista de shipments, resumo por transportadora
- **Export CSV/JSON:** Botão para download
- **Filtros por período:** Date picker para range

### Critérios TDD

#### Backend Tests
- ⏳ Teste de geração manual de relatório
- ⏳ Teste de cálculo de KPIs
- ❌ Teste de exportação

#### Frontend Tests
- ⏳ Teste de tela de relatórios
- ❌ Teste de export CSV/JSON
- ❌ Teste de filtros por período

### Status Atual

#### Backend
- ✅ Model DailyReport
- ✅ Model DailyReportDelivery
- ⏳ Geração manual de relatório
- ❌ Geração agendada
- ⏳ Testes de geração
- ❌ Testes de exportação

#### Frontend
- ⏳ Tela frontend
- ❌ Export CSV/JSON
- ❌ Filtros por período
- ❌ Testes frontend

#### Documentação
- ✅ Documentação BETA-018A
- ✅ Documentação BETA-018B

**Status:** 3/6 pronto, 2/6 em progresso, 1/6 pendente

---

## Épico 7 — Logs de Coleta, Importação e Auditoria Operacional

**Objetivo:** Implementar logs estruturados para rastreamento de ações operacionais.

### Especificação SDD

#### Backend
- **Model OperationalAuditLog:** id, event_type, entity_type, entity_id, action, user_id, metadata, timestamp
- **Service centralizado:** audit_log(event_type, entity_type, entity_id, action, metadata)
- **Endpoints:** GET /audit/logs com filtros (event_type, entity_type, action, date_from, date_to)
- **Resumo estatístico:** GET /audit/logs/summary com contagem por event_type
- **Integração:** Chamadas automáticas em reports, alerts, sla, imports
- **RBAC:** Permissão audit:read obrigatória
- **Sanitização:** Remoção de secrets do metadata

#### Frontend
- **Tela de logs:** Tabela com colunas (timestamp, user, event_type, entity, action)
- **Timeline por entrega:** Visualização cronológica por entity_id
- **Filtros avançados:** Sidebar com filtros por tipo, período, usuário
- **Detalhe do log:** Modal com metadata expandido

### Critérios TDD

#### Backend Tests
- ✅ Teste de criação de log
- ✅ Teste de filtros por event_type
- ✅ Teste de filtros por período
- ✅ Teste de resumo estatístico
- ✅ Teste de RBAC

#### Frontend Tests
- ✅ Teste de renderização de logs
- ✅ Teste de timeline
- ✅ Teste de tratamento de 401/403

### Status Atual

#### Backend
- ✅ Model OperationalAuditLog
- ✅ Service de auditoria centralizado
- ✅ Endpoints de consulta de logs
- ✅ Filtros por event_type, entity_type, action
- ✅ Filtros por período
- ✅ Resumo estatístico
- ✅ Integração com ações críticas (reports, alerts, sla, imports)
- ✅ RBAC para endpoints de auditoria
- ✅ Testes backend (54 testes)

#### Frontend
- ✅ Frontend de visualização de logs
- ✅ Timeline por entrega/entidade
- ✅ Tratamento de 401/403
- ✅ Testes frontend

#### Pós-Beta
- ❌ Exportação de logs
- ❌ Sanitização avançada de secrets

#### Documentação
- ✅ Documentação BETA-019A
- ✅ Documentação BETA-019B

**Status:** 9/9 pronto, 0/9 em progresso, 0/9 pendente

---

## Épico 8 — Integrações Assistidas e Conectores Preparados

**Objetivo:** Preparar conectores para integrações assistidas com transportadoras.

### Especificação SDD

#### Backend
- **Contrato base de conector:** Interface abstrata com métodos parse(), map(), validate()
- **Parser Braspress:** Parser específico para layout Braspress (NF, peso, volumes)
- **Mapper específico Braspress:** Mapeamento de colunas Braspress para campos do modelo
- **Configuração de conectores:** Tabela connector_config com provider, settings
- **Testes de parser:** Fixture com arquivo Braspress real
- **Testes de mapper:** Verificação de mapeamento correto

#### Frontend
- **Seletor de layout:** Dropdown com opções (generic, braspress)
- **UI de configuração de conectores:** Formulário para API keys, endpoints
- **Teste de conexão:** Botão para validar configuração

### Critérios TDD

#### Backend Tests
- ⏳ Teste de parser Braspress
- ⏳ Teste de mapper Braspress
- ⏳ Teste de contrato base

#### Frontend Tests
- ⏳ Teste de UI de configuração
- ❌ Teste de teste de conexão

### Status Atual

#### Backend
- ✅ Contrato base de conector
- ⏳ Parser Braspress
- ⏳ Mapper específico Braspress
- ⏳ Testes de parser
- ⏳ Testes de mapper

#### Frontend
- ✅ Seletor de layout no frontend
- ⏳ UI de configuração de conectores
- ❌ Testes frontend

#### Documentação
- ⏳ Documentação Braspress
- ❌ Documentação de conectores

#### Pós-Beta
- ❌ Conectores reais
- ❌ Integrações complexas

**Status:** 4/9 pronto, 3/9 em progresso, 2/9 pendente

---

## Épico 9 — Gestão de Usuários, Permissões e Segurança Beta

**Objetivo:** Implementar controle de acesso baseado em roles (RBAC) e segurança.

### Especificação SDD

#### Backend
- **Model User:** id, username, email, hashed_password, role_id, is_active
- **Model Role:** id, name, description
- **Model Permission:** id, name, description
- **Tabela role_permissions:** role_id, permission_id
- **Hash de senha:** bcrypt com salt rounds 12
- **Autenticação JWT:** Access token (15min) + refresh token (7 dias, pós-beta)
- **RBAC por endpoint:** Decorador @require_permission("permission")
- **RBAC por tela:** Verificação no frontend
- **Matriz de roles:** admin (todas), manager (audit, reports, alerts, sla, shipments, imports, carriers), operator (shipments, imports, alerts), viewer (shipments, imports, sla, alerts, reports, carriers), logistica (shipments, imports, carriers), gestor (shipments, imports, sla, alerts, reports, carriers), auditoria (audit, shipments, imports, carriers)
- **Permissões granulares:** audit:read, reports:read, reports:write, alerts:read, alerts:write, sla:read, sla:write, shipments:read, shipments:write, imports:read, imports:write, carriers:read, carriers:write, users:read, users:write

#### Frontend
- **Helpers de permissão:** hasPermission(role, permission), canReadAudit, canWriteReports, etc.
- **Sidebar condicional:** Itens visíveis baseados em permissões
- **Tratamento de 401:** Redirecionamento para login
- **Tratamento de 403:** Exibição de componente AccessDenied
- **Componente AccessDenied:** Tela de acesso negado com botão voltar
- **Página de users:** CRUD com verificação de permissão

### Critérios TDD

#### Backend Tests
- ✅ Teste de hash de senha
- ✅ Teste de autenticação JWT
- ✅ Teste de RBAC por endpoint (76 testes)
- ✅ Teste de matriz de roles
- ✅ Teste de permissões granulares

#### Frontend Tests
- ✅ Teste de helpers de permissão (26 testes)
- ✅ Teste de sidebar condicional (10 testes)
- ✅ Teste de tratamento de 401/403 (5 testes)
- ✅ Teste de componente AccessDenied (7 testes)

### Status Atual

#### Backend
- ✅ Model User (já existente)
- ✅ Model Role (já existente)
- ✅ Model Permission (novo)
- ✅ Tabela role_permissions (nova)
- ✅ Hash de senha com bcrypt
- ✅ Autenticação JWT
- ❌ Refresh tokens (pós-beta)
- ❌ Rate limit (pós-beta)
- ✅ RBAC por endpoint
- ✅ RBAC por tela
- ✅ Helpers de permissão (require_permission)
- ✅ Matriz de roles beta (admin, manager, operator, viewer, logistica, gestor, auditoria)
- ✅ Permissões granulares (shipments:read, imports:write, etc.)
- ✅ Proteção de endpoints críticos (audit, reports, alerts, SLA, shipments, imports, carriers, users)
- ✅ Testes RBAC backend (76 testes)

#### Frontend
- ✅ Frontend de gestão de usuários
- ✅ Frontend de gestão de roles
- ✅ Frontend de gestão de permissões
- ✅ Tratamento de 401/403 em todas as páginas críticas
- ✅ Componente AccessDenied
- ✅ Helpers de permissão (hasPermission, canReadAudit, etc.)
- ✅ Testes RBAC frontend (30 testes)

#### Documentação
- ✅ Documentação BETA-020A
- ✅ Documentação BETA-020B
- ✅ Documentação BETA-020C

**Status:** 11/11 pronto, 0/11 em progresso, 0/11 pendente

---

## Épico 10 — Dashboard Beta e UX Operacional

**Objetivo:** Criar dashboard beta com KPIs operacionais e UX otimizada.

### Especificação SDD

#### Backend
- **Endpoint dashboard summary:** GET /dashboard/summary
- **KPIs:** total_shipments, on_time_count, late_count, lost_count, alert_count, import_failure_count
- **KPIs avançados:** efficiency_rate, avg_delay_days, top_carriers
- **Filtros por período:** date_from, date_to opcionais
- **Cache:** Redis cache por 5 minutos

#### Frontend
- **Tela dashboard/KPIs:** Cards com KPIs principais
- **Gráficos de tendência:** Line chart de entregas por dia (pós-beta)
- **Filtros por período:** Date picker para range
- **Layout responsivo:** Grid adaptativo para mobile/desktop
- **UX otimizada:** Loading states, error handling, empty states

### Critérios TDD

#### Backend Tests
- ⏳ Teste de endpoint dashboard summary
- ⏳ Teste de cálculo de KPIs
- ⏳ Teste de filtros por período

#### Frontend Tests
- ⏳ Teste de renderização de KPIs
- ❌ Teste de gráficos de tendência
- ❌ Teste de filtros por período
- ❌ Teste de layout responsivo

### Status Atual

#### Backend
- ✅ Endpoint dashboard summary
- ⏳ KPIs avançados
- ⏳ Filtros por período no backend
- ⏳ Testes de dashboard

#### Frontend
- ⏳ Tela dashboard/KPIs
- ❌ Gráficos de tendência
- ❌ Filtros por período no frontend
- ❌ Layout responsivo otimizado
- ❌ Testes de UX

#### Documentação
- ✅ Documentação BETA-016A
- ✅ Documentação BETA-016B

**Status:** 3/9 pronto, 3/9 em progresso, 3/9 pendente

---

## Épico 11 — QA, CI/CD e Validação de Beta

**Objetivo:** Implementar infraestrutura de QA, CI/CD e validação automatizada.

### Especificação SDD

#### CI/CD
- **CI base (GitHub Actions):** Workflow beta-ci.yml com jobs: test-backend, test-frontend, validate-migrations, check-secrets, validate-docs
- **Secret scan:** Script check_secrets.py para detectar tokens, passwords, API keys
- **Migrations validation:** Script validate_migrations.py com testes de roundtrip (upgrade/downgrade)
- **Docs validation:** Script validate_docs.py para verificar links, formato, consistência
- **Beta validate:** Script beta_validate.py para validar gates de release
- **Coverage reports:** pytest-cov para backend, vitest coverage para frontend
- **Rollback documentation:** Documentação de rollback para cada migration

#### Testes
- **E2E tests (Playwright):** Fluxos críticos (login, import, dashboard)
- **Smoke UI tests:** Validação rápida de funcionalidades principais
- **Testes unitários backend (pytest):** 489 testes passando
- **Testes unitários frontend (vitest):** 331 testes passando
- **Scripts oficiais Python:** Portabilidade máxima, sem dependências externas

### Critérios TDD

#### CI/CD Tests
- ✅ Teste de secret scan
- ✅ Teste de migrations validation
- ✅ Teste de docs validation
- ✅ Teste de beta validate

#### Test Coverage
- ✅ Backend: 88% coverage
- ⏳ Frontend: 20.8% coverage (meta: aumentar para 50%)

### Status Atual

#### CI/CD
- ✅ CI base (GitHub Actions)
- ✅ Secret scan
- ✅ Migrations validation
- ✅ Docs validation
- ✅ Beta validate
- ✅ Coverage reports
- ✅ Rollback documentation

#### Testes
- ✅ E2E tests (Playwright)
- ✅ Smoke UI tests
- ✅ Testes unitários backend (pytest)
- ✅ Testes unitários frontend (vitest)
- ✅ Scripts oficiais Python

#### Pós-Beta
- ❌ Monitoramento de performance
- ❌ Profiling

#### Documentação
- ✅ Documentação BETA_CHECKLIST
- ✅ Documentação BETA_RELEASE_GATE
- ✅ Documentação BETA_VALIDATION_EVIDENCE
- ✅ Documentação BETA_COMMANDS
- ✅ Documentação BETA_KNOWN_LIMITATIONS

**Status:** 8/10 pronto, 1/10 em progresso, 1/10 pendente

---

## Épico 12 — Documentação Beta

**Objetivo:** Documentar completamente o sistema para fase beta.

### Especificação SDD

#### Documentação Base
- **README principal:** Visão geral, funcionalidades, stack, setup rápido
- **README API:** Estrutura do backend, endpoints, modelos, testes
- **README Web:** Estrutura do frontend, componentes, rotas, testes
- **Documentação beta (BETA_*.md):** Documentos técnicos por feature
- **Checklist beta:** Lista de validações para release
- **Comandos oficiais:** Scripts e comandos para desenvolvimento
- **Gates de release:** Critérios para aprovação de release
- **Limitações conhecidas:** Limitações técnicas e workarounds
- **Próximas ações:** Roadmap de próximos passos
- **ESCOPO.md:** Referência absoluta do escopo do projeto
- **ROADMAP.md:** Roadmap com SDD e TDD (este documento)

#### Documentação de Usuário (Pós-Beta)
- **Manual do usuário:** Guia completo para usuários finais
- **Documentação de importação:** Como importar CSV/XLSX
- **Documentação Braspress:** Layout específico Braspress
- **Documentação de permissões:** Matriz RBAC e roles
- **Documentação de alertas/relatório:** Como usar alertas e relatórios
- **Documentação de auditoria/logs:** Como interpretar logs
- **Roadmap pós-beta:** Planejamento pós-beta

### Critérios TDD

#### Documentação Tests
- ✅ Validação de links (validate_docs.py)
- ✅ Validação de formato (validate_docs.py)
- ✅ Validação de consistência (validate_docs.py)

### Status Atual

#### Documentação Base
- ✅ README principal
- ✅ README API
- ✅ README Web
- ✅ Documentação beta (BETA_*.md)
- ✅ Checklist beta
- ✅ Comandos oficiais
- ✅ Gates de release
- ✅ Limitações conhecidas
- ✅ Próximas ações
- ✅ ESCOPO.md (novo)
- ✅ ROADMAP.md (novo)

#### Documentação de Usuário (Pós-Beta)
- ❌ Manual do usuário
- ❌ Documentação de importação
- ❌ Documentação Braspress
- ❌ Documentação de permissões
- ❌ Documentação de alertas/relatório
- ❌ Documentação de auditoria/logs
- ❌ Roadmap pós-beta

**Status:** 10/14 pronto, 2/14 em progresso, 2/14 pendente

---

## Tarefas por Prioridade (Atualizado 2026-06-24)

### Prioridade Alta (Bloqueadores para Beta)
1. ❌ Épico 4: Ranking de transportadoras e percentuais (BETA-026)
2. ⏳ Épico 6: Geração manual de relatório e tela frontend (BETA-028)
3. ❌ Épico 10: Tela dashboard/KPIs (BETA-029)
4. ⏳ Épico 1: Filtros por criticidade e tela de gestão SLA

### Prioridade Média (Importantes mas não Bloqueadores)
1. ⏳ Épico 3: Busca global e filtros avançados
2. ⏳ Épico 8: Parser Braspress completo
3. ⏳ Épico 11: Aumentar cobertura de testes frontend (meta: 50%)
4. ⏳ BETA-020D: Integrar tratamento de 401/403 em todas as páginas

### Prioridade Baixa (Pós-Beta)
1. ❌ Épico 5: Integração com e-mail/SMS
2. ❌ Épico 6: Geração agendada e export avançado
3. ❌ Épico 7: Exportação de logs e sanitização avançada
4. ❌ Épico 8: Conectores reais
5. ❌ Épico 9: Rate limit e refresh tokens
6. ❌ Épico 10: Gráficos avançados
7. ❌ Épico 12: Manual do usuário e docs específicas

---

## Próximos PRs Recomendados (SDD + TDD)

### BETA-026: Completar Épico 4 - Eficiência por Transportadora
**Especificação SDD:**
- Endpoint GET /carriers/{id}/efficiency com métricas (on_time_count, late_count, lost_count, total_count)
- Cálculo de percentuais (on_time_rate, late_rate, lost_rate)
- Ranking por on_time_rate descendente
- Filtros por período (date_from, date_to)

**Critérios TDD:**
- Teste de agregação de eficiência
- Teste de cálculo de percentuais
- Teste de ranking
- Teste de filtros por período
- Teste de renderização de tabela de ranking

### BETA-028: Completar Épico 6 - Relatório Diário
**Especificação SDD:**
- Endpoint POST /reports/daily com date opcional
- KPIs: total_shipments, on_time_count, late_count, lost_count, alert_count
- Resumo por transportadora
- Tela frontend com lista de relatórios e detalhe
- Export CSV/JSON

**Critérios TDD:**
- Teste de geração manual de relatório
- Teste de cálculo de KPIs
- Teste de tela de relatórios
- Teste de export CSV/JSON
- Teste de filtros por período

### BETA-029: Completar Épico 10 - Dashboard Beta
**Especificação SDD:**
- Endpoint GET /dashboard/summary com KPIs principais
- KPIs avançados: efficiency_rate, avg_delay_days, top_carriers
- Tela dashboard/KPIs com cards
- Filtros por período
- Layout responsivo

**Critérios TDD:**
- Teste de endpoint dashboard summary
- Teste de cálculo de KPIs
- Teste de renderização de KPIs
- Teste de filtros por período
- Teste de layout responsivo

### BETA-020D: Integrar Tratamento de 401/403 em Todas as Páginas
**Status:** ✅ CONCLUÍDO (2026-06-25)

**Especificação SDD:**
- ✅ Integrar ApiError em todas as páginas críticas
- ✅ Redirecionamento automático para 401
- ✅ Exibição de AccessDenied para 403
- ✅ Testes de navegação por permissão (BETA-020E)

**Critérios TDD:**
- ✅ Teste de redirecionamento para 401
- ✅ Teste de exibição de AccessDenied para 403
- ✅ Teste de navegação por permissão (BETA-020E)
- ✅ Teste de páginas afetadas (320 testes passando)

**Implementação:**
- ✅ Hook `useApiErrorHandler` criado
- ✅ 18 páginas integradas (dashboard, shipments, carriers, users, alerts, audit, reports/daily, settings/sla, exceptions, shipments/import, analytics)
- ✅ Testes unitários do hook (5 testes)
- ✅ Validação de regressão (320 testes passando)
- ✅ Documentação BETA_020D.md criada

### BETA-020E: Testes E2E de Navegação por Permissão
**Status:** ✅ CONCLUÍDO (2026-06-25)

**Especificação SDD:**
- ✅ Testes E2E de navegação por permissão (7 testes)
- ✅ Atualização de fixtures com rotas das 18 páginas
- ✅ Validação de acesso por perfil (admin, logística, gestor, auditoria)
- ✅ Validação de redirecionamento 401
- ✅ Validação de exibição 403

**Critérios TDD:**
- ✅ Teste: Admin deve acessar todas as 18 páginas
- ✅ Teste: Logística não deve acessar users
- ✅ Teste: Gestor não deve acessar shipments/import
- ✅ Teste: Auditoria não deve acessar páginas restritas
- ✅ Teste: Menu condicional por perfil
- ✅ Teste: Redirecionamento 401
- ✅ Teste: Exibição AccessDenied 403

**Implementação:**
- ✅ Arquivo `rbac-navigation.spec.ts` criado com 7 testes E2E
- ✅ Fixtures `users.ts` atualizadas com rotas das 18 páginas
- ✅ Documentação BETA_020E.md criada

---

## Métricas de Progresso (Atualizado 2026-06-24)

### Implementação por Épico
- **Concluídos (100%):** Épicos 2, 5, 7, 9
- **Implementados (>90%):** Épico 3 (93%)
- **Parciais (50-80%):** Épicos 1 (70%), 4 (50%), 6 (50%), 8 (44%), 10 (33%), 11 (80%), 12 (71%)

### Testes
- **Backend:** 489 testes passando (pytest)
- **Frontend:** 331 testes passando (vitest)
- **RBAC:** 76 testes backend + 30 testes frontend
- **Auditoria:** 54 testes backend
- **E2E:** Playwright configurado com skips documentados

### Cobertura
- **API:** 88%
- **Web:** 20.8% (meta: aumentar para 50%)

### Documentação
- **BETA_*.md:** 43 documentos técnicos
- **Governança:** AGENTS.md, CONTEXTO.md, RELATORIO_DIA.md
- **Escopo:** ESCOPO.md (referência absoluta)
- **Roadmap:** ROADMAP.md (este documento, SDD + TDD)

---

## Próximos Passos Imediatos

1. **BETA-020F:** Remover `error-handler.ts` antigo após completa migração
2. **BETA-026:** Completar Épico 4 - Eficiência por Transportadora
3. **BETA-028:** Completar Épico 6 - Relatório Diário
4. **BETA-029:** Completar Épico 10 - Dashboard Beta
5. **Cobertura:** Aumentar cobertura de testes frontend de 20.8% para 50%
6. **E2E:** Completar testes E2E com Playwright

---

**Assinatura:** Equipe Ilex Logística  
**Data:** 2026-06-24  
**Versão:** 2.0 (SDD + TDD)
