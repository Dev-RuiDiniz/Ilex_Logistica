# BETA COMMANDS

Fonte oficial dos comandos de validação beta para o projeto Ilex Logística.

## Secret Scan

### Scan Normal
```bash
python scripts/check_secrets.py --repo-root .
```

**Saída Esperada:**
```
OK: No potential secrets found
```

### Self-Test
```bash
python scripts/check_secrets.py --repo-root . --self-test
```

**Saída Esperada:**
```
Self-test started
  Testing fake allowed values...
  OK: Fake values allowed
  Testing blocked secrets...
  OK: Simulated secret detected
Self-test completed successfully
```

## Migrations

### Validação Oficial (Python)
```bash
python scripts/validate_migrations.py
```

**Saída Esperada:**
```
Validating migrations...
Checking Alembic heads...
OK: Exactly 1 head found
Checking Alembic history...
OK: History check passed
Running migration tests...
OK: Migration validation passed
```

### Alembic CLI
```bash
cd apps/api

# Verificar head atual
alembic current

# Verificar heads
alembic heads

# Verificar histórico
alembic history

# Upgrade para head
alembic upgrade head

# Downgrade para base
alembic downgrade base
```

### Testes de Migrations
```bash
cd apps/api
python -m pytest tests/test_migrations.py -v
```


## API

### Testes Unitários
```bash
cd apps/api
python -m pytest -q
```

### Lint
```bash
cd apps/api
python -m ruff check .
```

## Web

### Testes Unitários
```bash
cd apps/web
npm run test
```

### Lint
```bash
cd apps/web
npm run lint
```

## E2E

### Testes E2E (Playwright)
```bash
cd apps/web
npx playwright test
```

### Testes E2E com UI
```bash
cd apps/web
npx playwright test --ui
```

## Cobertura

### API Coverage
```bash
cd apps/api
python -m pytest --cov=. --cov-report=xml --cov-report=html
```

**Saída Esperada:**
```
88% coverage
```

**Relatórios Gerados:**
- coverage.xml
- .coverage
- htmlcov/

### Web Coverage
```bash
cd apps/web
npm run test:coverage
```

**Saída Esperada:**
```
20.8% coverage
```

**Relatórios Gerados:**
- coverage/coverage-final.json
- coverage/coverage-summary.json

## Validação Beta Agregada

### Validação Oficial (Python)
```bash
python scripts/beta_validate.py
```

**Saída Esperada:**
```
Starting beta validation...
Project: <project-root>

1. Checking required scripts
OK: validate_migrations.py exists
OK: validate_docs.py exists

2. Validating documentation
OK: Documentation validation passed

3. Validating migrations (includes API tests)
OK: Migration validation passed

==========================================
BETA VALIDATION COMPLETED
==========================================

Validations passed:
  OK: Documentation validation
  OK: Migration validation (includes API tests)

Project is ready for Beta!
```

## Validação Documental

### Validação de Documentos
```bash
python scripts/validate_docs.py
```

**Saída Esperada:**
```
Validating documentation...
OK: All required docs exist
OK: All official commands exist
OK: No references to removed Bash wrappers
OK: No obvious secrets in docs
OK: No contradictory status
OK: Documentation validation passed
```

## Comandos de Desenvolvimento

### Setup API
```bash
cd apps/api
python -m pip install -e .[dev]
```

### Setup Web
```bash
cd apps/web
npm install
```

### Run API
```bash
cd apps/api
python -m uvicorn ilex.api:app --reload
```

### Run Web
```bash
cd apps/web
npm run dev
```

## Comandos de Git

### Status
```bash
git status
```

### Log
```bash
git log --oneline
```

### Diff
```bash
git diff
```

### Branch
```bash
git branch
```

### Fetch
```bash
git fetch origin
```


## BETA-021A — QA/CI/CD Final e Readiness Beta

### Gates Oficiais
```bash
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/beta_validate.py
```

### Backend QA Final
```bash
cd apps/api
python -m pytest tests/test_rbac_permissions.py tests/test_rbac_audit_api.py tests/test_rbac_reports_api.py tests/test_rbac_alerts_api.py tests/test_rbac_sla_api.py tests/test_rbac_shipments_api.py tests/test_rbac_imports_api.py tests/test_rbac_carriers_api.py tests/test_rbac_users_api.py -v -rs
python -m pytest tests/test_audit_log_model.py tests/test_audit_log_service.py tests/test_audit_log_api.py tests/test_audit_log_integrations.py -v -rs
python -m pytest tests/test_daily_report_model.py tests/test_daily_report_generation.py tests/test_daily_report_api.py tests/test_daily_report_integration.py -v -rs
python -m pytest tests/test_alerts_model.py tests/test_alerts_generation.py tests/test_alerts_api.py -v -rs
python -m pytest tests/test_sla_calculation.py tests/test_sla_rules.py tests/test_sla_api.py -v -rs
python -m pytest tests/test_braspress_assisted_import.py -v -rs
python -m pytest tests/test_shipment_detail_treatments_report_users.py -v -rs
```

### Frontend QA Final
```bash
cd apps/web
npm run lint
npm run test
npm run build
```

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

### Gates Oficiais (Revalidação)
```bash
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/beta_validate.py
```

### Backend QA Final (Revalidação)
```bash
cd apps/api
python -m pytest tests/test_rbac_permissions.py tests/test_rbac_audit_api.py tests/test_rbac_reports_api.py tests/test_rbac_alerts_api.py tests/test_rbac_sla_api.py tests/test_rbac_shipments_api.py tests/test_rbac_imports_api.py tests/test_rbac_carriers_api.py tests/test_rbac_users_api.py -v -rs
python -m pytest tests/test_audit_log_model.py tests/test_audit_log_service.py tests/test_audit_log_api.py tests/test_audit_log_integrations.py -v -rs
python -m pytest tests/test_daily_report_model.py tests/test_daily_report_generation.py tests/test_daily_report_api.py tests/test_daily_report_integration.py tests/test_alerts_model.py tests/test_alerts_generation.py tests/test_alerts_api.py tests/test_sla_calculation.py tests/test_sla_rules.py tests/test_sla_api.py tests/test_braspress_assisted_import.py tests/test_shipment_detail_treatments_report_users.py -v -rs
```

### Frontend QA Final (Revalidação)
```bash
cd apps/web
npm run lint
npm run test
npm run build
```

### Verificação de Conflito Potencial
```bash
git fetch origin
git diff --stat origin/main..origin/feature/beta-020a-security-rbac-backend-api
git diff --stat origin/feature/beta-020a-security-rbac-backend-api..origin/feature/beta-020b-rbac-operational-endpoints-backend
git diff --stat origin/feature/beta-020b-rbac-operational-endpoints-backend..origin/feature/beta-020c-security-rbac-frontend
git diff --stat origin/feature/beta-020c-security-rbac-frontend..origin/feature/beta-021a-qa-ci-cd-beta-readiness
```

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

### Script Auxiliar (Dry-Run)
```bash
python scripts/prepare_pending_prs.py
```

### Script Auxiliar (Execute)
```bash
python scripts/prepare_pending_prs.py --execute
```

### Verificação de Branches Remotos
```bash
git ls-remote --heads origin feature/beta-020a-security-rbac-backend-api
git ls-remote --heads origin feature/beta-020b-rbac-operational-endpoints-backend
git ls-remote --heads origin feature/beta-020c-security-rbac-frontend
git ls-remote --heads origin feature/beta-021a-qa-ci-cd-beta-readiness
git ls-remote --heads origin feature/beta-021b-final-integration-release-candidate
```

---

## Notas Importantes

### Python Oficial vs Bash Wrappers
- **Python Oficial:** Recomendado para máxima portabilidade
- **Bash Wrappers:** Removidos ou não oficiais (instáveis no Windows/Git Bash)
- **CI:** Usa Python diretamente

### Comandos Recomendados
1. `python scripts/check_secrets.py --repo-root .` - Secret scan
2. `python scripts/check_secrets.py --repo-root . --self-test` - Self-test real
3. `python scripts/validate_migrations.py` - Validação de migrations
4. `python scripts/beta_validate.py` - Validação beta agregada
5. `python scripts/validate_docs.py` - Validação documental

### Comandos Alternativos
- `cd apps/api && python -m pytest tests/test_migrations.py -v` - Testes de migrations diretos
- `cd apps/api && alembic heads` - Alembic CLI direto
- `cd apps/web && npx playwright test` - Playwright direto

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ✅ Concluído (BETA-021C - Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração)
