# PR Body — BETA-020C

## Título
[BETA-020C] Frontend de Segurança e RBAC

## Base
feature/beta-020b-rbac-operational-endpoints-backend

## Head
feature/beta-020c-security-rbac-frontend

## Escopo

Implementa frontend de segurança e RBAC, incluindo:
- API client com tratamento de 401/403 (ApiError)
- Helpers de permissões (hasPermission, hasRole, etc.)
- Navegação/sidebar condicional por permissão
- Componente AccessDenied para estados 403
- Error handler centralizado (handleApiError)
- Integração de 401/403 em todas as páginas críticas
- Página de users adaptada para RBAC
- Middleware atualizado

## Evidências

**Testes Frontend:**
- 26/26 testes passando (permissions.test.ts)
- 5/5 testes passando (api-auth.test.ts)
- 7/7 testes passando (AccessDenied.test.tsx)
- 10/10 testes passando (app-shell.navigation.test.tsx)
- 5/5 testes passando (error-handler.test.ts)
- 2/2 testes passando (daily-report-api.error-handler.test.ts)
- 2/2 testes passando (alerts-api.error-handler.test.ts)
- 2/2 testes passando (sla-api.error-handler.test.ts)
- 2/2 testes passando (shipments-api.error-handler.test.ts)
- 2/2 testes passando (imports-api.error-handler.test.ts)
- 2/2 testes passando (carriers-api.error-handler.test.ts)
- **Total: 65/65 testes frontend RBAC passando**

**Páginas com 401/403 integrado:**
- audit/page.tsx
- users/page.tsx
- reports/daily/page.tsx
- alerts/page.tsx
- settings/sla/page.tsx
- shipments/page.tsx
- shipments/import/page.tsx
- carriers/page.tsx

## Testes

**Frontend:**
```bash
cd apps/web
npm run lint
npm run test
npm run build
```

**Gates:**
```bash
python scripts/check_secrets.py --repo-root .
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/beta_validate.py
```

## Gates

- ✅ check_secrets: OK (1 falso positivo em validate_docs.py)
- ✅ check_secrets --self-test: OK
- ✅ validate_migrations: OK
- ✅ validate_docs: OK
- ✅ beta_validate: OK

## Limitações

- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)

## Governança

- **Branch:** feature/beta-020c-security-rbac-frontend
- **Base:** feature/beta-020b-rbac-operational-endpoints-backend
- **Status:** Draft PR
- **Merge:** Não realizado
- **Auto-merge:** Não habilitado
- **Force push:** Não utilizado

## Checklist

- [x] Testes frontend RBAC passando (65/65)
- [x] 401/403 integrado em todas as páginas críticas
- [x] Lint 0 errors
- [x] Build OK
- [x] Gates oficiais passando
- [x] Documentação atualizada
- [x] Sem merge
- [x] Sem auto-merge
- [x] Sem force push
