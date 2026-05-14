# C-09 - Plano de QA mínimo da Sprint 1 para LOG-001..LOG-005

## Objetivo do plano

Definir uma estratégia mínima, executável e rastreável para validar os critérios de aceite da fundação técnica do Ilex Logística na Sprint 1, cobrindo os itens LOG-001 a LOG-005 e os artefatos produzidos nas trilhas API, Web, Infra, Docs e `.github`.

## Escopo

- Validação de ambiente local com Docker Compose.
- Validação de healthcheck da API.
- Validação de acesso do banco para migrations.
- Validação de documentação de variáveis via `.env.example`.
- Validação de CI mínimo da API e do Web.
- Validação de healthchecks e logs para diagnóstico.
- Validação de templates de Issue/PR.
- Validação de ADR-001, matriz de risco e templates de cerimônias.

## Fora de escopo

- Testes end-to-end completos de fluxos LOG-006+.
- Testes de carga, segurança ofensiva ou pentest.
- Validação de deploy produtivo.
- Homologação com integrações externas reais.
- Automação completa de regressão funcional.

## Estratégia de teste

- Executar primeiro validações automatizadas de API e Web.
- Executar validações técnicas de Infra quando houver Docker disponível.
- Registrar evidência por caso de teste com comando, resultado, data e responsável.
- Usar validações manuais para governança, documentação e Review.
- Bloquear aceite da sprint quando um critério P0 não possuir evidência ou pendência registrada.

## Ambientes necessários

| Ambiente | Uso | Pré-requisitos |
|---|---|---|
| Local Windows/Linux/macOS | Execução manual de comandos e revisão documental | Git, Python 3.11, Node.js 22, acesso aos repositórios |
| Local com Docker | Validação de Compose, DB, healthchecks e logs | Docker Desktop ou Docker Engine com Compose |
| GitHub Actions | Validação de CI em PR/push | Workflows versionados e branch da sprint |
| GitHub Web | Revisão de templates, PR e evidências | Acesso ao repositório e permissões de review |

## Dados necessários

- Arquivo `Infra/.env.example` como referência segura de configuração.
- Variáveis locais derivadas dos templates sem secrets reais.
- Banco PostgreSQL local criado pelo Compose.
- Usuários ou dados sintéticos quando testes funcionais da API exigirem autenticação.
- Issues/PRs de teste ou preview dos templates GitHub.

## Critérios LOG-001..005

| Critério | Descrição de aceite |
|---|---|
| LOG-001 | Estrutura e responsabilidades dos repositórios estão documentadas e rastreáveis. |
| LOG-002 | Fundação da API pode ser validada por testes, healthcheck e CI mínimo. |
| LOG-003 | Banco local e migrations possuem caminho de validação documentado. |
| LOG-004 | Fundação Web pode ser validada por lint, testes, build e CI mínimo. |
| LOG-005 | Governança mínima de sprint existe com templates, ADR, riscos, QA e cerimônias. |

## Matriz de critérios vs testes

| Critério | Testes associados | Tipo | Evidência esperada |
|---|---|---|---|
| LOG-001 | QA-001, QA-002 | Manual | README/ADR com responsabilidades e branch correta |
| LOG-002 | QA-003, QA-004, QA-005 | Automatizado/Manual | Testes API passando, `/health` OK e workflow API versionado |
| LOG-003 | QA-006, QA-007, QA-008 | Manual/Técnico | DB saudável, migrations executadas e logs de Compose |
| LOG-004 | QA-009, QA-010, QA-011, QA-012 | Automatizado | Lint/test/build Web e workflow Web versionado |
| LOG-005 | QA-013, QA-014, QA-015, QA-016, QA-017 | Manual | Templates GitHub, ADR-001, matriz de risco, cerimônias e checklist Review |

## Casos de teste manuais

| ID | Critério | Objetivo | Passos | Resultado esperado | Evidência esperada | Responsável |
|---|---|---|---|---|---|---|
| QA-001 | LOG-001 | Confirmar branch e repositório | Executar `git branch --show-current` e revisar README do `Docs` | Branch `sprint-c-infra-qa-governanca` e documentação acessível | Saída do comando e link/trecho do README | QA |
| QA-002 | LOG-001 | Confirmar separação de responsabilidades | Revisar ADR-001 e README dos repositórios | API, Web, Infra, Docs e `.github` com papéis claros | Trecho do ADR-001 | QA/Arquiteto |
| QA-005 | LOG-002 | Confirmar healthcheck da API | Com API em execução, acessar `/health` e `/api/v1/health` | Resposta `{"status":"ok"}` | Saída `curl` ou print | QA |
| QA-006 | LOG-003 | Confirmar ambiente local com único comando | Executar `docker compose --env-file .env up --build` em `Infra` | API e DB sobem sem erro crítico | Log do Compose e `docker compose ps` | QA/DevOps |
| QA-007 | LOG-003 | Confirmar DB acessível para migrations | Executar startup da API ou `alembic upgrade head` contra DB local | Migrations aplicadas sem erro | Log do comando | Backend/QA |
| QA-008 | LOG-003 | Confirmar healthcheck/logs para diagnóstico | Executar `docker compose ps` e `docker compose logs --tail=100 api db` | Status e logs permitem identificar saúde de API/DB | Saída dos comandos | QA/DevOps |
| QA-013 | LOG-005 | Confirmar templates de Issue/PR | Revisar `.github/.github/ISSUE_TEMPLATE` e PR template | Templates têm ID, aceite, teste, evidência e riscos | Links ou trechos dos templates | QA/Scrum Master |
| QA-014 | LOG-005 | Confirmar ADR-001 | Revisar `Docs/adr/ADR-001.md` | ADR tem contexto, decisão, consequências e alternativas | Link/trecho do ADR | QA/Arquiteto |
| QA-015 | LOG-005 | Confirmar matriz de risco | Revisar `Docs/sprints/riscos-s1.md` | Riscos P0/P1 têm dono, status, gatilho e mitigação | Link/trecho da matriz | QA/PM Técnico |
| QA-016 | LOG-005 | Confirmar templates de cerimônias | Revisar documento de cerimônias da Sprint C | Planning, Daily, Review e Retrospective têm template | Link/trecho do documento | Scrum Master |
| QA-017 | LOG-005 | Confirmar prontidão para Review | Revisar checklist deste plano | Evidências mínimas anexadas e pendências explícitas | Checklist preenchido | QA |

## Casos de teste automatizados

| ID | Critério | Comando | Resultado esperado | Evidência esperada | Responsável |
|---|---|---|---|---|---|
| QA-003 | LOG-002 | `python -m pytest -q` no repositório `Api` | Suíte da API passa | Saída do pytest | Backend/QA |
| QA-004 | LOG-002 | Workflow de API em PR/push | Job de lint/test executa sem falha não justificada | Link/status do GitHub Actions | DevOps |
| QA-009 | LOG-004 | `npm run lint` no repositório `Web` | Lint sem erro | Log do comando | Frontend/QA |
| QA-010 | LOG-004 | `npm run test` no repositório `Web` | Testes passam | Saída Vitest | Frontend/QA |
| QA-011 | LOG-004 | `npm run build` no repositório `Web` | Build Next.js concluído | Log do build | Frontend/QA |
| QA-012 | LOG-004 | Workflow do Web em PR/push | Job de lint/build executa sem falha não justificada | Link/status do GitHub Actions | DevOps |

## Evidências esperadas

- Saídas de terminal para comandos Git, API, Web e Docker.
- Links ou prints de GitHub Actions para CI de API e Web.
- Trechos ou links dos arquivos `README.md`, `ADR-001.md`, `riscos-s1.md` e templates GitHub.
- Logs de `docker compose ps` e `docker compose logs` quando Docker estiver disponível.
- Checklist de Review preenchido antes da apresentação da sprint.

## Critério de entrada

- Branch `sprint-c-infra-qa-governanca` disponível.
- Commits das tarefas C-03, C-04, C-07 e C-08 disponíveis localmente ou na PR.
- README de API/Web/Infra acessíveis.
- Ambiente com Python 3.11 e Node.js 22 disponível.
- Docker disponível para validar Compose ou pendência registrada quando indisponível.

## Critério de saída

A Sprint 1 pode ser considerada pronta para Review quando:

- LOG-001..LOG-005 têm ao menos um teste executado ou pendência justificada.
- Casos P0 de ambiente, API healthcheck, DB/migrations, CI e governança têm evidência anexada.
- Falhas conhecidas possuem issue, risco ou pendência documentada.
- PRs estão abertos para revisão técnica, sem merge automático.
- ADR-001, matriz de risco e templates de cerimônias estão referenciados e revisáveis.
- Checklist de Review está completo ou com exceções aprovadas pelo PM Técnico.

## Riscos de QA

| ID | Risco | Mitigação |
|---|---|---|
| QA-R01 | Docker indisponível no workstation impede validação completa de Infra | Registrar bloqueio e validar em máquina alternativa com Docker |
| QA-R02 | CI não executado por falta de push/PR | Registrar validação local e executar CI assim que PR for aberta |
| QA-R03 | Evidências dispersas dificultam Review | Consolidar logs, links e prints no corpo da PR |
| QA-R04 | Critérios LOG-001..005 interpretados de forma diferente | Usar matriz critério vs teste como fonte de aceite |
| QA-R05 | Plano fica desatualizado após ajustes finais | Revalidar checklist antes da Review |

## Checklist de Review

- [ ] LOG-001 possui evidência de estrutura e responsabilidades.
- [ ] LOG-002 possui evidência de testes/API healthcheck/CI.
- [ ] LOG-003 possui evidência de DB, migrations ou pendência Docker justificada.
- [ ] LOG-004 possui evidência de lint, teste, build e CI Web.
- [ ] LOG-005 possui evidência de templates, ADR, riscos e cerimônias.
- [ ] Riscos P0/P1 foram revisados antes da Review.
- [ ] Pendências estão explícitas na PR.
- [ ] Nenhum secret real foi incluído nas evidências.
- [ ] Merge depende de revisão técnica.

## Responsáveis

| Papel | Responsabilidade |
|---|---|
| QA | Executar plano, coletar evidências e consolidar checklist |
| PM Técnico | Decidir aceite com base em evidências e riscos |
| Tech Lead | Revisar governança, CI, segurança e merge |
| DevOps | Validar Docker, healthchecks, logs e workflows |
| Backend | Validar API, migrations e healthcheck |
| Frontend | Validar lint, testes e build do Web |
| Scrum Master | Garantir uso dos templates e cerimônias |
