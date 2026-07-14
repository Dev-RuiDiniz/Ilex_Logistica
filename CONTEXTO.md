# CONTEXTO.md — Estado Vivo do Ilex Logística

<<<<<<< HEAD
**Atualizado em:** 2026-07-03
=======
**Atualizado em:** 2026-07-13 (auditoria completa de projeto)
>>>>>>> fix/infra-setup-local

## 2026-07-03 — Conclusão técnica de P1/P2

- Indicadores de listagem, dashboard e eficiência foram reconciliados por dataset controlado.
- Extravio explícito, população financeira válida e ranking determinístico foram formalizados.
- Testes vazios de exceções foram substituídos; fixture XLSX e specs E2E foram adicionadas.
- Senhas, expiração e rotação/revogação por versão foram endurecidas; políticas operacionais foram centralizadas.
- UAT técnico está em `docs/uat/P1_P2_UAT.md`; E2E integrado e aceite humano permanecem pendentes por ausência de API/seed no ambiente Playwright local.

<<<<<<< HEAD
## 2026-07-03 — Baseline técnico revalidado

- Ruff foi corrigido em migrations e seed de demonstração, incluindo a separação de imports corrompida em `migrations/env.py`.
- Os warnings do Web foram eliminados: callbacks possuem dependências explícitas, páginas privadas renderizam acesso negado e código morto foi removido.
- SPEC-04 e SPEC-08 deixaram de constar como bloqueadas no índice; filtros/busca estão confirmados e a homologação complementar de entregas/dashboard permanece pendente.
- Evidências frescas desta sessão foram registradas em `RELATORIO.md`.

## 2026-07-02 — Estabilização técnica do P0
=======
**Atualizações recentes:**
- **2026-06-18:** Login web local destravado no ambiente Docker com suporte de CORS no backend FastAPI. A API agora responde corretamente à preflight `OPTIONS` para origens locais do frontend (`localhost` e `127.0.0.1`, incluindo porta `3002`), eliminando o falso erro de credenciais inválidas no browser.
- **2026-06-18:** Normalização global de legibilidade textual aplicada ao frontend inteiro. O `web` recebeu reforço de contraste em subtítulos, labels, estados vazios, tabelas e telas legadas como `audit`, `exceptions`, `shipments/import`, `deliveries` e `settings/sla`, mantendo a base clara das superfícies.
- **2026-06-18:** Ajuste visual incremental aplicado ao frontend para remover o peso escuro das superfícies principais. `page-hero`, painéis, tabelas, cards e estados compartilhados ficaram mais claros, mantendo `header` e `sidebar` com a identidade premium escura.
- **2026-06-17:** Frontend redesenhado com a direcao visual "Excecoes com Inteligencia". O `web` agora possui design system proprio, login premium, shell privado com navegacao por dominio e padroes consistentes para dashboard, filtros, tabelas e formularios nas telas centrais.
- **2026-06-17:** Seed oficial de usuarios de desenvolvimento adicionado ao backend com script operacional em `scripts/seed_dev_users.py`, documentação registrada no README e migration incremental `20260627_02` para alinhar a coluna `roles.description` no PostgreSQL real da stack local.
- **2026-06-17:** Setup local da stack corrigido no monorepo atual. Infra ajustada para usar caminhos `apps/api` e `infra/...` no Docker build, entrypoint normalizado para evitar falha por CRLF em Windows e `infra/LOCAL_SETUP.md` alinhado ao layout real do repositório.
- **2026-06-17:** Bootstrap de migrations estabilizado para ambiente local. `apps/api/migrations/env.py` passou a priorizar a URL de banco em runtime, a árvore Alembic foi unificada em um único `head` com merge revision `20260627_01` e a migration `20260615_01` recebeu default booleano compatível com PostgreSQL.
- **2026-06-17:** Ambiente local validado com `db` e `api` saudáveis via Docker Compose, migrations em PostgreSQL real, frontend com `npm test` (391/391) e `npm run build` passando. Neste host específico, o PostgreSQL do Ilex foi exposto em `5433` e o frontend dev subiu em `3002` por conflito com portas já ocupadas por outros projetos.

Projeto de plataforma web para rastreio de entregas, gestao de excecoes operacionais e relatorios logisticos. Monorepo com API Python/FastAPI + frontend Next.js + infra Docker + documentacao extensa.

**Fase atual:** Auditoria completa realizada em 2026-07-13. **Backend 100% verde (655 testes)** após correção da suíte. **Frontend 100% verde (391 testes)**. Gates de CI (migrations, docs, secrets) verdes. Projeto em estado de release beta.
>>>>>>> fix/infra-setup-local

- Web confirmado com 393 testes, ESLint sem erros e build aprovado.
- API confirmou 664/664 testes em 72,52s, com SQLite em memória isolado e execução concorrente ao roundtrip Alembic.
- Contratos de entrega de alertas foram unificados entre model, migration, serviço e API; ausência de credencial agora responde `401` e falta de permissão responde `403`.
- Alembic possui uma única head e os testes de upgrade, downgrade e preservação de dados estão verdes.
- Testes de infraestrutura são importáveis pela raiz; workflows separados de API, Web e governança foram adicionados.
- A imagem da API não inclui mais o seed de demonstração e o template VPS não fixa endereço local como destino público.
- Gates locais e remotos do P0 estão verdes; a `main` exige os checks estritos `api`, `web` e `governance`, bloqueia force-push/exclusão e preserva bypass administrativo.

## 2026-07-02 — Auditoria completa e redefinição do encerramento

<<<<<<< HEAD
### Estado auditado

- Projeto classificado como MVP avançado em estabilização, não pronto para produção.
- Web: testes, lint e build vermelhos, incluindo erro de runtime na tela de envios.
- Banco: dois heads Alembic bloqueiam um caminho único de deploy.
- API: 659 testes coletados; execução completa requer diagnóstico de duração/isolamento.
- Infra/CI: testes não coletam pelo comando raiz e não há workflow ativo.
- Documentação e secret scan foram aprovados.

### Decisões
=======
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
- **Sistema visual:** design system proprietario com hero de pagina, surfaces, metric cards, data tables e formularios padronizados; conteudo principal ajustado para base mais clara nas superfícies centrais e com contraste textual reforçado no frontend inteiro
- **Testes:** Vitest unitario (391 testes passando) + Playwright E2E versionado
- **Cobertura:** ~20.8%
- **RBAC:** Tratamento de 401/403 implementado, helpers de permissões, sidebar condicional, componente AccessDenied

### Infraestrutura
- **Docker Compose:** PostgreSQL + API container + healthchecks, compatível com layout atual do monorepo
- **CI/CD:** GitHub Actions workflow `beta-ci.yml` (conflitos resolvidos, CI deve funcionar)
- **Scripts:** beta_validate, validate_migrations, check_secrets, validate_docs
>>>>>>> fix/infra-setup-local

- O README raiz passa a ser exclusivamente comercial/executivo; achados técnicos ficam em `AUDITORIA.md`.
- O marco de conclusão é o MVP assistido com cotação por CSV/XLSX, UAT e prontidão de produção.
- P0 do roadmap bloqueia novas funcionalidades até o baseline ficar verde.
- Integrações automáticas de ERP/transportadoras permanecem pós-MVP e dependentes de contratos.

### Próximos passos

Executar P0 na ordem: build/runtime Web, suíte/lint, migration única, API determinística, infra e CI.

### Execução P0

- Branches de governança e VPS foram consolidadas na `main`; branches paralelas locais e remotas foram removidas após confirmação de ancestralidade.
- O build Web voltou a passar após a consolidação.
- O dashboard foi restaurado ao contrato real com filtros e seus 26 testes voltaram ao baseline esperado.
- A suíte Web completa passou com 393 testes e o build Next.js foi aprovado; os erros ESLint foram eliminados, restando limpeza de avisos não bloqueantes.
- Alembic foi consolidado em uma única head; `alert_delivery_logs` agora possui schema coerente entre migration, model, service, rotas e testes.

## 2026-07-02 — Consolidação de governança

<<<<<<< HEAD
### Estado atual
=======
| Bloqueio | Severidade | Descricao |
|----------|-----------|-----------|
| ~~Conflitos de merge nao resolvidos~~ | ~~CRITICO~~ | **RESOLVIDO** em 2026-06-10 |
| ~~CI quebrado~~ | ~~CRITICO~~ | **RESOLVIDO** — workflow `beta-ci.yml` corrigido |
| ~~Documentacao ilegivel~~ | ~~ALTO~~ | **RESOLVIDO** — 6 documentos BETA_*.md limpos |
| ~~Build frontend com erros de tipo~~ | ~~MEDIO~~ | **RESOLVIDO** — tipos completos adicionados em `types.ts`, build passando |
| ~~PR #38 com conflitos~~ | ~~ALTO~~ | **MERGEADO** em 2026-06-10 |
| ~~PR #39 com base incorreta~~ | ~~ALTO~~ | **MERGEADO** em 2026-06-10 |
| Suite completa da API com regressões | RESOLVIDO | `python -m pytest tests` (2026-07-13, fim do dia): **655 passed, 0 failed**. Corrigido via: cache obsoleto limpo, `conftest` idempotente (roles), `reset_database` com `engine.dispose()`, fixture `_auth_admin` em testes de import, asserção 403→401, email consistente em `test_w15` |
| Porta 3000 ocupada no host atual | BAIXO | Frontend local precisou subir em `3002`; conflito é do ambiente e não da aplicação |
| ~~Login web local falhando por CORS~~ | ~~ALTO~~ | **RESOLVIDO em 2026-06-18** — preflight `OPTIONS` para `/api/v1/auth/login` passou a responder para origens locais permitidas |
>>>>>>> fix/infra-setup-local

- Monorepo com API FastAPI/SQLAlchemy/Alembic e Web Next.js/React.
- Domínios presentes: autenticação, usuários/RBAC, transportadoras, entregas/importações, envios/tratativas, SLA, dashboard, alertas, relatórios e auditoria.
- PostgreSQL 16 está configurado no Docker Compose; a configuração da aplicação também admite SQLite em desenvolvimento/testes.
- O Apêndice 1 foi incorporado como fonte de requisitos complementares.
- Os documentos raiz de arquitetura, banco, escopo, roadmap e relatório foram consolidados a partir do código atual.
- `ESCOPO.md` passou a consolidar o escopo completo e `docs/specs/` contém 12 especificações SDD por domínio, com índice e rastreabilidade LOG-027 a LOG-041.

### Decisões

<<<<<<< HEAD
- Código, migrations e testes prevalecem sobre alegações históricas de documentação.
- Requisitos do apêndice sem evidência ficam como planejados ou pendentes, nunca como concluídos.
- Cotação de frete por pedido será tratada como evolução separada, iniciando por importação assistida.
- Credenciais de ERP e transportadoras não serão persistidas em documentação ou frontend.
- `RELATORIO.md` substitui o arquivo histórico `RELATORIO_DIA.md` removido.
- Toda mudança funcional deve atualizar primeiro a spec do domínio e seus critérios de aceite antes do ciclo TDD.
- O `AGENTS.md` v3 tornou obrigatório o fluxo inspeção → SDD → TDD → validação → documentação → commit local, com push somente mediante autorização explícita.
- Instruções locais, como as regras de Next.js em `apps/web/AGENTS.md`, complementam a governança raiz sem reduzir seus gates.
=======
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
15. **CORRIGIR suíte de testes backend (BK-1)** — 104 falhas + 16 erros (4 causas raiz mapeadas em ROADMAP.md Apêndice de Auditoria)
16. Completar Épico 4 - Eficiência por Transportadora (ranking + percentuais)
17. Completar Épico 6 - Relatório Diário (geração manual + tela frontend + export)
18. Estabilizar Épico 8 - Braspress parser/mapper + UI de conectores
19. Implementar tela administrativa de usuarios completa (W15)
20. Implementar tela de auditoria de alteracoes (W18)
21. Desenvolver conectores de transportadoras (LOG-021/022)
22. Implementar envio de relatorio diario por e-mail (LOG-019)
23. Aumentar cobertura de testes E2E com Playwright e cobertura frontend para 50%
>>>>>>> fix/infra-setup-local

### Dependências e bloqueios

- Contrato, autenticação, campos e ambiente de homologação do ERP: **A CONFIRMAR**.
- APIs e tabelas negociadas das transportadoras: **A CONFIRMAR**.
- Regra operacional de SLA/no prazo/extravio: requer homologação do cliente.
- Aderência integral dos filtros e métricas financeiras do Apêndice 1: requer teste funcional ponta a ponta.

<<<<<<< HEAD
### Próximos passos
=======
- **Banco dev:** SQLite por padrao (`ilex.db`); PostgreSQL via Docker Compose para testes de integracao
- **Auth:** JWT com refresh token; secret de fallback hardcoded em dev (requer env var em prod)
- **RBAC:** 4 perfis (admin, logistica, gestor, auditoria)
- **Acessos seed locais:** admin, manager, operator, viewer, logistica, gestor e auditoria com senha padrao documentada
- **Importacao:** Parser CSV/XLSX com validacao linha a linha, deteccao de duplicidade, layout Braspress
- **UX frontend:** paleta clara com azul profundo/grafite, sem dark mode neste ciclo e sem alteracao de contratos do backend
>>>>>>> fix/infra-setup-local

1. Homologar LOG-027 a LOG-035 contra dados reais e fechar lacunas de filtros/indicadores.
2. Especificar contrato mínimo de pedidos do ERP (LOG-038).
3. Implementar o MVP assistido de cotação (LOG-036/037/039/040) via SDD e TDD.
4. Preservar e validar o fluxo Braspress sem credenciais (LOG-041).

## Histórico preservado

<<<<<<< HEAD
## 2026-07-03 — P3 pedidos ERP
=======
### 2026-06-18 (Ajuste claro das superfícies principais)
- Clareadas superfícies compartilhadas do frontend sem alterar header e sidebar
- Ajustado o showcase principal do login para composição mais luminosa
- Validação do frontend concluída com `npm test` e `npm run build`

### 2026-06-18 (Normalização global de contraste textual)
- Reforçados tokens e classes de texto do design system em `globals.css`
- Padronizada a legibilidade de labels, subtítulos, notas, tabelas e estados auxiliares
- Ajustadas telas antigas do frontend para convergir com a nova hierarquia de leitura
- Frontend validado novamente com `npm test` e `npm run build`

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
>>>>>>> fix/infra-setup-local

- SPEC-12 foi fixada com os contratos aprovados e permanece parcial.
- `orders`, `quote_rounds` e `freight_quotes` foram criados por migration reversível, com valores monetários decimais e constraints de identidade.
- A importação de pedidos aceita CSV/XLSX, valida erros por linha, não persiste domínio no preview e confirma por transação com idempotência por hash.
- O layout técnico está confirmado por fixtures sanitizadas; a homologação humana contra amostra do ERP continua pendente e não foi convertida em aceite.
- Rodadas incluem todas as transportadoras ativas e isolam resultados `pending`, `quoted`, `unavailable`, `error` e `expired`.
- A recomendação usa menor valor, menor prazo, maior eficiência observada em entregas concluídas e menor `carrier_id`; override exige justificativa e preserva a recomendação.
- Criação, registro/importação, conclusão e override geram auditoria operacional na mesma transação de domínio.
- A Web oferece listagem/importação de pedidos, detalhe com histórico e comparação de cotações em desktop/mobile, com estados de loading, vazio, erro e acesso negado.
- A matriz RBAC foi persistida por migration e testada em todas as rotas novas para respostas `401` e `403`.
- O fluxo P3 completo passou em Chromium, Firefox, WebKit e Mobile Chrome com API determinística interceptada; regras e contratos da API foram validados separadamente contra o banco de testes.
- A suíte Playwright histórica completa possui 304 cenários e excedeu dez minutos no ambiente local; ela permanece gate de P4 em ambiente semelhante à produção, sem ser tratada como aprovada.
- P4 rejeita configuração produtiva insegura e removeu o bypass de login Web que existia para desenvolvimento.
- Redis 7 suporta limites por IP/usuário; em produção sua indisponibilidade falha de forma segura. CORS usa exclusivamente `ILEX_CORS_ALLOWED_ORIGINS`.
- Tokens mantêm access de 15 minutos, refresh de sete dias e rotação por versão. O armazenamento Web continua sendo risco residual documentado para migração futura a cookie `HttpOnly`/BFF.
- O Compose produtivo fixa PostgreSQL 16.4, Redis 7.2 e Caddy 2.8; dados ficam em rede interna e somente o proxy publica portas.
- Scripts de backup/checksum/retenção, restore temporário, deploy e rollback foram implementados. A validação real foi tentada, mas o Docker Desktop não expunha o engine; PostgreSQL real e restore continuam bloqueios explícitos do gate P4.
- O gate local de preview + confirmação de 10 mil pedidos concluiu em 5,07 s com SQLite em memória. O runner HTTP reproduz 50 usuários e coleta p50/p95/p99, mas precisa ser executado na VPS/PostgreSQL para aprovar P4.
- Observabilidade produtiva inclui logs JSON/request ID, métricas HTTP e de pedidos/cotações, liveness/readiness, Prometheus e exporters em rede interna.
- Alertas cobrem API, 5xx, PostgreSQL, Redis, backlog de cotações e backup; runbooks cobrem os sete incidentes previstos. A ativação no VPS ainda não foi observada.
- Axe não encontrou violações sérias/críticas nas telas P3 após corrigir contraste do shell; o fluxo passou em Chrome, Firefox, WebKit e viewport móvel.
- Smoke read-only e E2E autenticado com escrita estão preparados e protegidos por variáveis explícitas. Sem VPS, DNS, TLS e credenciais descartáveis, a execução produtiva segue bloqueada.
- `npm audit fix` eliminou achados altos; restam dois moderados do PostCSS embarcado pelo Next.js, sem correção compatível indicada pelo npm.
- Roteiros UAT formais foram preparados para administrador, logística, gestor e auditoria. Todos permanecem `PENDENTE`; nenhuma assinatura ou aprovação foi simulada.
- Documentação de release candidata, implantação, treinamento, suporte e escalonamento foi preparada. A RC não foi tagueada/publicada porque P4 externo e UAT não passaram.
- `release_gate.py` falha fechado enquanto P4, UAT e decisão GO não possuem marcadores explícitos. O manifesto de `v1.0.0-rc.1` permanece `blocked`, sem tag/publicação/deploy.

<<<<<<< HEAD
### 2026-06-24 — Segurança e RBAC frontend
=======
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
>>>>>>> fix/infra-setup-local

Foi registrado tratamento de `401/403`, helpers de permissões, navegação condicional, componente `AccessDenied` e adaptação de páginas. O repositório atual contém testes de permissões, middleware, navegação e páginas privadas.

### 2026-06 — Beta operacional

O histórico Git e as migrations demonstram evolução incremental de fundação, imports, deliveries, shipments, campos fiscais, SLA, alertas, relatórios, auditoria e permissões. Documentos históricos detalhados foram removidos em 2026-07-02 por decisão explícita do usuário; as evidências permanentes continuam no Git.

## Notas técnicas

- Backend: Python >=3.11, FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, pytest.
- Frontend: Next.js 16, React 19, TypeScript 5, Tailwind 4, Vitest, Testing Library e Playwright.
- Validadores: `validate_docs.py`, `validate_migrations.py`, `check_secrets.py` e `beta_validate.py`.
- Não registrar números de testes como permanentes sem executar as suítes na mesma sessão.
