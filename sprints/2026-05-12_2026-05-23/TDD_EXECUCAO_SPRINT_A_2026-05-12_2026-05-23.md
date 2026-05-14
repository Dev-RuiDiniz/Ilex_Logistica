# TDD Execucao Sprint A (2026-05-12 a 2026-05-23)

Este documento registra evidencias RED/GREEN/REFACTOR por tarefa A-01..A-10.

## A-01 - Estruturar projeto FastAPI em camadas
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a01_health_endpoint_foundation` (falhou com `assert 200 == 503`).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a01_health_endpoint_foundation` (passou: `1 passed`).
- Evidencia tecnica: endpoint `/health` responde 200 e payload `{\"status\": \"ok\"}`.
- Rastreio: Issue Docs `#16`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-02 - Configurar conexao PostgreSQL e sessao SQLAlchemy
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a02_broken_database_ping` (falhou com excecao operacional nao tratada no teste inicial).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a02_broken_database_ping` (passou: `1 passed`).
- Evidencia tecnica: ping de banco com engine quebrada retorna `False` sem quebrar a aplicacao.
- Rastreio: Issue Docs `#17`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-03 - Criar migrations iniciais e modelos de usuarios/perfis
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a03_migration_upgrade_downgrade_flow` (falhou em assercao de tabela apos downgrade).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a03_migration_upgrade_downgrade_flow` (passou: `1 passed`).
- Evidencia tecnica: fluxo `upgrade -> downgrade` confirma criacao e remocao consistente da tabela `users`.
- Rastreio: Issue Docs `#18`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-04 - Implementar autenticacao JWT (login e refresh)
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a04_login_invalid_credentials` (falhou com `assert 401 == 200` no criterio inicial errado).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a04_login_invalid_credentials` (passou: `1 passed`).
- Evidencia tecnica: login com credencial invalida retorna `401` conforme contrato de seguranca.
- Rastreio: Issue Docs `#19`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-05 - Aplicar guardas por perfil em rotas protegidas
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a05_rbac_blocks_write_for_auditor` (falhou com `assert 403 == 201`).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a05_rbac_blocks_write_for_auditor` (passou: `1 passed`).
- Evidencia tecnica: perfil `auditoria` recebe `403` para escrita em `carriers`.
- Rastreio: Issue Docs `#20`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-06 - Criar CRUD de transportadoras
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a06_crud_carriers_flow` (falhou com `assert 0 == 1` na listagem final).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a06_crud_carriers_flow` (passou: `1 passed`).
- Evidencia tecnica: fluxo create/update/inactivate funcional e listagem padrao oculta itens inativos.
- Rastreio: Issue Docs `#21`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-07 - Padronizar validacao e respostas de erro
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a07_validation_error_contract` (falhou com `assert 422 == 200`).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a07_validation_error_contract` (passou: `1 passed`).
- Evidencia tecnica: payload invalido retorna `422` com codigo `VALIDATION_ERROR`.
- Rastreio: Issue Docs `#22`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-08 - Consolidar suite minima automatizada
- RED comando: `pytest -q tests/test_tdd_sprint_a.py::test_a08_suite_minima_sprint_a` (falhou no primeiro ciclo de especificacao da suite minima).
- GREEN comando: `pytest -q tests/test_tdd_sprint_a.py::test_a08_suite_minima_sprint_a` (passou: `1 passed`).
- Evidencia tecnica: suite TDD da trilha A consolidada com 8 testes de regressao (`test_a01`..`test_a08`).
- Rastreio: Issue Docs `#23`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-09 - Publicar contrato tecnico dos endpoints fundacionais
- RED evidenciado: `A09_RED_OK_MISSING` (arquivo de contrato ausente no inicio do ciclo).
- GREEN evidenciado: `GREEN_OK_FILES_CREATED` (arquivo criado e validado em disco).
- Artefato: `CONTRATO_API_FUNDACIONAL_A09_2026-05-12_2026-05-23.md`.
- Rastreio: Issue Docs `#24`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

## A-10 - Consolidar checklist de prontidao backend da Sprint 1
- RED evidenciado: `A10_RED_OK_MISSING` (checklist ausente no inicio do ciclo).
- GREEN evidenciado: `GREEN_OK_FILES_CREATED` (checklist criado e validado em disco).
- Artefato: `CHECKLIST_PRONTIDAO_BACKEND_A10_2026-05-12_2026-05-23.md`.
- Rastreio: Issue Docs `#25`, Epic Docs `#2`, Milestone `Sprint 01 - Fundacao do MVP (2026-05-12 a 2026-05-23)`.

