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

