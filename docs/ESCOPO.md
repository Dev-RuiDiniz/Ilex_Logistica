# ESCOPO DO PROJETO ILEX LOGÍSTICA

**Versão:** 1.0  
**Data:** 2026-06-11  
**Status:** Referência Absoluta do Projeto

---

## Visão Geral

O projeto Ilex Logística é um sistema de gestão logística para rastreamento de entregas, gestão de transportadoras, alertas operacionais e relatórios diários. Este documento define o escopo absoluto do projeto para fase beta.

---

## Objetivos do Projeto

1. **Rastreamento de Entregas:** Monitorar status de shipments em tempo real
2. **Gestão de Transportadoras:** Avaliar eficiência e performance por transportadora
3. **Alertas Operacionais:** Notificar sobre atrasos, exceções e problemas críticos
4. **Relatórios Diários:** Gerar relatórios operacionais automáticos
5. **Importação de Dados:** Importar dados de Excel/CSV de forma robusta
6. **Segurança e Permissões:** Controle de acesso baseado em roles (RBAC)
7. **Auditoria:** Logs operacionais completos de todas as ações

---

## Arquitetura

### Backend (Python/FastAPI)
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **Migrations:** Alembic
- **Autenticação:** JWT
- **Testes:** pytest

### Frontend (Next.js/TypeScript)
- **Framework:** Next.js 14 (App Router)
- **UI:** TailwindCSS + shadcn/ui
- **Testes:** Vitest + Playwright
- **Estado:** React Hooks

### CI/CD
- **Plataforma:** GitHub Actions
- **Validações:** Secret scan, migrations, testes automatizados
- **Scripts:** Python oficial para máxima portabilidade

---

## 12 Épicos do Roadmap Beta

### Épico 1 — SLA, Atraso e Criticidade

**Objetivo:** Implementar cálculo de SLA, detecção de atrasos e classificação de criticidade.

**Funcionalidades:**
- Model/tabela de regras SLA
- Endpoint CRUD para regras SLA
- Cálculo de atraso em dias/horas
- Classificação de criticidade (crítico, warning, normal)
- Recálculo automático de SLA para shipments
- Filtros por criticidade no frontend
- Badges visuais de SLA
- Tela de gestão de regras SLA

**Status Atual:** PARCIAL (70% implementado)

---

### Épico 2 — Importação Excel/CSV Robusta e Importação Assistida

**Objetivo:** Importar dados de Excel/CSV de forma robusta com validação linha a linha e layout assistido.

**Funcionalidades:**
- Parser CSV robusto
- Parser XLSX robusto
- Validação linha a linha
- Detecção de duplicidade
- Preview antes de confirmação
- Confirmação de importação
- Erros por linha detalhados
- Layout mapper preparado para Braspress
- Layout Braspress assistido beta
- Mapper específico Braspress
- Seletor de layout no frontend
- Tela upload frontend
- Preview UI
- Erros por linha UI
- Confirmação UI

**Status Atual:** IMPLEMENTADO (100%)

---

### Épico 3 — Campos Fiscais, Financeiros e Filtros do Apêndice 1

**Objetivo:** Adicionar campos fiscais e financeiros conforme Apêndice 1 com filtros avançados.

**Funcionalidades:**
- Migration com campos fiscais/financeiros
- Schemas Pydantic atualizados
- Filtros backend por campos fiscais
- Busca global
- Tabela/detalhe frontend
- Testes backend
- Testes frontend
- Documentação

**Status Atual:** IMPLEMENTADO (93%)

---

### Épico 4 — Eficiência por Transportadora

**Objetivo:** Calcular e exibir métricas de eficiência por transportadora.

**Funcionalidades:**
- Endpoint de agregação de eficiência
- Contagem de entregas no prazo
- Contagem de entregas atrasadas
- Contagem de entregas extraviadas
- Ranking de transportadoras
- Percentuais de performance
- Componente frontend com gráficos
- Filtros por período
- Testes de agregação
- Documentação

**Status Atual:** PARCIAL (50%)

---

### Épico 5 — Alertas e Notificações

**Objetivo:** Gerar alertas automáticos para eventos críticos e exibir painel de notificações.

**Funcionalidades:**
- Model Alert
- Model AlertDeliveryLog
- Geração de alertas para crítico
- Geração de alertas para sem atualização
- Geração de alertas para falha
- Deduplicação de alertas
- Painel/badge frontend
- Marcação como lido
- Marcação como resolvido
- Integração com e-mail (pós-beta)
- Integração com SMS (pós-beta)
- Testes de geração
- Testes de deduplicação

**Status Atual:** PARCIAL (40%)

---

### Épico 6 — Relatório Diário Automático

**Objetivo:** Gerar relatórios diários automáticos com KPIs operacionais.

**Funcionalidades:**
- Model DailyReport
- Model DailyReportDelivery
- Geração manual de relatório
- Geração agendada (pós-beta)
- Tela frontend
- Export CSV/JSON (pós-beta)
- Filtros por período
- KPIs: total shipments, entregas no prazo, atrasos, etc.
- Testes de geração
- Testes de exportação

**Status Atual:** PARCIAL (50%)

---

### Épico 7 — Logs de Coleta, Importação e Auditoria Operacional

**Objetivo:** Implementar logs estruturados para rastreamento de ações operacionais.

**Funcionalidades:**
- Model OperationalAuditLog
- Service de auditoria centralizado
- Endpoints de consulta de logs
- Filtros por event_type, entity_type, action
- Filtros por período
- Resumo estatístico
- Integração com ações críticas (reports, alerts, sla, imports)
- RBAC para endpoints de auditoria
- Frontend de visualização de logs
- Timeline por entrega/entidade
- Exportação de logs (pós-beta)
- Sanitização avançada de secrets (pós-beta)

**Status Atual:** CONCLUÍDO (100%)

---

### Épico 8 — Integrações Assistidas e Conectores Preparados

**Objetivo:** Preparar conectores para integrações assistidas com transportadoras.

**Funcionalidades:**
- Contrato base de conector
- Parser Braspress
- Documentação Braspress
- Mapper específico Braspress
- Seletor de layout no frontend
- Testes de parser
- Testes de mapper
- Conectores reais (pós-beta)
- Integrações complexas (pós-beta)

**Status Atual:** PARCIAL (44%)

---

### Épico 9 — Gestão de Usuários, Permissões e Segurança Beta

**Objetivo:** Implementar controle de acesso baseado em roles (RBAC) e segurança.

**Funcionalidades:**
- Model User (já existente)
- Model Role (já existente)
- Model Permission (novo)
- Tabela role_permissions (nova)
- Hash de senha com bcrypt
- Autenticação JWT
- Refresh tokens (pós-beta)
- Rate limit (pós-beta)
- RBAC por endpoint
- RBAC por tela
- Helpers de permissão (require_permission)
- Matriz de roles beta (admin, manager, operator, viewer, logistica, gestor, auditoria)
- Permissões granulares (shipments:read, imports:write, etc.)
- Proteção de endpoints críticos (audit, reports, alerts, SLA)
- Frontend de gestão de usuários
- Frontend de gestão de roles
- Frontend de gestão de permissões
- Tratamento de 401/403 no frontend
- Componente AccessDenied
- Testes RBAC backend
- Testes RBAC frontend

**Status Atual:** IMPLEMENTADO (100%)

---

### Épico 10 — Dashboard Beta e UX Operacional

**Objetivo:** Criar dashboard beta com KPIs operacionais e UX otimizada.

**Funcionalidades:**
- Endpoint dashboard summary
- KPIs: total shipments, entregas no prazo, atrasos, alertas ativos
- Tela dashboard/KPIs
- Gráficos de tendência (pós-beta)
- Filtros por período
- Layout responsivo
- UX otimizada para operações
- Testes de dashboard
- Testes de UX

**Status Atual:** PARCIAL (33%)

---

### Épico 11 — QA, CI/CD e Validação de Beta

**Objetivo:** Implementar infraestrutura de QA, CI/CD e validação automatizada.

**Funcionalidades:**
- CI base (GitHub Actions)
- Secret scan
- Migrations validation
- Docs validation
- Beta validate
- Coverage reports
- Rollback documentation
- E2E tests (Playwright)
- Smoke UI tests
- Testes unitários backend
- Testes unitários frontend
- Scripts oficiais Python
- Monitoramento de performance (pós-beta)

**Status Atual:** PARCIAL (80%)

---

### Épico 12 — Documentação Beta

**Objetivo:** Documentar completamente o sistema para fase beta.

**Funcionalidades:**
- README principal
- README API
- README Web
- Documentação beta (BETA_*.md)
- Checklist beta
- Comandos oficiais
- Gates de release
- Limitações conhecidas
- Próximas ações
- Manual do usuário (pós-beta)
- Documentação de importação (pós-beta)
- Documentação Braspress (pós-beta)
- Documentação de permissões (pós-beta)
- Documentação de alertas/relatório (pós-beta)
- Documentação de auditoria/logs (pós-beta)
- Roadmap pós-beta (pós-beta)

**Status Atual:** PARCIAL (71%)

---

## Tecnologias

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- Alembic
- Pydantic V2
- Pytest
- PostgreSQL

### Frontend
- Node.js 20
- Next.js 14 (App Router)
- TypeScript 5
- TailwindCSS
- shadcn/ui
- Vitest
- Playwright
- React 18

### DevOps
- GitHub Actions
- Git
- Docker (pós-beta)

---

## Limitações Conhecidas

### Cobertura de Testes
- Web coverage: 20.8% (baixa)
- lib/api.ts com baixa cobertura
- login/page.tsx com baixa cobertura

### Migrations
- Downgrade para base destrói dados por design
- Não há validação de preservação real de dados

### E2E
- Testes marcados como skip para UI não implementada
- Autenticação mockada (localStorage)
- Dados de teste mockados

### Segurança
- Rate limit não implementado
- Refresh tokens não implementados
- Sanitização avançada de secrets não implementada

### Performance
- Monitoramento de performance não implementado
- Profiling não implementado

### Acessibilidade
- Acessibilidade não implementada
- Contraste não validado
- Navegação por teclado não implementada

### Internacionalização
- i18n não implementado
- Suporte a múltiplos idiomas não implementado

---

## Próximos Passos

### Prioridade Alta
1. Completar Épico 4 (Eficiência) - ranking/percentuais
2. Completar Épico 5 (Alertas) - geração de alertas e painel
3. Completar Épico 6 (Relatório Diário) - geração manual
4. Completar Épico 10 (Dashboard) - tela dashboard/KPIs

### Prioridade Média
1. Aumentar cobertura de testes frontend
2. Implementar monitoramento de performance
3. Implementar acessibilidade básica

### Prioridade Baixa
1. Implementar internacionalização
2. Implementar rate limit
3. Implementar refresh tokens

---

**Assinatura:** Equipe Ilex Logística  
**Data:** 2026-06-11  
**Versão:** 1.0
