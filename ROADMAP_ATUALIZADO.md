# ROADMAP_ATUALIZADO.md — Ilex Logística

**Data:** 2026-07-20
**Base:** estado real do repositório (evidências de execução), não o roadmap anterior.

## 1. Estado atual

- **Técnico:** verde. API 783 testes, Web 421 testes, ruff/eslint limpos, build 19 rotas, migrations 1 head, CI presente, secret scan OK.
- **Funcional:** MVP assistido implementado (monitoramento + cotação CSV/XLSX + cobrança WhatsApp em degradação).
- **Prontidão:** 55%. Bloqueado por UAT, canais de alerta externos, backup/PG real, SLA final, E2E em prod.
- **Classificação:** Beta / Homologação.

## 2. Fases restantes

### Fase 0 — Correções emergenciais (P0)
- **Objetivo:** remover bloqueadores de homologação.
- **Tarefas:** T-P0-1 (UAT), T-P0-2 (canais alerta), T-P0-3 (backup PG), T-P0-4 (testes infra), T-P0-5 (SLA).
- **Dependências:** ambiente executável (Docker/PG).
- **Saída:** UAT assinado, alertas resolvidos, backup testado, SLA homologado, infra tests verdes.
- **Estimativa:** ~16,5 dias-homem.
- **Riscos:** indisponibilidade de VPS/Docker; resistência a decisão de canais fora do MVP.

### Fase 1 — Conclusão do MVP (P1)
- **Objetivo:** produto utilizável e auditável.
- **Tarefas:** T-P1-1 (E2E prod), T-P1-2 (política senha), T-P1-3 (Docker prod), T-P1-4 (doc), T-P1-5 (Braspress), T-P1-6 (pedidos), T-P1-7 (specs).
- **Dependências:** Fase 0.
- **Saída:** MVP homologado, E2E verde, specs fechadas.
- **Estimativa:** ~12,5 dias-homem.
- **Riscos:** E2E instável em prod; divergências de layout com cliente.

### Fase 2 — Segurança e estabilidade (P2)
- **Objetivo:** endurecer operação.
- **Tarefas:** T-P2-1 (MCP real), T-P2-2 (performance VPS), T-P2-3 (token cookie), T-P2-4/5 (retenção), T-P2-6 (obs VPS).
- **Dependências:** Fase 1.
- **Saída:** cobrança real ou documentada; métricas de carga; token seguro.
- **Estimativa:** ~12,5 dias-homem.
- **Riscos:** templates Meta não aprovados; custo de VPS.

### Fase 3 — Homologação (P5 original)
- **Objetivo:** aceite formal e release.
- **Tarefas:** release notes, treinamento, suporte, go-live decision, tag RC.
- **Dependências:** Fases 0–2.
- **Saída:** RC publicada + piloto + decisão GO.
- **Estimativa:** ~3 dias-homem.

### Fase 4 — Produção
- **Objetivo:** operação com monitoramento e rollback.
- **Tarefas:** deploy VPS, observabilidade ativa, runbooks, backup agendado.
- **Dependências:** Fase 3.

### Fase 5 — Melhorias pós-lançamento (P3)
- **Objetivo:** evolução (ERP/transportadoras automáticas, multi-tenant, LGPD).
- **Dependências:** contrato com parceiros.
- **Estimativa:** >31 dias-homem.

## 3. Entregáveis por fase

| Fase | Entregáveis principais |
|---|---|
| 0 | UAT assinado, alertas resolvidos, backup testado, SLA homologado |
| 1 | MVP homologado, E2E verde, specs fechadas, Docker prod validado |
| 2 | Cobrança real, performance medida, token seguro, retenção definida |
| 3 | RC + piloto + go-live |
| 4 | Produção operando com obs/backup |
| 5 | ERP/transportadoras/multi-tenant/LGPD |

## 4. Dependências críticas

- VPS/Docker/PostgreSQL disponíveis para validação real.
- Decisão de produto sobre canais de alerta externos (real vs fora do MVP).
- Amostras sanitizadas de Braspress e ERP para homologação de layout.
- Templates Meta aprovados para WhatsApp (se canal real).

## 5. Critérios de saída

- Gates P0–P5 do ROADMAP original atendidos com evidência fresca.
- UAT por perfil assinado.
- `release_gate.py` aprovado (P4/UAT/GO marcados).
- Backup/restore testado; observabilidade ativa.

## 6. Riscos

- Ambiente externo (VPS/DNS/TLS/credenciais) não provisionado → trava P4.
- Falsa conclusão por documentação otimista (README/ESCOPO/"confirmado").
- SLA sem default global enviesa indicadores.
- `AUDITORIA.md` obsoleto confunde leitura de status.

## 7. Cenário mínimo (MVP utilizável)

- **% atual vs cenário:** ~88% do MVP já implementado.
- **Tarefas restantes:** T-P0-1, T-P0-3, T-P0-5, T-P1-1, T-P1-5, T-P1-6, T-P1-7.
- **Esforço:** ~3–4 semanas-homem.
- **Riscos:** UAT revelar lacunas; SLA divergir do cliente.
- **Condições:** ambiente executável + amostras sanitizadas + decisão de canais.

## 8. Cenário recomendado (produção controlada)

- **% atual vs cenário:** ~70%.
- **Tarefas restantes:** Fases 0–3.
- **Esforço:** ~6–8 semanas-homem.
- **Riscos:** performance em PG real; custo VPS; templates Meta.
- **Condições:** VPS + Docker + PostgreSQL + backup + observabilidade validados.

## 9. Cenário completo (escopo original + pós-MVP)

- **% atual vs cenário:** ~45%.
- **Tarefas restantes:** Fases 0–5.
- **Esforço:** >12 semanas-homem.
- **Riscos:** dependência de terceiros (ERP/transportadoras), multi-tenant, LGPD.
- **Condições:** contratos homologados, sandbox, credenciais seguras.
