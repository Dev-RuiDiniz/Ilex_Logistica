# TAREFAS_PARA_CONCLUSAO.md — Ilex Logística

**Data:** 2026-07-20
**Critério de aceite:** evidência de execução (teste/gate/comando) + documentação atualizada.

## 1. Lista completa de tarefas restantes (por prioridade)

### P0 — Bloqueadores críticos

| ID | Área | Tarefa | Problema | Arquivos | Complex. | Estimativa | Aceite | Risco |
|---|---|---|---|---|---|---|---|---|
| T-P0-1 | Qualidade | Executar UAT por perfil e registrar evidências/assinaturas | Nenhum aceite formal | `docs/uat/*.md` | Média | 5d | UAT aprovado por admin/logística/gestor/auditoria | Crítico |
| T-P0-2 | Alertas | Implementar dispatcher de canais externos OU marcar fora do MVP | `external_alert_channels_enabled` morto; só `in_app` | `modules/alerts/service.py`, `core/config.py` | Alta | 4d | Alerta sai por canal real OU decisão documentada | Alto |
| T-P0-3 | Infra | Validar backup/restore em PostgreSQL real | Gate P4 bloqueado | `infra/scripts/backup_postgres.sh`, `restore_postgres.sh` | Média | 2d | Restore testado em PG 16 | Alto |
| T-P0-4 | Testes | Corrigir `infra/tests/test_c01_compose.py` (helpers ausentes) | 2 falhas NameError | `infra/tests/test_c01_compose.py`, `infra/infra_checks.py` | Baixa | 0,5d | `pytest infra/tests` 12 passed | Médio |
| T-P0-5 | SLA | Homologar regra de SLA (default global + parâmetros) | Status `unknown` sem regra | `modules/sla/service.py`, `seed_demo.py` | Média | 3d | Regra assinada pelo cliente | Alto |

### P1 — Obrigatório para o lançamento

| ID | Área | Tarefa | Problema | Arquivos | Complex. | Estimativa | Aceite | Risco |
|---|---|---|---|---|---|---|---|---|
| T-P1-1 | E2E | Executar suíte Playwright em ambiente semelhante à produção | Risco de regressão | `apps/web/e2e` | Alta | 3d | E2E crítico verde em VPS | Alto |
| T-P1-2 | Segurança | Definir política de senha/expiração/revogação operacional | Apenas rotação por versão | `core/config.py`, `modules/auth` | Média | 2d | Política documentada e testada | Médio |
| T-P1-3 | Infra | Subir Docker Compose prod e validar health/observabilidade | Não validado em execução | `docker-compose.prod.yml`, `Caddyfile` | Média | 2d | Containers saudáveis + métricas | Médio |
| T-P1-4 | Doc | Atualizar `AUDITORIA.md` para estado pós-P0 | Obsoleto, contradiz estado | `AUDITORIA.md` | Baixa | 0,5d | Documento reflete Web verde + CI | Médio |
| T-P1-5 | Braspress | Homologar layout Braspress com amostra sanitizada | Layout não validado | `modules/imports/braspress*.py` | Média | 2d | Amostra importada sem erro | Médio |
| T-P1-6 | Pedidos | Homologar layout de pedidos ERP (humano) | Layout técnico OK, aceite pendente | `modules/orders/service.py` | Média | 2d | Amostra sanitizada aprovada | Médio |
| T-P1-7 | Release | Fechar specs do MVP como homologadas/excluídas | Specs em "confirmado" | `docs/specs/*` | Baixa | 1d | Specs com estado final | Médio |

### P2 — Importante após estabilização

| ID | Área | Tarefa | Complex. | Estimativa | Aceite | Risco |
|---|---|---|---|---|---|---|
| T-P2-1 | Cobrança | Configurar MCP WhatsApp real + templates Meta + ligar scheduler | Alta | 3d | Disparo real ou degradação documentada | Médio |
| T-P2-2 | Performance | Medir carga em VPS/PostgreSQL (50 users, 10k pedidos) | Média | 2d | p50/p95/p99 em PG | Alto |
| T-P2-3 | Segurança Web | Migrar token para cookie HttpOnly/BFF | Alta | 4d | Token fora de localStorage | Médio |
| T-P2-4 | Relatórios | Definir retenção/agendamento de relatório diário | Baixa | 1d | Retenção documentada | Baixo |
| T-P2-5 | Auditoria | Definir retenção de logs operacionais | Baixa | 0,5d | Retenção documentada | Baixo |
| T-P2-6 | Observabilidade | Validar alertas Prometheus + runbooks em VPS | Média | 2d | Alerta dispara em incidente | Médio |

### P3 — Evoluções futuras

| ID | Área | Tarefa | Complex. | Estimativa | Risco |
|---|---|---|---|---|---|
| T-P3-1 | ERP | Integração automática ERP (pós-contrato) | Alta | 10d+ | Alto |
| T-P3-2 | Transportadoras | APIs de rastreio/cotação automáticas | Alta | 10d+ | Alto |
| T-P3-3 | Multi-tenant | Segregação de dados por cliente | Alta | 8d+ | Alto |
| T-P3-4 | LGPD | Política de retenção/descarte | Média | 3d | Médio |

## 2. Dependências

- T-P0-1 (UAT) depende de T-P0-3/P-P1-3 (ambiente rodando) e T-P0-5 (SLA).
- T-P0-2 (canais) independe, mas bloqueia valor de negócio de alertas.
- T-P1-1 (E2E) depende de T-P1-3 (ambiente prod).
- T-P2-2 (performance) depende de T-P1-3.

## 3. Estimativas agregadas

- P0: ~16,5 dias-homem
- P1: ~12,5 dias-homem
- P2: ~12,5 dias-homem
- P3: >31 dias-homem

## 4. Critérios de aceite (globais)

Ver `AGENTS.md` §14 e `ROADMAP.md` §10. Resumo: gates verdes (api/web/infra/docs/secrets), UAT assinado, canais de alerta resolvidos, backup/PG validado, E2E em prod verde, specs fechadas.

## 5. Ordem recomendada

1. T-P0-4 (corrigir testes infra) — rápido, destrava gate.
2. T-P0-5 (SLA) + T-P1-5/T-P1-6 (homologar layouts).
3. T-P0-3 + T-P1-3 (subir e validar ambiente prod/backup).
4. T-P0-2 (canais de alerta) ou decisão documentada.
5. T-P1-1 (E2E em prod).
6. T-P0-1 (UAT por perfil).
7. T-P1-2/T-P1-4/T-P1-7 (segurança operacional, doc, specs).
8. T-P2-* (cobrança real, performance, hardening Web, retenção, obs).
9. T-P3-* (pós-MVP).

## 6. Checklist para MVP

- [ ] UAT executado e assinado
- [ ] SLA homologado (default + parâmetros)
- [ ] Layouts Braspress e pedidos aprovados
- [ ] Canais de alerta resolvidos (real ou fora de escopo)
- [ ] Build/testes/lint/secret scan verdes
- [ ] Migrations 1 head + roundtrip OK
- [ ] Specs do MVP fechadas

## 7. Checklist para produção

- [ ] Ambiente Docker prod saudável (health checks)
- [ ] Backup/restore PostgreSQL testado
- [ ] Observabilidade ativa (métricas/alertas/runbooks)
- [ ] Rate limiting com Redis validado
- [ ] E2E em prod verde
- [ ] Política de senha/expiração documentada
- [ ] Token Web fora de localStorage (ou mitigado)
- [ ] Release notes + go-live decision assinados

## 8. Definition of Done

Projeto concluído somente quando: todos os requisitos obrigatórios implementados; critérios de aceite atendidos; projeto compila/executa; fluxos críticos funcionam; zero bloqueadores P0; zero vulnerabilidades críticas conhecidas; banco consistente; migrations funcionam; integrações obrigatórias conectadas; testes críticos verdes; deploy configurado; logs/alertas mínimos funcionando; documentação operacional atualizada; processo de backup/recuperação existente; ambiente de produção preparado; operável sem conhecimento informal.
