# CONTEXTO.md — Estado e Contexto do Projeto Ilex Logistica

**Atualizado em:** 2026-06-25

---

## Visao Geral Atual

Projeto de plataforma web para rastreio de entregas, gestao de excecoes operacionais e relatorios logisticos. Monorepo com API Python/FastAPI + frontend Next.js + infra Docker + documentacao extensa.

**Fase atual:** Branch `main` com BETA-020F e BETA-029 concluídos. Projeto em estado estável com 489 testes backend passando e 331 testes frontend passando.

**Atualizações recentes:**
- **2026-06-25:** BETA-Test-E2E-Completion completado — Habilitados 14 testes E2E (8 daily-report, 6 alerts), instaladas dependências faltantes (recharts, date-fns), adicionados 14 testes unitários para carriers/page.tsx. Cobertura de testes frontend: 63.82% (meta: 50% ✅).
- **2026-06-25:** BETA-029 completado — Completado Épico 10 (Dashboard Beta) com habilitação de 6 testes E2E. Layout responsivo, loading states, error handling e empty states já estavam implementados.
- **2026-06-25:** BETA-020F completado — Removido error-handler.ts e error-handler.test.ts legacy após completa migração para useApiErrorHandler.
- **2026-06-25:** BETA-020E completado — Testes E2E de navegação por permissão (7 testes) validando acesso por perfil (admin, logística, gestor, auditoria) nas 18 páginas integradas, redirecionamento 401 e exibição 403.
- **2026-06-25:** BETA-020D completado — Integração de tratamento de erros 401/403 em 18 páginas privadas do frontend usando hook `useApiErrorHandler`. 5 testes unitários do hook, 320 testes frontend passando.
- **2026-06-24:** BETA-020C completado — Frontend de Segurança e RBAC com tratamento de 401/403, helpers de permissões, sidebar condicional e componente AccessDenied. 30 novos testes frontend.
- **2026-06-17:** BETA-027 completado — Alertas e Notificações com `AlertDeliveryLog`, deduplicação por origem, geração de alertas para múltiplos tipos e integração com dashboard/exceções. 88 testes backend + 19 testes frontend.

---

## Estado dos Componentes

### Backend (`apps/api`)
- **Status:** Funcional, conflitos de merge RESOLVIDOS
- **Modulos prontos:** auth, users, carriers, shipments, imports (CSV/XLSX), sla, alerts, reports, dashboard
- **Migrations:** 11 versoes Alembic
- **Testes:** 489 testes passando, 0 falhando
- **Cobertura:** ~88% (declarado)

### Frontend (`apps/web`)
- **Status:** Build passando, RBAC integrado
- **Telas prontas:** login, carriers, shipments, shipments/import, exceptions, reports/daily, alerts, users (com RBAC), settings (parcial)
- **Testes:** Vitest unitario (331 testes passando) + Playwright E2E (alguns skipados)
- **Cobertura:** ~20.8%
- **RBAC:** Tratamento de 401/403 implementado, helpers de permissões, sidebar condicional, componente AccessDenied

### Infraestrutura
- **Docker Compose:** PostgreSQL + API container + healthchecks
- **CI/CD:** GitHub Actions workflow `beta-ci.yml` (conflitos resolvidos, CI deve funcionar)
- **Scripts:** beta_validate, validate_migrations, check_secrets, validate_docs

### Documentacao
- **~50+ documentos** em `docs/`
- **Conflitos de merge:** RESOLVIDOS em todos os documentos BETA_*.md

---

## Decisoes Arquiteturais Recentes

1. **Monorepo consolidado:** todos os modulos (api, web, infra, docs, scripts) unificados na raiz
2. **CI base unificado:** workflow `beta-ci.yml` na raiz orquestra validacoes
3. **Migrations testaveis:** testes de roundtrip (upgrade/downgrade) com Alembic
4. **Importacao assistida:** suporte a multiplos layouts de CSV/XLSX (incluindo Braspress) com preview e confirmacao

---

## Dependencias e Bloqueios

| Bloqueio | Severidade | Descricao |
|----------|-----------|-----------|
| ~~Conflitos de merge nao resolvidos~~ | ~~CRITICO~~ | **RESOLVIDO** em 2026-06-10 |
| ~~CI quebrado~~ | ~~CRITICO~~ | **RESOLVIDO** — workflow `beta-ci.yml` corrigido |
| ~~Documentacao ilegivel~~ | ~~ALTO~~ | **RESOLVIDO** — 6 documentos BETA_*.md limpos |
| ~~Build frontend com erros de tipo~~ | ~~MEDIO~~ | **RESOLVIDO** — tipos completos adicionados em `types.ts`, build passando |
| ~~PR #38 com conflitos~~ | ~~ALTO~~ | **MERGEADO** em 2026-06-10 |
| ~~PR #39 com base incorreta~~ | ~~ALTO~~ | **MERGEADO** em 2026-06-10 |
| Cobertura Web baixa | MEDIO | 20.8% — limita confianca no frontend |
| E2E incompletos | MEDIO | Testes skipados para telas nao implementadas |

---

## Proximos Passos Pendentes (Macro)

1. ~~Resolver todos os conflitos de merge nao resolvidos~~ **(FEITO 2026-06-10)**
2. ~~Corrigir e consolidar CI/CD na raiz~~ **(FEITO 2026-06-10)**
3. ~~Corrigir build do frontend — tipos incompletos em `types.ts`~~ **(FEITO 2026-06-10)**
4. ~~Rodar suite completa de testes e gerar novo relatorio de cobertura~~ **(FEITO — 489 passed, 0 failed)**
5. ~~Atualizar `BETA_FUNCTIONAL_EPIC_AUDIT.md`~~ **(FEITO 2026-06-10)**
6. ~~Revisar e mergear PR #38 (BETA-019B — Frontend de Auditoria)~~ **(MERGEADO 2026-06-10)**
7. ~~Revisar e mergear PR #39 (BETA-020A — Seguranca e RBAC)~~ **(MERGEADO 2026-06-10)**
8. ~~Implementar BETA-020B (RBAC operational endpoints)~~ **(FEITO)**
9. ~~Implementar BETA-020C (Frontend de Seguranca e RBAC)~~ **(FEITO 2026-06-24)**
10. ~~Implementar BETA-027 (Alertas e Notificacoes)~~ **(FEITO 2026-06-17)**
11. ~~Integrar tratamento de 401/403 em todas as páginas restantes (BETA-020D)** **(FEITO 2026-06-25)**
12. ~~Implementar testes E2E de navegação por permissão (BETA-020E)** **(FEITO 2026-06-25)**
13. ~~Remover `error-handler.ts` antigo após completa migração (BETA-020F)** **(FEITO 2026-06-25)**
14. ~~Completar Épico 10 - Dashboard Beta (BETA-029)** **(FEITO 2026-06-25)**
15. Implementar tela administrativa de usuarios completa (W15)
16. Implementar tela de auditoria de alteracoes (W18)
17. Desenvolver conectores de transportadoras (LOG-021/022)
18. Implementar envio de relatorio diario por e-mail (LOG-019)
19. Aumentar cobertura de testes E2E com Playwright

---

## Notas Tecnicas

- **Banco dev:** SQLite por padrao (`ilex.db`); PostgreSQL via Docker Compose para testes de integracao
- **Auth:** JWT com refresh token; secret de fallback hardcoded em dev (requer env var em prod)
- **RBAC:** 4 perfis (admin, logistica, gestor, auditoria)
- **Importacao:** Parser CSV/XLSX com validacao linha a linha, deteccao de duplicidade, layout Braspress

---

## Historico de Mudancas (Linha do Tempo)

### 2026-06-24 (Sessao de governanca)
- Atualizacao de CONTEXTO.md com estado atual do projeto
- BETA-020C (Frontend de Seguranca e RBAC) marcado como concluido
- BETA-027 (Alertas e Notificacoes) marcado como concluido
- Verificacao de estado: branch main limpo, testes backend passando
- Proximos passos priorizados: integracao 401/403, conectores, E2E

### 2026-06-17 (BETA-027 — Alertas e Notificacoes)
- Adicionado `AlertDeliveryLog` para registrar geração, leitura, resolução e duplicidades ignoradas
- Implementada geração de alertas para `sla_critical`, `sla_late`, `sla_warning`, `unknown_sla`, `no_update` e `import_failure`
- Corrigidos filtros de `sla_status` e `is_late` no painel de exceções
- Corrigido o `delay_days` do painel de exceções para usar o cálculo do SLA
- Ajustado o dashboard para contar falhas de importação e alertas ativos com dados reais
- Atualizado o frontend de alertas para expor o tipo `no_update`
- Backend validado: 88 passed
- Frontend validado: 19 passed
- Branch `feature/beta-027-alerts-notifications` preparado para PR

### 2026-06-10 (Continuacao — Correcao de PRs)
- Analise de PRs abertas: #38 (BETA-019B) e #39 (BETA-020A)
- PR #38: conflitos com `main` resolvidos via rebase manual (cherry-pick de 6 commits)
- PR #39: base alterada de `feature/beta-019b` para `main`, conflitos resolvidos via cherry-pick
- Resultado: ambas as PRs agora `mergeable` e prontas para revisao/merge

### 2026-06-10 (Continuacao — Merge das PRs)
- Merge squash da PR #38 (BETA-019B — Auditoria Operacional) para `main`
- Merge squash da PR #39 (BETA-020A — Seguranca e RBAC) para `main`
- Resolucao de conflitos durante merge da #39 (models.py, audit/router.py, BETA_NEXT_ACTIONS.md)
- Geracao de relatorio completo: `docs/RELATORIO_MERGE_PR38_PR39.md`
- Total de arquivos modificados: 47 (34 criados + 19 modificados)
- Novos modulos: audit (backend), RBAC/permissions (backend), tela de auditoria (frontend)

### 2026-06-08 a 2026-06-09
- Merge de 36 PRs beta na branch `main`
- Resolucao manual de conflitos em varios PRs durante merge
- Correcao do workflow de CI para instalar `apps/api[dev]`

### 2026-06-01
- Roadmap e relatorio de telas gerados
- BETA_FUNCTIONAL_EPIC_AUDIT.md criado

---

**Arquivo vivo — atualizar a cada sessao de trabalho**
