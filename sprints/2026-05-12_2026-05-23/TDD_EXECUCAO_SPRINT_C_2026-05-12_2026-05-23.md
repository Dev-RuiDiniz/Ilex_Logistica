# TDD Execucao Sprint C (2026-05-12 a 2026-05-23)

## Nota de reconciliacao historica
Os artefatos legados da janela `2026-05-11_2026-05-21` foram mantidos para auditoria.
A base oficial desta execucao passa a ser a janela `2026-05-12 a 2026-05-23`.

## C-01 - Docker compose base
- RED: `python -m pytest -q tests/test_c01_compose.py` falhou com `ModuleNotFoundError`.
- GREEN: implementado `compose_services_summary` em `Infra/infra_checks.py`.
- GREEN validado: `python -m pytest -q tests/test_c01_compose.py`.
- Execucao: https://github.com/ilex-logistica/Infra/issues/5

## C-02 - Env templates
- RED: `python -m pytest -q tests/test_c02_env_templates.py` falhou por função ausente.
- GREEN: implementado `env_template_keys` em `Infra/infra_checks.py`.
- GREEN validado: `python -m pytest -q tests/test_c02_env_templates.py`.
- Execucao: https://github.com/ilex-logistica/Infra/issues/6

## C-03 - CI API
- RED: `python -m pytest -q tests/test_c03_c04_workflows.py` falhou por parser ausente.
- GREEN: parser `workflow_step_names` implementado e valida etapas `Run lint`/`Run tests`.
- GREEN validado: `python -m pytest -q tests/test_c03_c04_workflows.py`.
- Execucao: https://github.com/ilex-logistica/Infra/issues/7

## C-04 - CI Web
- RED: mesmo ciclo RED do teste de workflow com função ausente.
- GREEN: validação de `Run lint` e `Run build` no workflow Web.
- GREEN validado: `python -m pytest -q tests/test_c03_c04_workflows.py`.
- Execucao: https://github.com/ilex-logistica/Infra/issues/8

## C-05 - Observabilidade inicial
- RED: `python -m pytest -q tests/test_c05_observability.py` falhou por função ausente.
- GREEN: implementado `observability_has_minimum_sections`.
- GREEN validado: `python -m pytest -q tests/test_c05_observability.py`.
- Execucao: https://github.com/ilex-logistica/Infra/issues/9

## C-06 - Templates de issue/PR
- Checklist primeiro: sprint oficial, vinculos obrigatorios e campos de aceite.
- Evidencia: template `scrum-task.yml` atualizado para calendario oficial.
- Execucao: https://github.com/ilex-logistica/.github/issues/2

## C-07 - ADR fundacional
- Checklist primeiro: contexto, decisao, alternativas, consequencias e relacao com sprint.
- Evidencia: ADR oficial referenciado no documento C-07.
- Execucao: https://github.com/ilex-logistica/Docs/issues/42

## C-08 - Matriz de riscos
- Checklist primeiro: risco P0/P1 com dono, gatilho e mitigacao.
- Evidencia: matriz oficial C-08 publicada na janela oficial.
- Execucao: https://github.com/ilex-logistica/Docs/issues/43

## C-09 - Plano QA minimo
- Checklist primeiro: casos por LOG-001..LOG-005 e criterio de saida.
- Evidencia: plano QA oficial C-09 e vínculo de execucao em Integrations.
- Execucao: https://github.com/ilex-logistica/Integrations/issues/3

## C-10 - Cerimonias Scrum
- Checklist primeiro: planning, daily, review e retro com dono e prazo.
- Evidencia: pacote oficial de cerimonias publicado na janela oficial.
- Execucao: https://github.com/ilex-logistica/Docs/issues/45
