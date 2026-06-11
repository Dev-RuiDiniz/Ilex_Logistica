# BETA-021B — Verificação de Conflito Potencial

## Análise de Diffs

### BETA-020A vs main
**Arquivos alterados:** 5
- CONTEXTO.md (27 linhas)
- PROMPT_GOVERNANCE_TEMPLATE.md (removido, 327 linhas)
- RELATORIO_DIA.md (43 linhas)
- beta019b_backend_targeted_current.txt (binário)
- docs/RELATORIO_MERGE_PR38_PR39.md (removido, 171 linhas)

**Tipo de mudança:** Documentação e limpeza de arquivos temporários
**Risco de conflito:** Nenhum (BETA-018B, BETA-019A, BETA-019B já em main)

### BETA-020B vs BETA-020A
**Arquivos alterados:** 20
- apps/api/app/modules/carriers/router.py (10 linhas)
- apps/api/app/modules/imports/router.py (16 linhas)
- apps/api/app/modules/shipments/router.py (20 linhas)
- apps/api/app/modules/users/router.py (10 linhas)
- apps/api/app/modules/users/seed_permissions.py (8 linhas)
- migrations/20260624_01_add_carriers_permissions.py (38 linhas)
- apps/api/tests/test_rbac_carriers_api.py (133 linhas)
- apps/api/tests/test_rbac_imports_api.py (136 linhas)
- apps/api/tests/test_rbac_shipments_api.py (126 linhas)
- apps/api/tests/test_rbac_users_api.py (115 linhas)
- apps/web/src/app/(private)/reports/daily/page.tsx (2 linhas)
- apps/web/src/lib/types.ts (19 linhas)
- apps/web/vitest.config.ts (1 linha)
- apps/web/vitest.setup.ts (10 linhas)
- docs/BETA_020A_SECURITY_RBAC_BACKEND_API.md (2 linhas)
- docs/BETA_020B_RBAC_OPERATIONAL_ENDPOINTS_BACKEND.md (279 linhas)
- docs/BETA_KNOWN_LIMITATIONS.md (18 linhas)
- docs/BETA_NEXT_ACTIONS.md (3 linhas)

**Tipo de mudança:** RBAC backend para endpoints operacionais
**Risco de conflito:** Baixo (aditivo, não sobrescreve código existente)

### BETA-020C vs BETA-020B
**Arquivos alterados:** 33
- AGENTS.md (35 linhas)
- apps/web/middleware.ts (4 linhas)
- apps/web/src/app/(private)/alerts/page.tsx (9 linhas)
- apps/web/src/app/(private)/audit/page.tsx (7 linhas)
- apps/web/src/app/(private)/carriers/page.tsx (13 linhas)
- apps/web/src/app/(private)/reports/daily/page.tsx (3 linhas)
- apps/web/src/app/(private)/settings/sla/page.tsx (21 linhas)
- apps/web/src/app/(private)/shipments/import/page.tsx (7 linhas)
- apps/web/src/app/(private)/shipments/page.tsx (5 linhas)
- apps/web/src/app/(private)/users/page.tsx (53 linhas)
- apps/web/src/components/AccessDenied.test.tsx (44 linhas)
- apps/web/src/components/AccessDenied.tsx (27 linhas)
- apps/web/src/components/app-shell.navigation.test.tsx (101 linhas)
- apps/web/src/components/app-shell.test.tsx (15 linhas)
- apps/web/src/components/app-shell.tsx (102 linhas)
- apps/web/src/lib/alerts-api.error-handler.test.ts (45 linhas)
- apps/web/src/lib/api-auth.test.ts (107 linhas)
- apps/web/src/lib/api.ts (15 linhas)
- apps/web/src/lib/carriers-api.error-handler.test.ts (46 linhas)
- apps/web/src/lib/daily-report-api.error-handler.test.ts (45 linhas)
- apps/web/src/lib/error-handler.test.ts (43 linhas)
- apps/web/src/lib/error-handler.ts (25 linhas)
- apps/web/src/lib/imports-api.error-handler.test.ts (45 linhas)
- apps/web/src/lib/permissions.test.ts (229 linhas)
- apps/web/src/lib/permissions.ts (160 linhas)
- apps/web/src/lib/shipments-api.error-handler.test.ts (45 linhas)
- apps/web/src/lib/sla-api.error-handler.test.ts (46 linhas)
- apps/web/src/lib/types.ts (20 linhas)
- docs/BETA_020C_SECURITY_RBAC_FRONTEND.md (332 linhas)
- docs/BETA_FUNCTIONAL_EPIC_AUDIT.md (12 linhas)
- docs/BETA_KNOWN_LIMITATIONS.md (14 linhas)
- docs/BETA_NEXT_ACTIONS.md (38 linhas)
- docs/BETA_RELEASE_GATE.md (54 linhas)

**Tipo de mudança:** Frontend RBAC (error-handler, permissions, AccessDenied)
**Risco de conflito:** Baixo (aditivo, não sobrescreve código existente)

### BETA-021A vs BETA-020C
**Arquivos alterados:** 13
- docs/BETA_021A_CI_CD_WORKFLOWS.md (78 linhas)
- docs/BETA_021A_DIAGNOSTICO_INICIAL.md (47 linhas)
- docs/BETA_021A_GITHUB_CREDENTIAL.md (34 linhas)
- docs/BETA_021A_PR_BLOQUEIO.md (165 linhas)
- docs/BETA_021A_QA_CI_CD_READINESS.md (164 linhas)
- docs/BETA_021A_SEGURANCA_READINESS.md (61 linhas)
- docs/BETA_COMMANDS.md (37 linhas)
- docs/BETA_FUNCTIONAL_EPIC_AUDIT.md (7 linhas)
- docs/BETA_KNOWN_LIMITATIONS.md (126 linhas)
- docs/BETA_NEXT_ACTIONS.md (27 linhas)
- docs/BETA_RELEASE_GATE.md (45 linhas)
- docs/BETA_VALIDATION_EVIDENCE.md (62 linhas)
- scripts/validate_web.sh (2 linhas)

**Tipo de mudança:** Documentação de QA/CI/CD e correção de script
**Risco de conflito:** Nenhum (documentação e scripts)

## Conclusão

**Risco Geral de Conflito:** Baixo

**Justificativa:**
1. Mudanças são em áreas distintas (documentação, backend RBAC, frontend RBAC, QA/CI/CD)
2. Mudanças são principalmente aditivas (não sobrescrevem código existente)
3. Cadeia linear de dependências (cada branch baseado no anterior)
4. Nenhum conflito óbvio nos diffs
5. BETA-018B, BETA-019A, BETA-019B já estão em main

**Recomendação:** Merge sequencial em ordem de dependência
1. BETA-020A → main
2. BETA-020B → main (após BETA-020A)
3. BETA-020C → main (após BETA-020B)
4. BETA-021A → main (após BETA-020C)
5. BETA-021B → main (após BETA-021A)
