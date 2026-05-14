# Contrato API Fundacional A-09 (2026-05-12 a 2026-05-23)

## Endpoints
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh
- GET /api/v1/carriers
- POST /api/v1/carriers
- PUT /api/v1/carriers/{carrier_id}
- POST /api/v1/carriers/{carrier_id}/inactivate

## Regras de autorizacao
- admin: leitura e escrita
- logistica: leitura e escrita operacional
- gestor: leitura e escrita operacional
- auditoria: somente leitura

## Contratos de erro
- 401 para autenticacao invalida/expirada
- 403 para perfil sem permissao
- 422 para payload invalido com `error.code = VALIDATION_ERROR`

## Evidencias
- tests/test_auth.py
- tests/test_rbac.py
- tests/test_carriers.py
- tests/test_tdd_sprint_a.py
