# CONTEXTO.md — Estado Vivo do Ilex Logística

**Atualizado em:** 2026-07-16

## 2026-07-16 — SPEC-13: Integração WhatsApp (MCP) e rotina de cobrança

- Implementada a rotina de cobrança de remessas atrasadas via MCP server de WhatsApp (LOG-042/043).
- Backend: `app/integrations/mcp_whatsapp.py` (cliente HTTP com retry 3x + degradação), `app/modules/shipments/cobranca_service.py` (seleção, escalonamento 1–3/4–7/>7 dias, idempotência 24h), `router.py` (`POST /api/v1/shipments/cobranca/run` com `require_permission("shipments:write")`+`("shipments:read")`), `scheduler.py` (APScheduler, cron `ILEX_COBRANCA_CRON`, default desligado).
- Canal `whatsapp` reutiliza `AlertDeliveryLog` (campo `channel` já livre); falha de MCP gera alerta interno `critical` e log `failed`.
- Frontend: `ChargeDispatchModal` em shipments e carriers; tipos `ChargeDispatchRequest/Response` e `dispatchCharge` em `api.ts`.
- Corrigido bug latente do `JsonFormatter` (observability) e validação de range movida para o router (HTTPException 422) para evitar serialização de `ValueError` no Starlette.
- Gates verdes: API 783 testes, ruff limpo, Web 421 testes + lint + build, migrations 1 head, secrets OK.
- SPEC-13 segue em "Implementado; UAT pendente".

## 2026-07-03 — Conclusão técnica de P1/P2

- Indicadores de listagem, dashboard e eficiência foram reconciliados por dataset controlado.
- Extravio explícito, população financeira válida e ranking determinístico foram formalizados.
- Testes vazios de exceções foram substituídos; fixture XLSX e specs E2E foram adicionadas.
- Senhas, expiração e rotação/revogação por versão foram endurecidas; políticas operacionais foram centralizadas.
- UAT técnico está em `docs/uat/P1_P2_UAT.md`; E2E integrado e aceite humano permanecem pendentes por ausência de API/seed no ambiente Playwright local.

## 2026-07-03 — Baseline técnico revalidado

- Ruff foi corrigido em migrations e seed de demonstração, incluindo a separação de imports corrompida em `migrations/env.py`.
- Os warnings do Web foram eliminados: callbacks possuem dependências explícitas, páginas privadas renderizam acesso negado e código morto foi removido.
- SPEC-04 e SPEC-08 deixaram de constar como bloqueadas no índice; filtros/busca estão confirmados e a homologação complementar de entregas/dashboard permanece pendente.
- Evidências frescas desta sessão foram registradas em `RELATORIO.md`.

## 2026-07-02 — Estabilização técnica do P0

- Web confirmado com 417 testes (46 arquivos), ESLint sem erros (0 erros, avisos não bloqueantes) e build aprovado (19 rotas).
- API confirmou 761 testes em 72,54s, com SQLite em memória isolado e execução concorrente ao roundtrip Alembic.
- Contratos de entrega de alertas foram unificados entre model, migration, serviço e API; ausência de credencial agora responde `401` e falta de permissão responde `403`.
- Alembic possui uma única head e os testes de upgrade, downgrade e preservação de dados estão verdes.
- Testes de infraestrutura são importáveis pela raiz; workflows separados de API, Web e governança foram adicionados.
- A imagem da API não inclui mais o seed de demonstração e o template VPS não fixa endereço local como destino público.
- Gates locais e remotos do P0 estão verdes; a `main` exige os checks estritos `api`, `web` e `governance`, bloqueia force-push/exclusão e preserva bypass administrativo.

## 2026-07-02 — Auditoria completa e redefinição do encerramento

### Estado auditado

- Projeto classificado como MVP avançado em estabilização, não pronto para produção.
- Web: testes, lint e build vermelhos, incluindo erro de runtime na tela de envios.
- Banco: dois heads Alembic bloqueiam um caminho único de deploy.
- API: 659 testes coletados; execução completa requer diagnóstico de duração/isolamento.
- Infra/CI: testes não coletam pelo comando raiz e não há workflow ativo.
- Documentação e secret scan foram aprovados.

### Decisões

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

### Estado atual

- Monorepo com API FastAPI/SQLAlchemy/Alembic e Web Next.js/React.
- Domínios presentes: autenticação, usuários/RBAC, transportadoras, entregas/importações, envios/tratativas, SLA, dashboard, alertas, relatórios e auditoria.
- PostgreSQL 16 está configurado no Docker Compose; a configuração da aplicação também admite SQLite em desenvolvimento/testes.
- O Apêndice 1 foi incorporado como fonte de requisitos complementares.
- Os documentos raiz de arquitetura, banco, escopo, roadmap e relatório foram consolidados a partir do código atual.
- `ESCOPO.md` passou a consolidar o escopo completo e `docs/specs/` contém 12 especificações SDD por domínio, com índice e rastreabilidade LOG-027 a LOG-041.

### Decisões

- Código, migrations e testes prevalecem sobre alegações históricas de documentação.
- Requisitos do apêndice sem evidência ficam como planejados ou pendentes, nunca como concluídos.
- Cotação de frete por pedido será tratada como evolução separada, iniciando por importação assistida.
- Credenciais de ERP e transportadoras não serão persistidas em documentação ou frontend.
- `RELATORIO.md` substitui o arquivo histórico `RELATORIO_DIA.md` removido.
- Toda mudança funcional deve atualizar primeiro a spec do domínio e seus critérios de aceite antes do ciclo TDD.
- O `AGENTS.md` v3 tornou obrigatório o fluxo inspeção → SDD → TDD → validação → documentação → commit local, com push somente mediante autorização explícita.
- Instruções locais, como as regras de Next.js em `apps/web/AGENTS.md`, complementam a governança raiz sem reduzir seus gates.

### Dependências e bloqueios

- Contrato, autenticação, campos e ambiente de homologação do ERP: **A CONFIRMAR**.
- APIs e tabelas negociadas das transportadoras: **A CONFIRMAR**.
- Regra operacional de SLA/no prazo/extravio: requer homologação do cliente.
- Aderência integral dos filtros e métricas financeiras do Apêndice 1: requer teste funcional ponta a ponta.

### Próximos passos

1. Homologar LOG-027 a LOG-035 contra dados reais e fechar lacunas de filtros/indicadores.
2. Especificar contrato mínimo de pedidos do ERP (LOG-038).
3. Implementar o MVP assistido de cotação (LOG-036/037/039/040) via SDD e TDD.
4. Preservar e validar o fluxo Braspress sem credenciais (LOG-041).

## Histórico preservado

## 2026-07-03 — P3 pedidos ERP

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

### 2026-06-24 — Segurança e RBAC frontend

Foi registrado tratamento de `401/403`, helpers de permissões, navegação condicional, componente `AccessDenied` e adaptação de páginas. O repositório atual contém testes de permissões, middleware, navegação e páginas privadas.

### 2026-06 — Beta operacional

O histórico Git e as migrations demonstram evolução incremental de fundação, imports, deliveries, shipments, campos fiscais, SLA, alertas, relatórios, auditoria e permissões. Documentos históricos detalhados foram removidos em 2026-07-02 por decisão explícita do usuário; as evidências permanentes continuam no Git.

## Notas técnicas

- Backend: Python >=3.11, FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, pytest.
- Frontend: Next.js 16, React 19, TypeScript 5, Tailwind 4, Vitest, Testing Library e Playwright.
- Validadores: `validate_docs.py`, `validate_migrations.py`, `check_secrets.py` e `beta_validate.py`.
- Não registrar números de testes como permanentes sem executar as suítes na mesma sessão.
