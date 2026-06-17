# CONTEXTO.md — Estado e Contexto do Projeto Ilex Logistica

**Atualizado em:** 2026-06-17

---

## Visao Geral Atual

Projeto de plataforma web para rastreio de entregas, gestao de excecoes operacionais e relatorios logisticos. Monorepo com API Python/FastAPI + frontend Next.js + infra Docker + documentacao extensa.

**Fase atual:** Branch `feature/beta-027-alerts-notifications` com o Épico 5 (alertas e notificações) concluído localmente. Backend e frontend validados em 2026-06-17; PR pendente de abertura/revisão.

**Atualização 2026-06-17:** alertas passaram a registrar `AlertDeliveryLog`, deduplicar por origem e gerar `import_failure`/`no_update`; o dashboard usa contadores reais de alertas e falhas de importação.

---

## Estado dos Componentes

### Backend (`apps/api`)
- **Status:** Funcional, conflitos de merge RESOLVIDOS
- **Modulos prontos:** auth, users, carriers, shipments, imports (CSV/XLSX), sla, alerts, reports, dashboard
- **Migrations:** 11 versoes Alembic
- **Testes:** 489 testes passando, 0 falhando
- **Cobertura:** ~88% (declarado)

### Frontend (`apps/web`)
- **Status:** Build passando (tipos completos adicionados em `types.ts`)
- **Telas prontas:** login, carriers, shipments, shipments/import, exceptions, reports/daily, alerts, users (parcial), settings (parcial)
- **Testes:** Vitest unitario + Playwright E2E (alguns skipados)
- **Cobertura:** ~20.8%

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
8. Implementar BETA-020B (frontend de seguranca e RBAC)
9. Implementar tela administrativa de usuarios (W15)
10. Implementar tela de auditoria de alteracoes (W18)
11. Desenvolver conectores de transportadoras (LOG-021/022)
12. Implementar envio de relatorio diario por e-mail (LOG-019)

---

## Notas Tecnicas

- **Banco dev:** SQLite por padrao (`ilex.db`); PostgreSQL via Docker Compose para testes de integracao
- **Auth:** JWT com refresh token; secret de fallback hardcoded em dev (requer env var em prod)
- **RBAC:** 4 perfis (admin, logistica, gestor, auditoria)
- **Importacao:** Parser CSV/XLSX com validacao linha a linha, deteccao de duplicidade, layout Braspress

---

## Historico de Mudancas (Linha do Tempo)

### 2026-06-10 (Sessao completa)
- Criacao de `AGENTS.md`, `CONTEXTO.md` e `RELATORIO_DIA.md`
- Auditoria completa do projeto gerada (`AUDITORIA.md`)
- Identificacao e **resolucao** de 48 conflitos de merge nao resolvidos em 10 arquivos
- Merge de PR #36 (BETA-018B — Relatorio Diario Frontend) na main
- Correcao de build frontend: tipos completos adicionados em `types.ts`
- Correcao de 13 testes preexistentes (8 Braspress, 3 auth, 1 daily report, 1 logging)
- Reescrita do `README.md` com apresentacao comercial
- Atualizacao de `AUDITORIA.md` e `BETA_FUNCTIONAL_EPIC_AUDIT.md` com estado pos-merge
- Suite completa: **489 passed, 0 failed**

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
