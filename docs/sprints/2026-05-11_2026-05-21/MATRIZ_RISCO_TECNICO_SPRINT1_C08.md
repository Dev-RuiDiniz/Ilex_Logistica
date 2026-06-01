# C-08 - Matriz de risco técnico da Sprint 1

## Contexto

Período: 11/05/2026 a 21/05/2026.

Objetivo: acompanhar riscos técnicos que podem afetar ambiente, CI, observabilidade, API, Web e governança do MVP Ilex Logística.

## Escala

| Campo | Valores |
|---|---|
| Probabilidade | Baixa, Média, Alta |
| Impacto | Baixo, Médio, Alto |
| Severidade | P0, P1, P2 |

## Matriz

| ID | Risco | Probabilidade | Impacto | Severidade | Gatilho | Mitigação | Dono | Status |
|---|---|---|---|---|---|---|---|---|
| R-01 | Ambiente local não reproduzível por ausência de Docker no workstation | Média | Alto | P0 | `docker` indisponível ou compose falha | Documentar pré-requisitos e validar em máquina com Docker | DevOps | Aberto |
| R-02 | Secrets reais vazarem em templates ou commits | Baixa | Alto | P0 | `.env` commitado ou secret real em workflow | Usar placeholders, revisar diff e manter `.env` ignorado | Tech Lead | Monitorado |
| R-03 | API e Web divergirem na URL base e contrato de endpoints | Média | Médio | P1 | Web aponta para API incorreta ou endpoint muda sem registro | Padronizar `NEXT_PUBLIC_API_URL` e contrato em Docs | Tech Lead | Aberto |
| R-04 | CI não refletir ambiente local | Média | Médio | P1 | Testes passam local e falham no GitHub Actions | Fixar versões Python/Node e comandos equivalentes | DevOps | Monitorado |
| R-05 | Migrations quebrarem bootstrap do banco | Média | Alto | P0 | `alembic upgrade head` falha no container | Validar migrations em CI/ambiente local antes do deploy | Backend | Aberto |
| R-06 | Observabilidade insuficiente para troubleshooting | Média | Médio | P1 | Falha sem log ou healthcheck inconclusivo | Logs HTTP básicos e healthchecks no compose | QA/DevOps | Monitorado |
| R-07 | Templates Scrum não serem usados na operação | Média | Médio | P2 | Issues/PRs sem critérios e evidências | Revisar cerimônias e exigir checklist antes do merge | Scrum Master | Aberto |
| R-08 | Vulnerabilidades moderadas no Web ficarem sem triagem | Média | Médio | P1 | `npm audit` reporta vulnerabilidades | Registrar pendência e avaliar upgrade seguro em branch própria | Tech Lead | Aberto |

## Acompanhamento nas dailies

- Revisar riscos P0 diariamente.
- Atualizar dono, status e mitigação quando houver nova evidência.
- Converter risco em issue quando houver ação técnica necessária.

## Critérios de aceite

- Todo risco P0/P1 possui dono e ação de mitigação.
- Riscos são revisados antes da Sprint Review.
- Pendências técnicas são refletidas na PR da Sprint C.
