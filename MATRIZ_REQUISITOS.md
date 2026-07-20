# MATRIZ_REQUISITOS.md — Ilex Logística

**Auditoria:** 2026-07-20
**Método:** inspeção de código + execução de gates (pytest, ruff, vitest, eslint, build, secret scan, infra tests)
**Critério de percentual:** ver seção 4 do prompt de auditoria (0/10/25/50/70/85/95/100%).

> Legenda de status: Concluído (C), Parcial (P), Não iniciado (N), Bloqueado (B), Não comprovado (X), Fora do escopo (F).

## Pesos por área (soma = 100%)

| Área | Peso |
|---|---|
| Funcionalidades principais | 30% |
| Regras de negócio | 15% |
| Back-end e APIs | 10% |
| Front-end e experiência | 10% |
| Banco e integridade | 8% |
| Autenticação, autorização e segurança | 8% |
| Integrações externas | 5% |
| Testes e qualidade | 5% |
| Infraestrutura, deploy e observabilidade | 5% |
| Documentação e operação | 4% |

## Matriz consolidada

| ID | Módulo | Requisito | Origem | Prior. | Peso área | Status | % | Evidência | Pendências | Risco | Dep. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUTH-001 | Auth | Login + refresh JWT | SPEC-01 | Crítica | Seg | C | 95 | `modules/auth/router.py`, `core/security.py`, testes | Política de expiração/rotação por versão presente; hardening operacional pendente | Médio | — |
| USER-001 | Users/RBAC | Usuários, papéis, permissões, proteção de rotas | SPEC-01 | Crítica | Seg | P | 85 | `modules/users`, `middleware.ts`, `lib/permissions.ts`, 783 testes | Definição de política de senha/expiração/revogação operacional | Médio | AUTH-001 |
| CARR-001 | Carriers | Cadastro, edição, listagem, inativação | SPEC-02 | Alta | Func | C | 90 | `modules/carriers`, página `/carriers` | UAT ponta a ponta | Baixo | AUTH-001 |
| IMP-001 | Imports | CSV/XLSX preview, validação, confirmação, duplicidade, histórico | SPEC-03 | Crítica | Func | C | 90 | `modules/imports`, `/shipments/import`, `/shipments/deliveries` | Homologação com amostra operacional | Baixo | AUTH-001 |
| IMP-002 | Braspress | Mapper Braspress assistido | SPEC-03 | Alta | Func | P | 85 | `modules/imports/braspress*.py`, fixtures | Layout versionado + amostra sanitizada homologada | Médio | IMP-001 |
| SHIP-001 | Shipments | Listagem, detalhe, filtros combináveis, busca | SPEC-04 | Crítica | Func | C | 90 | `modules/shipments/router.py`, `/shipments`, `/shipments/[id]` | — | Baixo | IMP-001 |
| SHIP-002 | Fiscal/Fin | Campos NF, valor, frete, % sem divisão por zero | SPEC-04/Apêndice1 | Crítica | Regra | C | 90 | `shipments/models.py`, `analytics_service.py`, 17 testes API | — | Baixo | SHIP-001 |
| SLA-001 | SLA | Regras, recálculo, atraso, criticidade | SPEC-05 | Alta | Regra | P | 80 | `modules/sla/service.py`, `seed_demo.py` (3 regras por carrier) | Regra operacional final a homologar; **sem regra global default** (status `unknown` se não houver regra) | Alto | SHIP-001 |
| TREAT-001 | Tratativas | Registro de ações, painel priorizado | SPEC-06 | Alta | Func | P | 85 | `modules/shipments/exceptions_service.py`, `/exceptions` | E2E integrado + taxonomia a homologar; `test_exceptions_panel_sla.py` tinha placeholders (substituídos) | Médio | SHIP-001 |
| EFF-001 | Eficiência | Agregação por transportadora, ranking determinístico | SPEC-07 | Alta | Regra | P | 85 | `analytics_service.py`, `/carrier-efficiency`, dataset reconciliado | UAT humano do ranking/desempate | Médio | SHIP-002 |
| DASH-001 | Dashboard | KPIs, resumo, filtros, tendência | SPEC-08 | Alta | Func | C | 90 | `modules/dashboard`, `/dashboard` | — | Baixo | EFF-001 |
| ALA-001 | Alertas | Geração, leitura, resolução, logs | SPEC-09 | Alta | Func | P | 85 | `modules/alerts/service.py`, `/alerts` | Canais externos não conectados (ver ALA-002) | Médio | SHIP-001 |
| ALA-002 | Alertas (canal) | Entrega externa de alertas (e-mail/WhatsApp) | SPEC-09 | Média | Integração | N | 10 | Flag `external_alert_channels_enabled` em `core/config.py` **nunca referenciado**; `AlertDeliveryLog.channel` só `in_app` | Implementar dispatcher externo real ou marcar fora do MVP | Alto | ALA-001 |
| REP-001 | Relatórios | Geração, consulta, exportação diária | SPEC-10 | Média | Func | P | 85 | `modules/reports`, `/reports/daily` | Retenção/agendamento a definir | Baixo | SHIP-001 |
| AUD-001 | Auditoria | Eventos operacionais, consulta, resumo | SPEC-11 | Alta | Func | C | 90 | `modules/audit`, `/audit` | Retenção A CONFIRMAR | Baixo | AUTH-001 |
| ORD-001 | Pedidos | Importação assistida ERP CSV/XLSX | SPEC-12 | Alta | Func | P | 85 | `modules/orders/service.py`, `/orders`, migration `20260703_02` | Homologação humana do layout | Médio | IMP-001 |
| ORD-002 | Cotação | Motor comparativo, melhor opção, override | SPEC-12 | Alta | Regra | C | 90 | `modules/orders/quote_service.py`, `choose_best_quote` | — | Baixo | ORD-001 |
| ORD-003 | Pedidos Web | Subaba, detalhe, histórico, comparação | SPEC-12 | Alta | Front | P | 85 | `/orders`, `/orders/[id]`, `/quote-rounds/[id]` | UAT do fluxo P3 | Médio | ORD-002 |
| WHA-001 | WhatsApp | Cobrança via MCP, escalonamento, idempotência | SPEC-13 | Média | Integração | P | 60 | `integrations/mcp_whatsapp.py`, `cobranca_service.py`, `POST /shipments/cobranca/run`, `ChargeDispatchModal.tsx` | MCP não configurado → modo degradação (só log interno); scheduler default off; UAT pendente | Médio | ALA-001 |
| SEC-001 | Segurança | JWT, RBAC, validação de entrada, auditoria | SPEC-01 | Crítica | Seg | P | 85 | `core/config.py`, `dependencies.py`, `errors.py` | Rate limiting depende de Redis; hardening de senha pendente | Médio | AUTH-001 |
| SEC-002 | Segurança prod | Rejeita JWT default, CORS, headers, HSTS | ARQUITETURA §8 | Crítica | Seg | P | 85 | `core/config.py.validate_production`, `main.py` security headers | Não validado em ambiente real de produção | Médio | SEC-001 |
| DB-001 | Banco | Models, migrations, FK, índices, 1 head | BANCO_DADOS | Crítica | Banco | C | 90 | 21 migrations + merge, `validate_migrations.py` | Backup/restore real não validado | Baixo | — |
| TEST-001 | Testes API | Unit/integration | ROADMAP P0 | Alta | Testes | C | 95 | **783 passed** em 95,79s | — | Baixo | — |
| TEST-002 | Testes Web | Unit/component | ROADMAP P0 | Alta | Testes | C | 95 | **421 passed** (vitest) | — | Baixo | — |
| TEST-003 | E2E | Playwright crítico | ROADMAP P4 | Alta | Testes | P | 50 | Suíte preparada (304 cenários); não executada em ambiente semelhante à produção | Execução em VPS/PostgreSQL pendente | Alto | TEST-001 |
| INFRA-001 | Infra | Docker Compose dev/prod | infra/ | Alta | Infra | P | 85 | `docker-compose.yml`, `docker-compose.prod.yml`, Dockerfiles | Execução real do Docker não observada nesta sessão | Médio | DB-001 |
| INFRA-002 | CI | Workflows API/Web/governance | .github/workflows | Alta | Infra | C | 90 | `api-ci.yml`, `web-ci.yml`, `governance-ci.yml` (contradiz `ARQUITETURA.md` que dizia "NÃO IDENTIFICADO") | — | Baixo | TEST-001 |
| INFRA-003 | Observabilidade | Logs JSON, métricas, Prometheus | infra/ | Média | Infra | P | 70 | `core/observability.py`, `prometheus.yml`, exporters no compose prod | Ativação no VPS não observada | Médio | INFRA-001 |
| INFRA-004 | Backup | Backup/restore/rollback | infra/scripts | Alta | Infra | P | 60 | `backup_postgres.sh`, `restore_postgres.sh`, `deploy_vps.sh`, `rollback_vps.sh` | Validação real em PostgreSQL bloqueada (Docker Desktop inativo) | Alto | INFRA-001 |
| INFRA-005 | Secrets | Gestão de secrets fora do repo | scripts/ | Alta | Seg | P | 85 | `check_secrets.py` self-test OK; `.env.example` | Valores reais não provisionados | Médio | — |
| DOC-001 | Documentação | Specs, README, runbooks | docs/ | Média | Doc | C | 90 | 13 specs, `AUDITORIA.md` (obsoleto pré-P0), runbooks | `AUDITORIA.md` desatualizado; UAT/Release pendentes | Baixo | — |
| UAT-001 | UAT | Execução por perfil + aceite | ROADMAP P5 | Crítica | Qualidade | N | 5 | `docs/uat/*.md` preparados; **nenhuma execução/assinatura** | Executar UAT e obter aceite | Crítico | TEST-003 |
| PERF-001 | Performance | Metas de carga, gate 10k pedidos | ROADMAP P4 | Média | Infra | P | 40 | Gate local 10k pedidos = 5,07s (SQLite mem); runner HTTP 50 users pronto | Medição em VPS/PostgreSQL pendente | Alto | INFRA-001 |
| ERP-001 | ERP API | Integração automática ERP | ESCOPO §7.2 | Baixa | Integração | F | 0 | Fora do MVP; pós-contrato | — | — | — |

## Contagem

- Concluído (≥90%): 9 itens (AUTH-001, CARR-001, IMP-001, SHIP-001, SHIP-002, DASH-001, AUD-001, ORD-002, DB-001, TEST-001, TEST-002, INFRA-002, DOC-001) — 13
- Parcial (50–89%): 18 itens
- Não iniciado / fora de escopo: ALA-002 (10%), ERP-001 (0%), UAT-001 (5%)
- Bloqueadores (P0): UAT-001, INFRA-004, ALA-002, TEST-003, SLA-001 (regra final)

## Memória de cálculo (por área)

| Área | Itens | Média % | Peso | Contribuição |
|---|---|---|---|---|
| Funcionalidades principais | AUTH,USER,CARR,IMP,IMP2,SHIP,SHIP2,SLA,TREAT,EFF,DASH,ALA,REP,AUD,ORD1,ORD2,ORD3,WHA | 81,8 | 30% | 24,54 |
| Regras de negócio | SLA,EFF,SHIP2,ORD2,TREAT | 86,0 | 15% | 12,90 |
| Back-end e APIs | (saúde geral API) | 90,0 | 10% | 9,00 |
| Front-end | (19 rotas, 421 testes, build OK) | 88,0 | 10% | 8,80 |
| Banco e integridade | DB-001 | 90,0 | 8% | 7,20 |
| Auth/segurança | AUTH,USER,SEC1,SEC2,INFRA5 | 87,5 | 8% | 7,00 |
| Integrações externas | IMP2,WHA,ALA2,ERP | 41,25 | 5% | 2,06 |
| Testes e qualidade | TEST1,TEST2,TEST3 | 80,0 | 5% | 4,00 |
| Infra/deploy/obs | INFRA1,INFRA3,INFRA4 | 71,7 | 5% | 3,58 |
| Documentação/operação | DOC-001 | 90,0 | 4% | 3,60 |

**Percentual geral ponderado = 82,7%** (arredondado para **83%**).

> Nota: o percentual geral reflete implementação+testes locais. A prontidão para produção é menor (veja `RESUMO_AUDITORIA.md`) por depender de UAT, validação externa e canais de alerta.
