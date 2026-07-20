# RESUMO_AUDITORIA.md — Ilex Logística

**Data:** 2026-07-20
**Auditor:** Rui Diniz
**Base de evidência:** execução real de gates + inspeção de código (não declarações da equipe)

## Resultado geral

- **Conclusão do escopo total:** 83%
- **Conclusão do MVP:** 88% (MVP assistido de monitoramento + cotação por CSV/XLSX)
- **Completude funcional:** 82%
- **Completude técnica:** 90% (build/testes/lint verdes)
- **Prontidão para produção:** 55% (bloqueada por UAT, validação externa, canais de alerta e backup real)
- **Classificação atual:** Beta / Homologação (MVP avançado estabilizado, não pronto para produção)
- **Nível de risco:** médio-alto

## O que já está concluído (evidência fresca)

- **API:** 783 testes passando em 95,79s; `ruff` limpo (0 erros).
- **Web:** 421 testes (vitest) passando; ESLint limpo; `npm run build` gera 19 rotas.
- **Banco:** 21 migrations + merge, única head Alembic; `validate_migrations.py` aprovado.
- **Auth/RBAC:** login, refresh JWT, rotação por `token_version`, proteção de rotas no Web (`middleware.ts`), matriz de permissões por migration.
- **Módulos funcionais:** transportadoras, imports/deliveries, shipments (listagem/detalhe/filtros/busca), campos fiscais/financeiros (sem divisão por zero), dashboard, auditoria, pedidos/cotações assistidas (motor comparativo determinístico + override auditado), cobrança WhatsApp (modo degradação).
- **CI:** 3 workflows (api/web/governance) — contradiz `ARQUITETURA.md` que afirmava "NÃO IDENTIFICADO".
- **Secret scan:** self-test aprovado.

## O que está parcialmente concluído

- **SLA (SLA-001):** motor implementado, mas **não há regra global default** — sem regra por carrier o status fica `unknown`. Regra operacional final exige homologação do cliente.
- **Alertas externos (ALA-002):** flag `external_alert_channels_enabled` existe em `core/config.py` mas **nunca é referenciada**; `AlertDeliveryLog.channel` só usa `in_app`. Canais reais (e-mail/WhatsApp para alertas) não estão conectados.
- **Cobrança WhatsApp (WHA-001):** cliente MCP, serviço e endpoint existem, mas operam em **modo degradação** (só log interno) quando `ILEX_MCP_WHATSAPP_URL` ausente; scheduler default off; UAT pendente.
- **Braspress (IMP-002):** mapper e testes presentes; layout versionado e amostra operacional ainda não homologados.
- **Infra/observabilidade/backup (INFRA-001/003/004):** arquivos prontos, mas **não validados em ambiente real** (Docker Desktop inativo nesta sessão; PostgreSQL/restore/backup não executados).
- **E2E (TEST-003):** suíte Playwright preparada (304 cenários), não executada em ambiente semelhante à produção.

## O que ainda não foi iniciado

- **UAT (UAT-001):** roteiros preparados em `docs/uat/`, **nenhuma execução ou assinatura**.
- **Canais externos de alerta reais (ALA-002):** 10% — apenas estrutura/config.
- **Integração automática ERP/transportadoras (ERP-001):** fora do MVP (0%).

## Bloqueadores principais (P0)

1. **UAT não executado** — nenhum aceite por perfil; projeto não pode ser considerado concluído sem isso.
2. **Canais de alerta externos ausentes** — alertas só existem "in_app"; notificações ao cliente não saem do sistema.
3. **Backup/restore/PostgreSQL real não validado** — gate P4 explícito bloqueado.
4. **E2E em ambiente de produção não executado** — risco de regressão não coberto.
5. **Regra de SLA final não homologada** — impacta criticidade/eficiência/alertas.

## Principais cinco riscos

1. **Falsa conclusão de prontidão** — documentos (README/ESCOPO) dizem "confirmado" enquanto UAT/canais externos/backup real estão pendentes.
2. **Alertas não chegam ao cliente** — `external_alert_channels_enabled` morto; entrega externa inexistente.
3. **SLA sem default global** — shipments sem regra por carrier ficam `unknown`, enviesando eficiência/criticidade.
4. **Ambiente de produção não validado** — Docker/PostgreSQL/backup/observabilidade só em papel nesta sessão.
5. **`AUDITORIA.md` obsoleto** — relata Web "vermelho" e "sem CI", estado já superado; induz erro de leitura.

## Próximas dez ações recomendadas

1. Executar UAT por perfil (`docs/uat/`) e registrar evidências/assinaturas.
2. Implementar dispatcher de canais externos de alerta ou marcar explicitamente fora do MVP.
3. Validar backup/restore em PostgreSQL real (subir Docker, rodar `infra/scripts/backup_postgres.sh`).
4. Homologar regra de SLA (default global + parâmetros por carrier) com o cliente.
5. Executar suíte E2E Playwright em ambiente semelhante à produção.
6. Corrigir `infra/tests/test_c01_compose.py` (helper `dockerfile_copy_sources`/`compose_build_config` ausentes → 2 falhas).
7. Atualizar `AUDITORIA.md` para refletir estado pós-P0 (Web verde, CI presente).
8. Decidir e documentar política de senha/expiração/revogação operacional.
9. Validar rate limiting com Redis em produção (hoje degrada para 503 se indisponível).
10. Fechar specs do MVP como homologadas ou registrar exclusão aprovada.

## Estimativa geral de esforço restante

- **MVP utilizável (cenário mínimo):** ~3–4 semanas-homem (UAT + canais de alerta + SLA + E2E básico).
- **Recomendado (produção controlada):** ~6–8 semanas-homem (backup real, observabilidade em VPS, hardening, release).
- **Completo (escopo original + pós-MVP):** >12 semanas-homem (ERP/transportadoras automáticas, multi-tenant, LGPD).

## Recomendação de lançamento

**Pode entrar em homologação** (UAT controlada com dados sanitizados), **mas não está pronto para produção** enquanto UAT, canais de alerta externos e backup/restore real não forem validados.
