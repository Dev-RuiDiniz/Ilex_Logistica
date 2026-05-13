# C-08 - Matriz de risco técnico da Sprint 1

## Contexto

Período da Sprint 1: 11/05/2026 a 21/05/2026.

Objetivo: acompanhar riscos técnicos da fundação do Ilex Logística relacionados a ambiente local, CI/CD, observabilidade, governança GitHub, documentação e QA mínimo.

## Escala

| Campo | Valores |
|---|---|
| Probabilidade | Baixa, Média, Alta |
| Impacto | Baixo, Médio, Alto |
| Severidade | P0, P1, P2 |
| Status | Aberto, Monitorado, Mitigado, Convertido em issue |

## Matriz de riscos

| ID | Descrição | Categoria | Probabilidade | Impacto | Severidade | Gatilho objetivo | Dono | Mitigação preventiva | Plano de contingência | Status | Data de revisão |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Pipeline falhando por dependência não travada ou mudança transiente de pacote | CI/CD | Média | Alto | P1 | `npm ci`, `pip install`, lint, teste ou build falha sem alteração funcional relacionada | DevOps | Usar lockfile no Web, versões mínimas documentadas e cache configurado | Abrir issue técnica, fixar versão afetada e reexecutar pipeline | Monitorado | 2026-05-13 |
| R-02 | Ambientes divergentes entre equipe impedem reprodução da stack | Ambiente local | Alta | Alto | P0 | `docker compose config/up` falha em uma máquina ou Docker indisponível | DevOps | Documentar pré-requisitos, `.env.example`, compose e comandos de setup | Validar em máquina alternativa com Docker e registrar variação no setup | Aberto | 2026-05-13 |
| R-03 | Falta de governança de backlog causa tarefas sem DoD, aceite ou evidência | Governança | Média | Médio | P1 | Issue ou PR aberto sem ID, critérios, plano de teste ou evidência | Scrum Master | Templates de Issue/PR e checklist antes do merge | Bloquear revisão até completar template e atualizar backlog | Monitorado | 2026-05-13 |
| R-04 | Comandos de API/Web ausentes ou inconsistentes entre documentação e CI | CI/CD | Média | Alto | P1 | README diverge de workflow ou comando local não existe | Tech Lead | Documentar comandos equivalentes ao CI em README de API/Web | Corrigir README/workflow e revalidar localmente antes da PR | Monitorado | 2026-05-13 |
| R-05 | Healthcheck inexistente ou instável reduz capacidade de diagnóstico | Observabilidade | Média | Alto | P1 | `docker compose ps` mostra `starting/unhealthy` sem causa clara ou endpoint `/health` falha | DevOps/QA | Healthchecks com `interval`, `timeout`, `retries`, `start_period` e logs documentados | Consultar `docker compose logs --tail=100 api db` e ajustar healthcheck | Monitorado | 2026-05-13 |
| R-06 | Secrets reais commitados por engano | Segurança | Baixa | Alto | P0 | `git diff` ou PR contém token, senha real ou `.env` versionado | Tech Lead | `.gitignore`, placeholders em `.env.example` e revisão de diff | Remover secret, rotacionar credencial e reescrever histórico se necessário | Monitorado | 2026-05-13 |
| R-07 | Capacidade da sprint sem margem para validar Docker, CI e QA | Planejamento | Média | Alto | P1 | Tarefas C-01..C-10 ficam sem validação ou evidência até a review | PM Técnico | Priorizar P0/P1, separar commits por tarefa e acompanhar daily | Reduzir escopo não crítico e registrar pendências explícitas na PR | Aberto | 2026-05-13 |
| R-08 | Plano de QA não cobre critérios reais de LOG-001..LOG-005 | QA | Média | Alto | P1 | Casos de teste não mapeiam login, perfis, CRUD ou aceite funcional | QA | Criar plano mínimo com casos, critérios e evidências esperadas | Abrir tarefas complementares de QA e bloquear aceite sem evidência | Aberto | 2026-05-13 |
| R-09 | Documentação desatualizada após mudanças em API, Web ou Infra | Documentação | Média | Médio | P1 | README, ADR ou guia local diverge do código/workflow vigente | Docs Owner | Referenciar ADR, README e guias nas tarefas e revisar no PR | Atualizar documentação antes do merge ou registrar pendência rastreável | Monitorado | 2026-05-13 |
| R-10 | PRs grandes sem separação por tarefa dificultam review e rollback | Governança Git | Média | Médio | P1 | PR mistura C-01..C-10 sem commits claros ou arquivos sem relação | Scrum Master | Commits exclusivos por tarefa e templates de PR | Solicitar split/squash orientado ou PRs por repositório/tarefa | Aberto | 2026-05-13 |
| R-11 | Merge sem revisão técnica introduz regressão ou quebra governança | Governança Git | Baixa | Alto | P0 | PR mergeado sem aprovação, checklist ou evidências | Tech Lead | Reforçar checklist e regra de não fazer merge automático sem revisão | Reverter merge e abrir revisão pós-incidente | Aberto | 2026-05-13 |
| R-12 | Migrations do banco quebram bootstrap da API no container | Banco/API | Média | Alto | P0 | `alembic upgrade head` falha durante startup da API | Backend | Validar migrations localmente e manter DB healthcheck antes da API | Corrigir migration, limpar volume local se necessário e recriar stack | Aberto | 2026-05-13 |
| R-13 | Vulnerabilidades moderadas do Web ficam sem triagem | Segurança frontend | Média | Médio | P1 | `npm audit` reporta vulnerabilidade moderada sem issue de acompanhamento | Tech Lead | Registrar pendência e avaliar upgrade seguro em branch separada | Abrir issue de segurança e priorizar atualização controlada | Aberto | 2026-05-13 |

## Riscos P0/P1 para acompanhamento diário

| ID | Severidade | Dono | Ação de mitigação | Status |
|---|---|---|---|---|
| R-01 | P1 | DevOps | Usar lockfile, versões documentadas e cache configurado | Monitorado |
| R-02 | P0 | DevOps | Validar Docker/Compose e documentar setup local | Aberto |
| R-03 | P1 | Scrum Master | Exigir templates de Issue/PR completos | Monitorado |
| R-04 | P1 | Tech Lead | Alinhar README e workflows da API/Web | Monitorado |
| R-05 | P1 | DevOps/QA | Validar healthchecks e logs da stack | Monitorado |
| R-06 | P0 | Tech Lead | Manter `.env` ignorado e revisar diffs | Monitorado |
| R-07 | P1 | PM Técnico | Priorizar P0/P1 e registrar pendências | Aberto |
| R-08 | P1 | QA | Mapear QA mínimo para LOG-001..LOG-005 | Aberto |
| R-09 | P1 | Docs Owner | Atualizar docs junto com mudanças técnicas | Monitorado |
| R-10 | P1 | Scrum Master | Separar commits/PRs por tarefa | Aberto |
| R-11 | P0 | Tech Lead | Bloquear merge sem revisão e aprovação | Aberto |
| R-12 | P0 | Backend | Validar migrations e bootstrap do container | Aberto |
| R-13 | P1 | Tech Lead | Triar `npm audit` e planejar upgrade seguro | Aberto |

## Acompanhamento nas dailies

Usar esta matriz na daily para responder:

- Algum gatilho objetivo ocorreu desde a última daily?
- Algum risco P0/P1 mudou de probabilidade, impacto ou status?
- Alguma mitigação precisa virar issue ou PR?
- Alguma pendência bloqueia C-01..C-10?
- Algum risco pode ser marcado como mitigado com evidência?

## Riscos da Sprint C cobertos

- C-01: ambiente local, Docker Compose, DB e migrations.
- C-02: `.env.example`, secrets e configuração local.
- C-03: CI da API, dependências Python e testes.
- C-04: CI do Web, dependências Node e build.
- C-05: healthchecks, logs e diagnóstico.
- C-06: templates de Issue/PR e revisão antes do merge.
- C-07: ADR e decisões arquiteturais.
- C-08: matriz de risco técnico.
- C-09: plano de QA mínimo para LOG-001..LOG-005.
- C-10: cerimônias Scrum e acompanhamento semanal.

## Critérios de atualização

- Atualizar `Status` em toda daily quando houver nova evidência.
- Converter risco em issue quando existir ação técnica concreta.
- Manter dono obrigatório para todo risco P0/P1.
- Registrar data de revisão sempre que o risco mudar de status.
