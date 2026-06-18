# CONTEXTO.md — Estado e Contexto do Projeto Ilex Logistica

**Atualizado em:** 2026-06-17

---

## Visao Geral Atual

**Atualizações recentes:**
- **2026-06-18:** Ajuste visual incremental aplicado ao frontend para remover o peso escuro das superfícies principais. `page-hero`, painéis, tabelas, cards e estados compartilhados ficaram mais claros, mantendo `header` e `sidebar` com a identidade premium escura.
- **2026-06-17:** Frontend redesenhado com a direcao visual "Excecoes com Inteligencia". O `web` agora possui design system proprio, login premium, shell privado com navegacao por dominio e padroes consistentes para dashboard, filtros, tabelas e formularios nas telas centrais.
- **2026-06-17:** Seed oficial de usuarios de desenvolvimento adicionado ao backend com script operacional em `scripts/seed_dev_users.py`, documentação registrada no README e migration incremental `20260627_02` para alinhar a coluna `roles.description` no PostgreSQL real da stack local.
- **2026-06-17:** Setup local da stack corrigido no monorepo atual. Infra ajustada para usar caminhos `apps/api` e `infra/...` no Docker build, entrypoint normalizado para evitar falha por CRLF em Windows e `infra/LOCAL_SETUP.md` alinhado ao layout real do repositório.
- **2026-06-17:** Bootstrap de migrations estabilizado para ambiente local. `apps/api/migrations/env.py` passou a priorizar a URL de banco em runtime, a árvore Alembic foi unificada em um único `head` com merge revision `20260627_01` e a migration `20260615_01` recebeu default booleano compatível com PostgreSQL.
- **2026-06-17:** Ambiente local validado com `db` e `api` saudáveis via Docker Compose, migrations em PostgreSQL real, frontend com `npm test` (391/391) e `npm run build` passando. Neste host específico, o PostgreSQL do Ilex foi exposto em `5433` e o frontend dev subiu em `3002` por conflito com portas já ocupadas por outros projetos.

Projeto de plataforma web para rastreio de entregas, gestao de excecoes operacionais e relatorios logisticos. Monorepo com API Python/FastAPI + frontend Next.js + infra Docker + documentacao extensa.

**Fase atual:** Branch `fix/infra-setup-local` com stack local funcional para `db` + `api` + `web`, frontend premium consolidado nas telas centrais e regressões existentes apenas na suíte completa da API fora do escopo de bootstrap local.

---

## Estado dos Componentes

### Backend (`apps/api`)
- **Status:** API sobe localmente via Docker, com migrations aplicadas em PostgreSQL
- **Modulos prontos:** auth, users, carriers, shipments, imports (CSV/XLSX), sla, alerts, reports, dashboard
- **Migrations:** 11 versoes Alembic
- **Seeds operacionais:** usuarios de desenvolvimento/homologacao padronizados e idempotentes
- **Testes:** validações de migrations passando; suíte completa atual tem regressões fora do escopo de setup local
- **Cobertura:** ~88% (declarado)

### Frontend (`apps/web`)
- **Status:** Build passando, frontend dev validado em porta alternativa quando `3000` estiver ocupada
- **Telas prontas:** login, carriers, shipments, shipments/import, exceptions, reports/daily, alerts, users (com RBAC), settings (parcial)
- **Sistema visual:** design system proprietario com hero de pagina, surfaces, metric cards, data tables e formularios padronizados; conteudo principal ajustado para base mais clara nas superfícies centrais
- **Testes:** Vitest unitario (391 testes passando) + Playwright E2E versionado
- **Cobertura:** ~20.8%
- **RBAC:** Tratamento de 401/403 implementado, helpers de permissões, sidebar condicional, componente AccessDenied

### Infraestrutura
- **Docker Compose:** PostgreSQL + API container + healthchecks, compatível com layout atual do monorepo
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
| Suite completa da API com regressões | ALTO | `python -m pytest -q` ainda falha em testes antigos de `AlertDeliveryLog`, imports e expectativas de autenticação, apesar do bootstrap local estar funcional |
| Porta 3000 ocupada no host atual | BAIXO | Frontend local precisou subir em `3002`; conflito é do ambiente e não da aplicação |

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
- **Acessos seed locais:** admin, manager, operator, viewer, logistica, gestor e auditoria com senha padrao documentada
- **Importacao:** Parser CSV/XLSX com validacao linha a linha, deteccao de duplicidade, layout Braspress
- **UX frontend:** paleta clara com azul profundo/grafite, sem dark mode neste ciclo e sem alteracao de contratos do backend

---

## Historico de Mudancas (Linha do Tempo)

### 2026-06-18 (Ajuste claro das superfícies principais)
- Clareadas superfícies compartilhadas do frontend sem alterar header e sidebar
- Ajustado o showcase principal do login para composição mais luminosa
- Validação do frontend concluída com `npm test` e `npm run build`

### 2026-06-17 (BETA-030 - Redesign premium do frontend)
- Criado design system visual proprio do `web` em `globals.css`
- Redesenhados login, `AppShell`, dashboard e telas operacionais centrais
- Padronizados botoes, formularios, filtros, metricas, tabelas e estados visuais
- Suite `npm test` do frontend validada com 391/391 testes passando
- Build de producao do `web` validado com sucesso

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

### 2026-06-17 (Seeds de usuarios e README comercial)
- Criado seed idempotente de usuarios locais em `apps/api/app/modules/users/seed_dev_users.py`
- Criado script `scripts/seed_dev_users.py` com leitura automatica de `infra/.env`
- Registrados 7 usuarios padrao para desenvolvimento e homologacao local
- Adicionada migration `20260627_02_add_role_description.py` para alinhar schema real do Postgres com o modelo `Role`
- README reestruturado com posicionamento comercial, fluxo operacional da plataforma e acessos de teste

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
