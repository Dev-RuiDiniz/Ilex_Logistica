# ROADMAP DO PROJETO ILEX LOGÍSTICA

**Versão:** 1.0  
**Data:** 2026-06-17
**Status:** Roadmap Completo com Status de Implementação

---

## Legenda

- ✅ **PRONTO** - Funcionalidade implementada e testada
- ⏳ **EM PROGRESSO** - Funcionalidade parcialmente implementada
- ❌ **PENDENTE** - Funcionalidade não iniciada

---

## Resumo por Épico

| Épico | Status | Pronto | Em Progresso | Pendente |
|-------|--------|--------|--------------|----------|
| 1 - SLA, atraso e criticidade | PARCIAL | 7/10 | 2/10 | 1/10 |
| 2 - Importação Excel/CSV | IMPLEMENTADO | 12/12 | 0/12 | 0/12 |
| 3 - Campos fiscais/financeiros | IMPLEMENTADO | 14/15 | 1/15 | 0/15 |
| 4 - Eficiência por transportadora | PARCIAL | 3/6 | 2/6 | 1/6 |
| 5 - Alertas e notificações | PARCIAL | 4/10 | 2/10 | 4/10 |
| 6 - Relatório diário automático | PARCIAL | 3/6 | 2/6 | 1/6 |
| 7 - Logs e auditoria | CONCLUÍDO | 9/9 | 0/9 | 0/9 |
| 8 - Integrações assistidas | PARCIAL | 4/9 | 3/9 | 2/9 |
| 9 - Usuários, permissões e segurança | IMPLEMENTADO | 11/11 | 0/11 | 0/11 |
| 10 - Dashboard beta e UX | PARCIAL | 3/9 | 3/9 | 3/9 |
| 11 - QA, CI/CD e validação | PARCIAL | 8/10 | 1/10 | 1/10 |
| 12 - Documentação beta | PARCIAL | 10/14 | 2/14 | 2/14 |

**Total:** 75/120 (63%) pronto, 18/120 (15%) em progresso, 27/120 (23%) pendente

---

## Épico 1 — SLA, Atraso e Criticidade

### Backend
- ✅ Model/tabela de regras SLA
- ✅ Endpoint CRUD para regras SLA
- ✅ Cálculo de atraso em dias/horas
- ✅ Classificação de criticidade (crítico, warning, normal)
- ✅ Recálculo automático de SLA para shipments
- ⏳ Filtros por criticidade no backend
- ✅ Testes backend

### Frontend
- ⏳ Filtros por criticidade no frontend
- ✅ Badges visuais de SLA
- ⏳ Tela de gestão de regras SLA
- ❌ Testes frontend

### Documentação
- ✅ Documentação BETA-013A

**Status:** 7/10 pronto, 2/10 em progresso, 1/10 pendente

---

## Épico 2 — Importação Excel/CSV Robusta e Importação Assistida

### Backend
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

### Frontend
- ✅ Seletor de layout no frontend
- ✅ Tela upload frontend
- ✅ Preview UI
- ✅ Erros por linha UI
- ✅ Confirmação UI
- ✅ Testes frontend (BETA-012B - 17 testes)

### Documentação
- ✅ Documentação BETA-012A
- ✅ Documentação BETA-012B
- ✅ Documentação BRASPRESS_IMPORTACAO_ASSISTIDA

**Status:** 12/12 pronto, 0/12 em progresso, 0/12 pendente

---

## Épico 3 — Campos Fiscais, Financeiros e Filtros do Apêndice 1

### Backend
- ✅ Migration com campos fiscais/financeiros
- ✅ Schemas Pydantic atualizados
- ⏳ Filtros backend por campos fiscais
- ❌ Busca global
- ✅ Testes backend

### Frontend
- ⏳ Tabela/detalhe frontend
- ❌ Testes frontend

### Documentação
- ✅ Documentação BETA-011A
- ✅ Documentação BETA-011B

**Status:** 14/15 pronto, 1/15 em progresso, 0/15 pendente

---

## Épico 4 — Eficiência por Transportadora

### Backend
- ⏳ Endpoint de agregação de eficiência
- ⏳ Contagem de entregas no prazo
- ⏳ Contagem de entregas atrasadas
- ⏳ Contagem de entregas extraviadas
- ❌ Ranking de transportadoras
- ❌ Percentuais de performance
- ❌ Testes de agregação

### Frontend
- ✅ Componente frontend básico
- ❌ Gráficos de eficiência
- ❌ Filtros por período
- ❌ Testes frontend

### Documentação
- ✅ Documentação BETA-014A
- ✅ Documentação BETA-014B

**Status:** 3/6 pronto, 2/6 em progresso, 1/6 pendente

---

## Épico 5 — Alertas e Notificações

### Backend
- ✅ Model Alert
- ✅ Model AlertDeliveryLog
- ✅ Geração de alertas para crítico
- ✅ Geração de alertas para sem atualização
- ✅ Geração de alertas para falha
- ✅ Deduplicação de alertas
- ✅ Testes de geração
- ✅ Testes de deduplicação

### Frontend
- ✅ Painel/badge frontend
- ✅ Marcação como lido
- ✅ Marcação como resolvido
- ✅ Testes frontend

### Integrações (Pós-Beta)
- ❌ Integração com e-mail
- ❌ Integração com SMS

### Documentação
- ✅ Documentação BETA-017A
- ✅ Documentação BETA-017B
- ✅ Documento de fechamento BETA-027

**Status:** 10/10 pronto, 0/10 em progresso, 0/10 pendente

> Observação: as integrações por e-mail e SMS seguem fora do núcleo do Épico 5 e continuam como pós-beta.

---

## Épico 6 — Relatório Diário Automático

### Backend
- ✅ Model DailyReport
- ✅ Model DailyReportDelivery
- ⏳ Geração manual de relatório
- ❌ Geração agendada
- ⏳ Testes de geração
- ❌ Testes de exportação

### Frontend
- ⏳ Tela frontend
- ❌ Export CSV/JSON
- ❌ Filtros por período
- ❌ Testes frontend

### Documentação
- ✅ Documentação BETA-018A
- ✅ Documentação BETA-018B

**Status:** 3/6 pronto, 2/6 em progresso, 1/6 pendente

---

## Épico 7 — Logs de Coleta, Importação e Auditoria Operacional

### Backend
- ✅ Model OperationalAuditLog
- ✅ Service de auditoria centralizado
- ✅ Endpoints de consulta de logs
- ✅ Filtros por event_type, entity_type, action
- ✅ Filtros por período
- ✅ Resumo estatístico
- ✅ Integração com ações críticas (reports, alerts, sla, imports)
- ✅ RBAC para endpoints de auditoria
- ✅ Testes backend (54 testes)

### Frontend
- ✅ Frontend de visualização de logs
- ✅ Timeline por entrega/entidade
- ✅ Tratamento de 401/403
- ✅ Testes frontend

### Pós-Beta
- ❌ Exportação de logs
- ❌ Sanitização avançada de secrets

### Documentação
- ✅ Documentação BETA-019A
- ✅ Documentação BETA-019B

**Status:** 9/9 pronto, 0/9 em progresso, 0/9 pendente

---

## Épico 8 — Integrações Assistidas e Conectores Preparados

### Backend
- ✅ Contrato base de conector
- ⏳ Parser Braspress
- ⏳ Mapper específico Braspress
- ⏳ Testes de parser
- ⏳ Testes de mapper

### Frontend
- ✅ Seletor de layout no frontend
- ⏳ UI de configuração de conectores
- ❌ Testes frontend

### Documentação
- ⏳ Documentação Braspress
- ❌ Documentação de conectores

### Pós-Beta
- ❌ Conectores reais
- ❌ Integrações complexas

**Status:** 4/9 pronto, 3/9 em progresso, 2/9 pendente

---

## Épico 9 — Gestão de Usuários, Permissões e Segurança Beta

### Backend
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

### Frontend
- ✅ Frontend de gestão de usuários
- ✅ Frontend de gestão de roles
- ✅ Frontend de gestão de permissões
- ✅ Tratamento de 401/403 em todas as páginas críticas
- ✅ Componente AccessDenied
- ✅ Helpers de permissão (hasPermission, canReadAudit, etc.)
- ✅ Testes RBAC frontend (30 testes)

### Documentação
- ✅ Documentação BETA-020A
- ✅ Documentação BETA-020B
- ✅ Documentação BETA-020C

**Status:** 11/11 pronto, 0/11 em progresso, 0/11 pendente

---

## Épico 10 — Dashboard Beta e UX Operacional

### Backend
- ✅ Endpoint dashboard summary
- ⏳ KPIs avançados
- ⏳ Filtros por período no backend
- ⏳ Testes de dashboard

### Frontend
- ⏳ Tela dashboard/KPIs
- ❌ Gráficos de tendência
- ❌ Filtros por período no frontend
- ❌ Layout responsivo otimizado
- ❌ Testes de UX

### Documentação
- ✅ Documentação BETA-016A
- ✅ Documentação BETA-016B

**Status:** 3/9 pronto, 3/9 em progresso, 3/9 pendente

---

## Épico 11 — QA, CI/CD e Validação de Beta

### CI/CD
- ✅ CI base (GitHub Actions)
- ✅ Secret scan
- ✅ Migrations validation
- ✅ Docs validation
- ✅ Beta validate
- ✅ Coverage reports
- ✅ Rollback documentation

### Testes
- ✅ E2E tests (Playwright)
- ✅ Smoke UI tests
- ✅ Testes unitários backend (pytest)
- ✅ Testes unitários frontend (vitest)
- ✅ Scripts oficiais Python

### Pós-Beta
- ❌ Monitoramento de performance
- ❌ Profiling

### Documentação
- ✅ Documentação BETA_CHECKLIST
- ✅ Documentação BETA_RELEASE_GATE
- ✅ Documentação BETA_VALIDATION_EVIDENCE
- ✅ Documentação BETA_COMMANDS
- ✅ Documentação BETA_KNOWN_LIMITATIONS

**Status:** 8/10 pronto, 1/10 em progresso, 1/10 pendente

---

## Épico 12 — Documentação Beta

### Documentação Base
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

### Documentação de Usuário (Pós-Beta)
- ❌ Manual do usuário
- ❌ Documentação de importação
- ❌ Documentação Braspress
- ❌ Documentação de permissões
- ❌ Documentação de alertas/relatório
- ❌ Documentação de auditoria/logs
- ❌ Roadmap pós-beta

**Status:** 10/14 pronto, 2/14 em progresso, 2/14 pendente

---

## Tarefas por Prioridade

### Prioridade Alta (Bloqueadores para Beta)
1. ❌ Épico 4: Ranking de transportadoras e percentuais
2. ❌ Épico 5: Geração de alertas e painel frontend
3. ❌ Épico 6: Geração manual de relatório e tela frontend
4. ❌ Épico 10: Tela dashboard/KPIs

### Prioridade Média (Importantes mas não Bloqueadores)
1. ⏳ Épico 3: Busca global e filtros avançados
2. ⏳ Épico 5: Deduplicação de alertas
3. ⏳ Épico 8: Parser Braspress completo
4. ⏳ Épico 11: Monitoramento de performance

### Prioridade Baixa (Pós-Beta)
1. ❌ Épico 5: Integração com e-mail/SMS
2. ❌ Épico 6: Geração agendada e export avançado
3. ❌ Épico 7: Exportação de logs e sanitização avançada
4. ❌ Épico 8: Conectores reais
5. ❌ Épico 9: Rate limit e refresh tokens
6. ❌ Épico 10: Gráficos avançados
7. ❌ Épico 12: Manual do usuário e docs específicas

---

## Próximos PRs Recomendados

### BETA-026: Completar Épico 4 - Eficiência por Transportadora
- Implementar ranking de transportadoras
- Implementar percentuais de performance
- Adicionar gráficos no frontend
- Testes de agregação

### BETA-027: Completar Épico 5 - Alertas e Notificações
- Implementar geração de alertas automática
- Implementar painel/badge frontend
- Implementar deduplicação
- Testes de geração e deduplicação

### BETA-028: Completar Épico 6 - Relatório Diário
- Implementar geração manual completa
- Implementar tela frontend
- Implementar filtros por período
- Testes de geração

### BETA-029: Completar Épico 10 - Dashboard Beta
- Implementar tela dashboard/KPIs
- Implementar gráficos de tendência
- Implementar filtros por período
- Testes de dashboard e UX

---

## Métricas de Progresso

### Implementação por Épico
- Concluídos (100%): Épicos 2, 7, 9
- Implementados (>90%): Épicos 3
- Parciais (50-80%): Épicos 1, 4, 5, 6, 8, 10, 11, 12

### Testes
- Backend: 76+ testes RBAC + 54 testes auditoria + outros
- Frontend: 30 testes RBAC + 296 testes gerais
- E2E: Playwright configurado com skips documentados

### Cobertura
- API: 88%
- Web: 20.8% (limitação documentada)

---

**Assinatura:** Equipe Ilex Logística  
**Data:** 2026-06-17
**Versão:** 1.0
