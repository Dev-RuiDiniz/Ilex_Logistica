# PR Body — BETA-020B

## Título
[BETA-020B] RBAC Backend para Endpoints Operacionais Restantes

## Base
feature/beta-020a-security-rbac-backend-api

## Head
feature/beta-020b-rbac-operational-endpoints-backend

## Escopo

Implementa RBAC para endpoints operacionais restantes, incluindo:
- Permissões para carriers (read/write)
- Permissões para imports (read/write)
- Permissões para shipments (read/write)
- Permissões para users (read/write, admin only)
- Testes de RBAC para endpoints operacionais
- Migration de carriers_permissions

## Evidências

**Testes RBAC Operacionais:**
- 8/8 testes passando (test_rbac_carriers_api.py)
- 8/8 testes passando (test_rbac_imports_api.py)
- 7/7 testes passando (test_rbac_shipments_api.py)
- 7/7 testes passando (test_rbac_users_api.py)
- **Total: 30/30 testes RBAC operacionais passando**

**Migrations:**
- 20260624_01_add_carriers_permissions.py: Permissões de carriers

**Frontend:**
- Correção de regressão frontend (types.ts)
- Atualização de vitest.config.ts e vitest.setup.ts

## Testes

**Backend:**
```bash
cd apps/api
python -m pytest tests/test_rbac_carriers_api.py tests/test_rbac_imports_api.py tests/test_rbac_shipments_api.py tests/test_rbac_users_api.py -v -rs
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

- **Branch:** feature/beta-020b-rbac-operational-endpoints-backend
- **Base:** feature/beta-020a-security-rbac-backend-api
- **Status:** Draft PR
- **Merge:** Não realizado
- **Auto-merge:** Não habilitado
- **Force push:** Não utilizado

## Checklist

- [x] Testes RBAC operacionais passando (30/30)
- [x] Migrations validadas
- [x] Gates oficiais passando
- [x] Documentação atualizada
- [x] Sem merge
- [x] Sem auto-merge
- [x] Sem force push
