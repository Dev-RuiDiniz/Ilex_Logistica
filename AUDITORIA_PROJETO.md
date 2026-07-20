# AUDITORIA_PROJETO.md — Ilex Logística

**Data da auditoria:** 2026-07-20
**Auditor:** Rui Diniz
**Base de evidência:** execução real de gates + inspeção de código (não declarações da equipe)
**Método:** inspeção de código + execução de gates reais (não declarações da equipe)
**Restrições respeitadas:** não apagar arquivos, não alterar regras de negócio, não rodar migrations destrutivas, não usar credenciais reais, não fazer commit.

---

## 1. Resumo executivo

O Ilex Logística é um monorepo (FastAPI + Next.js) com MVP assistido de monitoramento de entregas e cotação de frete por CSV/XLSX. A base técnica está **verde e ampla**: 783 testes API, 421 testes Web, lint/build limpos, 21 migrations com única head, CI presente e secret scan OK. Contudo, o projeto **não está pronto para produção**: UAT não executado, canais externos de alerta não conectados, backup/PostgreSQL real não validado e regra de SLA final não homologada. Documentação (README/ESCOPO) marca muitos itens como "confirmado" de forma otimista.

**Classificação:** Beta / Homologação. **Nível de risco:** médio-alto.

## 2. Descrição do projeto

Plataforma web que centraliza entregas de múltiplas transportadoras, importa dados (CSV/XLSX/Braspress), calcula SLA/criticidade, registra tratativas, gera alertas/relatórios e controla acesso por perfil. Evolução: cotação de frete por pedido (MVP assistido) e cobrança WhatsApp de remessas atrasadas.

## 3. Stack identificada

- **API:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, JWT (PyJWT), bcrypt, Redis (rate limit), APScheduler, httpx.
- **Web:** Next.js 16 App Router, React 19, TypeScript 5, Tailwind 4, Vitest, Testing Library, Playwright.
- **Banco:** PostgreSQL 16 (Docker), SQLite (dev/testes).
- **Infra:** Docker Compose (dev/prod), Caddy, Prometheus + exporters, scripts de backup/deploy/rollback.
- **CI:** GitHub Actions (api-ci, web-ci, governance-ci).

## 4. Documentos analisados

README, ROADMAP, ESCOPO, ARQUITETURA, BANCO_DADOS, CONTEXTO, AGENTS, 13 specs SDD (`docs/specs/`), `docs/uat/*`, `AUDITORIA.md` (obsoleto), `Runbook.md`, `infra/*`, `scripts/*`, migrations, seed, código `apps/api/app` e `apps/web/src`.

## 5. Escopo consolidado

12 domínios SDD + SPEC-13 (WhatsApp). MVP assistido = monitoramento + cotação por arquivo. Integrações automáticas ERP/transportadoras = pós-MVP.

## 6. Metodologia

1. Inventário documental e técnico.
2. Execução de gates: `pytest` (API), `ruff`, `vitest`, `eslint`, `next build`, `check_secrets`, `infra/tests`.
3. Mapeamento requisito × implementação com evidências de arquivo/função/rota/teste.
4. Cálculo ponderado por área.
5. Identificação de divergências, riscos e plano de conclusão.

## 7–12. Percentuais

| Métrica | Valor |
|---|---|
| Escopo total | 83% |
| MVP | 88% |
| Completude funcional | 82% |
| Completude técnica | 90% |
| Prontidão para produção | 55% |

Ver memória de cálculo em `MATRIZ_REQUISITOS.md`.

## 13. Memória de cálculo

Áreas e contribuição ponderada (soma = 82,7% ≈ 83%):
- Funcionalidades 30% × 81,8 = 24,54
- Regras de negócio 15% × 86,0 = 12,90
- Back-end 10% × 90,0 = 9,00
- Front-end 10% × 88,0 = 8,80
- Banco 8% × 90,0 = 7,20
- Segurança 8% × 87,5 = 7,00
- Integrações 5% × 41,25 = 2,06
- Testes 5% × 80,0 = 4,00
- Infra 5% × 71,7 = 3,58
- Documentação 4% × 90,0 = 3,60

## 14. Matriz de requisitos

Ver `MATRIZ_REQUISITOS.md` (24 itens com ID, peso, status, %, evidência, pendências, risco, dependências).

## 15. Funcionalidades concluídas

Auth/RBAC, Transportadoras, Imports/Deliveries, Shipments (listagem/detalhe/filtros/busca), Campos fiscais/financeiros, Dashboard, Auditoria, Motor de cotação + override, Banco (migrations 1 head), Testes API/Web, CI, Documentação SDD, Secret scan.

## 16. Funcionalidades parciais

SLA (sem default global), Alertas externos (canal morto), Cobrança WhatsApp (modo degradação), Braspress (layout não homologado), Infra/Observabilidade/Backup (não validados em produção), E2E (não executado em prod), Relatórios (retenção a definir), Pedidos Web (UAT pendente).

## 17. Funcionalidades não iniciadas

UAT (0 execução), Canais externos de alerta reais (10%), Integração automática ERP/transportadoras (fora do MVP).

## 18. Divergências

### Documentado, mas não implementado
- **Canais externos de alerta** (`external_alert_channels_enabled` em `core/config.py` nunca usado; `AlertDeliveryLog.channel` só `in_app`). ESCOPO §9 diz "logs de entrega presentes; canal real PENDENTE DE VALIDAÇÃO".
- **CI ausente** — `ARQUITETURA.md` §3 diz "CI atual NÃO IDENTIFICADO"; na verdade há 3 workflows em `.github/workflows/`.
- **Web "não fecha build/testes/lint"** — `ARQUITETURA.md` §10 e `AUDITORIA.md` relatam estado pré-P0; hoje está verde (421 testes, build 19 rotas).

### Implementado, mas não documentado
- Endpoint `POST /api/v1/shipments/cobranca/run` e scheduler APScheduler (CONTEXTO cita, mas `ARQUITETURA.md` não lista cobrança).
- Métricas Prometheus em `/metrics` e exporters no compose prod.

### Implementado parcialmente
- SLA sem regra global default (status `unknown`).
- Cobrança WhatsApp em modo degradação (sem MCP configurado).

### Código órfão / não utilizado
- Flag `external_alert_channels_enabled` (configurada, nunca lida).
- `AUDITORIA.md` inteiro está obsoleto (pré-P0) e contradiz o estado atual.

### Mocks e placeholders
- Cobrança WhatsApp: `McpWhatsAppClient` retorna `None` (modo degradação) quando `ILEX_MCP_WHATSAPP_URL` ausente.
- `test_exceptions_panel_sla.py` tinha testes-placeholder (`pass`) — substituídos conforme CONTEXTO 2026-07-03.
- Fixture XLSX Web estava como TODO (resolvido por spec E2E).

### Riscos de falsa conclusão
- README/ESCOPO marcam domínios como "Confirmado" ignorando UAT/canais externos/backup real.
- `AUDITORIA.md` desatualizado induz leitura de "não pronto" quando já está estabilizado.

## 19. Auditoria de código (back-end)

- **Arquitetura:** routers / services / schemas / models bem separados. `app/main.py` monta 13 routers sob `/api/v1`.
- **Segurança de middleware:** dois blocos `CORSMiddleware` iguais (um `allow_credentials=False`, outro `True`) — redundante; `allow_credentials=False` no primeiro é inócuo. Baixo impacto.
- **Rate limiting:** `RedisRateLimiter`; em produção, indisponibilidade de Redis → `503` (seguro por design).
- **Tratamento global:** `register_exception_handlers` presente.
- **Problemas:**
  - `AUD-INFRA`: `infra/tests/test_c01_compose.py` referencia `compose_build_config` e `dockerfile_copy_sources` que **não existem** em `infra_checks.py` → 2 testes falham (NameError). Evidência: execução `pytest infra/tests` → 2 failed, 10 passed.
  - `external_alert_channels_enabled` morto (ver acima).
  - `enable_logging = True` hardcoded (sem desligar em teste) — aceitável.

## 20. Auditoria de segurança

- JWT: `HS256`, access 15min/refresh 7d, rotação por `token_version` (migration `20260703_01`).
- Produção rejeita JWT default, SQLite, CORS localhost, debug, falta Redis (`validate_production` em `core/config.py`).
- Headers defensivos + HSTS em produção (`main.py`).
- RBAC por `require_permission` em todas as rotas privadas; Web trata 401/403 (`AccessDenied`, `useApiErrorHandler`).
- **Pendências:** política de senha/expiração/revogação operacional; rate limiting depende de Redis; armazenamento de token no Web é risco residual (localStorage → recomendado cookie HttpOnly/BFF futuro).
- Secret scan self-test: aprovado. Nenhum secret real encontrado no repo.

## 21. Auditoria de banco

- 21 migrations + merge (`cbee64373bd6`), única head. `validate_migrations.py` aprovado.
- Models cobrem todas as entidades do escopo (users/roles/permissions, carriers, import_histories, deliveries, shipments, shipment_treatments, sla_rules, alerts, alert_delivery_logs, daily_reports, operational_audit_logs, orders, quote_rounds, freight_quotes).
- Valores monetários em `Numeric` (decimal). `orders` único por `(source, external_number)`; `freight_quotes` por `(round_id, carrier_id)`.
- **Pendências:** backup/restore real não validado; retenção de auditoria/relatórios A CONFIRMAR; SLA sem regra global default.

## 22. Auditoria de testes

- **API:** 783 passed / 0 failed em 95,79s (`pytest -q`). Ruff limpo.
- **Web:** 421 passed (vitest) / 0 failed; ESLint 0 erros; build 19 rotas.
- **Infra:** 10 passed / 2 failed (helper ausente em `test_c01_compose.py`).
- **E2E:** suíte Playwright preparada (304 cenários) — não executada em ambiente semelhante à produção (bloqueio P4).
- **Cobertura:** sem relatório de cobertura executado nesta sessão; estimada alta em módulos centrais com base no volume de testes.
- **Falsos positivos:** nenhum identificado; testes-placeholder de exceções já substituídos.

## 23. Auditoria de infraestrutura

- **Docker:** `docker-compose.yml` (dev) e `docker-compose.prod.yml` (prod com Caddy, Prometheus, exporters, redes internas). Dockerfiles em `infra/docker/`.
- **Health checks:** db/redis/api/web no dev; api/web no prod.
- **Observabilidade:** logs JSON + request-id (`core/observability.py`), `/metrics`, Prometheus + postgres/redis/node exporters no compose prod.
- **Backup/DR:** `infra/scripts/{backup,restore,deploy,rollback}_postgres.sh`.
- **Prontidão operacional:** Parcial — arquivos prontos, mas **não validados em execução real** nesta sessão (Docker Desktop inativo; PostgreSQL/restore/backup não executados).
- **CI:** 3 workflows presentes e como checks da `main` (contradiz `ARQUITETURA.md`).

## 24. Riscos

| Risco | Impacto | Severidade |
|---|---|---|
| UAT não executado | Não há aceite; DoD não atendido | Crítico |
| Canais de alerta externos ausentes | Cliente não recebe alertas | Alto |
| SLA sem default global | Status `unknown` enviesa métricas | Alto |
| Produção não validada (Docker/PG/backup) | Falha de continuidade | Alto |
| `AUDITORIA.md` obsoleto | Erro de leitura do estado | Médio |
| Testes infra quebrados (2) | Gate de infra vermelho | Médio |
| Rate limit depende de Redis | 503 se Redis cair (por design) | Médio |
| Token em localStorage (Web) | Risco de XSS em token | Médio |

## 25. Conclusão final

O Ilex Logística tem uma **base técnica sólida e verde** (testes, lint, build, migrations, CI, secret scan). O MVP assistido está funcionalmente implementado. Porém, **prontidão para produção é 55%**: depende de UAT executado, canais de alerta externos conectados (ou exclusão documentada), backup/PostgreSQL real validado, regra de SLA homologada e E2E em produção. Recomenda-se **entrada em homologação controlada**, não lançamento em produção.

Ver também: `TAREFAS_PARA_CONCLUSAO.md`, `ROADMAP_ATUALIZADO.md`, `MATRIZ_REQUISITOS.md`, `RESUMO_AUDITORIA.md`.
