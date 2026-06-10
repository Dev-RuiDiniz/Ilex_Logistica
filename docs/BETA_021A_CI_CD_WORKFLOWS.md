# BETA-021A — CI/CD e Workflows

## Workflows Existentes

**1. Beta CI Bootstrap** (`.github/workflows/beta-ci.yml`)
- Gatilho: PR/push em main
- Jobs: validate
- Passos:
  - Checkout
  - Setup Python 3.11
  - Install dependencies (apps/api[dev])
  - Secret scan
  - Secret self-test
  - Validate migrations
  - Validate docs
  - Beta validation
- Status: Alinhado com scripts oficiais ✓

**2. API CI** (`apps/api/.github/workflows/api-ci.yml`)
- Gatilho: PR/push em main
- Jobs: lint-and-test
- Passos:
  - Checkout
  - Setup Python 3.11
  - Install dependencies
  - Run lint (ruff check)
  - Run tests (pytest -q)
  - Test migrations
  - Check secrets
- Status: Alinhado com scripts oficiais ✓

**3. Web CI** (`apps/web/.github\workflows/web-ci.yml`)
- Gatilho: PR/push em main
- Jobs: lint-and-build
- Passos:
  - Checkout
  - Setup Node.js 22
  - Run Web validation script
  - Check secrets
  - Install Playwright browsers
  - Run E2E validation script
  - Upload Playwright report
- Status: **PROBLEMA IDENTIFICADO**

## Problemas Identificados

**Web CI:**
- `scripts/validate_web.sh` usa `npm test` (linha 13)
- Comando correto é `npm run test`
- Isso causará falha no CI quando rodar

## Secrets Referenciados

**Beta CI:**
- Nenhum secret referenciado (usa scripts oficiais)

**API CI:**
- ILEX_APP_NAME
- ILEX_ENVIRONMENT
- ILEX_DATABASE_URL
- ILEX_JWT_SECRET
- ILEX_JWT_ALGORITHM
- ILEX_JWT_ACCESS_MINUTES
- ILEX_JWT_REFRESH_MINUTES
- Status: Variáveis de ambiente, não secrets hardcoded ✓

**Web CI:**
- NEXT_PUBLIC_API_URL
- Status: Variável de ambiente, não secret hardcoded ✓

## Correção Necessária

**scripts/validate_web.sh:**
- Linha 13: `npm test` → `npm run test`

## Recomendação

Corrigir `scripts/validate_web.sh` para usar `npm run test` em vez de `npm test`.
