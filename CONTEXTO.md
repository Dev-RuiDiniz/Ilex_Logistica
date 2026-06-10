# CONTEXTO.md — Estado e Contexto do Projeto Ilex Logistica

**Atualizado em:** 2026-06-10

---

## Visao Geral Atual

Projeto de plataforma web para rastreio de entregas, gestao de excecoes operacionais e relatorios logisticos. Monorepo com API Python/FastAPI + frontend Next.js + infra Docker + documentacao extensa.

**Fase atual:** Pos-merge de 36 PRs beta. Conflitos de merge nao resolvidos identificados como problema critico.

---

## Estado dos Componentes

### Backend (`apps/api`)
- **Status:** Funcional, conflitos de merge RESOLVIDOS
- **Modulos prontos:** auth, users, carriers, shipments, imports (CSV/XLSX), sla, alerts, reports, dashboard
- **Migrations:** 11 versoes Alembic
- **Testes:** ~39 arquivos de teste pytest (testes criticos passando)
- **Cobertura:** ~88% (declarado)

### Frontend (`apps/web`)
- **Status:** Build com erros de tipo pendentes (BETA-018B mergeado sem tipos completos)
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
| Cobertura Web baixa | MEDIO | 20.8% — limita confianca no frontend |
| E2E incompletos | MEDIO | Testes skipados para telas nao implementadas |

---

## Proximos Passos Pendentes (Macro)

1. ~~Resolver todos os conflitos de merge nao resolvidos~~ **(FEITO 2026-06-10)**
2. ~~Corrigir e consolidar CI/CD na raiz~~ **(FEITO 2026-06-10)**
3. ~~Corrigir build do frontend — tipos incompletos em `types.ts`~~ **(FEITO 2026-06-10)**
4. ~~Rodar suite completa de testes e gerar novo relatorio de cobertura~~ **(FEITO — 489 passed, 0 failed)**
5. ~~Atualizar `BETA_FUNCTIONAL_EPIC_AUDIT.md`~~ **(FEITO 2026-06-10)**
6. Implementar tela administrativa de usuarios (W15)
7. Implementar tela de auditoria de alteracoes (W18)
8. Desenvolver conectores de transportadoras (LOG-021/022)
9. Implementar envio de relatorio diario por e-mail (LOG-019)

---

## Notas Tecnicas

- **Banco dev:** SQLite por padrao (`ilex.db`); PostgreSQL via Docker Compose para testes de integracao
- **Auth:** JWT com refresh token; secret de fallback hardcoded em dev (requer env var em prod)
- **RBAC:** 4 perfis (admin, logistica, gestor, auditoria)
- **Importacao:** Parser CSV/XLSX com validacao linha a linha, deteccao de duplicidade, layout Braspress

---

## Historico de Mudancas (Linha do Tempo)

### 2026-06-10
- Criacao de `AGENTS.md`, `CONTEXTO.md` e `RELATORIO_DIA.md`
- Auditoria completa do projeto gerada (`AUDITORIA.md`)
- Identificacao de 48 conflitos de merge nao resolvidos em 10 arquivos
- Merge de PR #36 (BETA-018B — Relatorio Diario Frontend) na main

### 2026-06-08 a 2026-06-09
- Merge de 36 PRs beta na branch `main`
- Resolucao manual de conflitos em varios PRs durante merge
- Correcao do workflow de CI para instalar `apps/api[dev]`

### 2026-06-01
- Roadmap e relatorio de telas gerados
- BETA_FUNCTIONAL_EPIC_AUDIT.md criado

---

**Arquivo vivo — atualizar a cada sessao de trabalho**
