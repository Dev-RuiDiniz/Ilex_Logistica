# PR Body — BETA-020A

## Título
[BETA-020A] Segurança e RBAC Backend/API

## Base
main

## Head
feature/beta-020a-security-rbac-backend-api

## Escopo

Implementa segurança e RBAC (Role-Based Access Control) no backend/API, incluindo:
- Tabela de permissões no banco de dados
- Sistema de roles e permissões
- Dependências de autenticação com verificação de permissões
- Testes de RBAC para todos os endpoints críticos
- Seed de permissões para setup inicial

## Evidências

**Testes RBAC:**
- 8/8 testes passando (test_rbac_permissions.py)
- 6/6 testes passando (test_rbac_audit_api.py)
- 7/7 testes passando (test_rbac_reports_api.py)
- 7/7 testes passando (test_rbac_alerts_api.py)
- 7/7 testes passando (test_rbac_sla_api.py)
- 7/7 testes passando (test_rbac_shipments_api.py)
- 7/7 testes passando (test_rbac_imports_api.py)
- 7/7 testes passando (test_rbac_carriers_api.py)
- 7/7 testes passando (test_rbac_users_api.py)
- **Total: 63/63 testes RBAC passando**

**Migrations:**
- 20260623_01_add_permissions.py: Tabela de permissões
- Seed de permissões: 7 roles, 15 permissões

## Testes

**Backend:**
```bash
cd apps/api
python -m pytest tests/test_rbac_permissions.py tests/test_rbac_audit_api.py tests/test_rbac_reports_api.py tests/test_rbac_alerts_api.py tests/test_rbac_sla_api.py tests/test_rbac_shipments_api.py tests/test_rbac_imports_api.py tests/test_rbac_carriers_api.py tests/test_rbac_users_api.py -v -rs
```

**Gates:**
```bash
python scripts/check_secrets.py --repo-root .
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/beta_validate.py
```

## Gates

- ✅ check_secrets: OK
- ✅ validate_migrations: OK
- ✅ validate_docs: OK
- ✅ beta_validate: OK

## Limitações

- Nenhuma limitação crítica

## Governança

- **Branch:** feature/beta-020a-security-rbac-backend-api
- **Base:** main (com merge commit de BETA-018B, BETA-019A, BETA-019B)
- **Status:** Draft PR
- **Merge:** Não realizado
- **Auto-merge:** Não habilitado
- **Force push:** Não utilizado

## Checklist

- [x] Testes RBAC passando (63/63)
- [x] Migrations validadas
- [x] Gates oficiais passando
- [x] Documentação atualizada
- [x] Sem merge
- [x] Sem auto-merge
- [x] Sem force push
