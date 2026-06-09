# BETA_AUTOMATED_VALIDATION_MAP - Scripts de Validação Beta

**Data:** 2026-06-08  
**PR:** BETA-002 - Scripts de Smoke/CI e Validação Beta Automatizada  
**Objetivo:** Criar scripts padronizados de validação beta para API, Web, E2E, migrations e secrets

---

## 1. Resumo Executivo

O BETA-002 cria uma camada de scripts que permite validar o beta inteiro com comandos simples, documentados e seguros, reduzindo comandos manuais soltos para uma validação automatizada reproduzível localmente e no CI.

**Estratégia:**
- Scripts bash no diretório `scripts/`
- Validação unificada via `scripts/beta_validate.sh`
- Scripts modulares para cada domínio (API, Web, E2E, Migrations, Secrets)
- Integração com workflows CI existentes
- Sem dependência de serviços externos reais

---

## 2. Scripts Criados

### 2.1 Script Raiz

**Arquivo:** `scripts/beta_validate.sh`

**Função:** Orquestra todas as validações beta em um único comando

**Validações:**
1. Verificação de scripts obrigatórios
2. Verificação de secrets
3. Validação da API
4. Validação do Web
5. Validação E2E
6. Validação de migrations (básico)

**Uso:**
```bash
bash scripts/beta_validate.sh
```

### 2.2 Scripts Modulares

#### validate_api.sh

**Arquivo:** `scripts/validate_api.sh`

**Função:** Valida a API (Python/FastAPI)

**Validações:**
- Instalação de dependências
- Lint (ruff)
- Testes (pytest)
- Validação de migrations (básico)

**Uso:**
```bash
bash scripts/validate_api.sh
```

#### validate_web.sh

**Arquivo:** `scripts/validate_web.sh`

**Função:** Valida o Web (Next.js/TypeScript)

**Validações:**
- Instalação de dependências (npm ci)
- Lint (eslint)
- Testes unitários (vitest)
- Build (next build)

**Uso:**
```bash
bash scripts/validate_web.sh
```

#### validate_e2e.sh

**Arquivo:** `scripts/validate_e2e.sh`

**Função:** Valida testes E2E (Playwright)

**Validações:**
- Verificação de Playwright instalado
- Instalação de browsers (se necessário)
- Execução de testes E2E

**Uso:**
```bash
bash scripts/validate_e2e.sh
```

#### validate_migrations.sh

**Arquivo:** `scripts/validate_migrations.sh`

**Função:** Valida migrations (Alembic)

**Validações:**
- Verificação de configuração Alembic
- Importação de configuração
- Verificação de versão atual

**Limitação:** Teste de rollback completo será implementado no BETA-004

**Uso:**
```bash
bash scripts/validate_migrations.sh
```

#### check_secrets.sh

**Arquivo:** `scripts/check_secrets.sh`

**Função:** Verifica secrets no código

**Padrões Proibidos:**
- Senhas com 8+ caracteres
- Tokens com 20+ caracteres
- Secrets com 20+ caracteres
- API keys
- Private keys
- Bearer tokens
- DATABASE_URL real
- SMTP real

**Padrões Permitidos (fixtures fake):**
- fake
- test
- example
- ilex.test
- changeme
- localhost
- 127.0.0.1
- sqlite

**Uso:**
```bash
bash scripts/check_secrets.sh
```

#### check_scripts_exist.sh

**Arquivo:** `scripts/check_scripts_exist.sh`

**Função:** Verificação mínima que falha quando scripts obrigatórios não existem (TDD Red)

**Validações:**
- Verifica script raiz (beta_validate.sh)
- Verifica scripts auxiliares
- Verifica comando test:e2e no package.json

**Uso:**
```bash
bash scripts/check_scripts_exist.sh
```

---

## 3. Integração CI

### 3.1 API CI

**Arquivo:** `apps/api/.github/workflows/api-ci.yml`

**Alterações:**
- Substitui comandos diretos por script `validate_api.sh`
- Adiciona verificação de secrets via `check_secrets.sh`

**Antes:**
```yaml
- name: Install dependencies
  run: python -m pip install -e .[dev]

- name: Run lint
  run: python -m ruff check .

- name: Run tests
  run: python -m pytest -q
```

**Depois:**
```yaml
- name: Run API validation script
  run: bash ../../scripts/validate_api.sh

- name: Check secrets
  run: bash ../../scripts/check_secrets.sh
```

### 3.2 Web CI

**Arquivo:** `apps/web/.github/workflows/web-ci.yml`

**Alterações:**
- Substitui comandos diretos por script `validate_web.sh`
- Adiciona verificação de secrets via `check_secrets.sh`
- Adiciona validação E2E via `validate_e2e.sh`
- Mantém upload de relatórios Playwright

**Antes:**
```yaml
- name: Install dependencies
  run: npm ci

- name: Run lint
  run: npm run lint

- name: Run build
  run: npm run build
```

**Depois:**
```yaml
- name: Run Web validation script
  run: bash ../../scripts/validate_web.sh

- name: Check secrets
  run: bash ../../scripts/check_secrets.sh

- name: Install Playwright browsers
  run: npx playwright install --with-deps

- name: Run E2E validation script
  run: bash ../../scripts/validate_e2e.sh
  env:
    CI: true

- name: Upload Playwright report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 7
```

---

## 4. Como Rodar Localmente

### 4.1 Validação Completa

```bash
# Na raiz do projeto
bash scripts/beta_validate.sh
```

### 4.2 Validação Individual

```bash
# API
bash scripts/validate_api.sh

# Web
bash scripts/validate_web.sh

# E2E
bash scripts/validate_e2e.sh

# Migrations
bash scripts/validate_migrations.sh

# Secrets
bash scripts/check_secrets.sh
```

### 4.3 Windows (PowerShell)

```powershell
# No PowerShell, use bash via WSL ou Git Bash
bash scripts/beta_validate.sh
```

---

## 5. Critérios de Aceite

- ✅ `bash scripts/beta_validate.sh` existe e executa validação beta agregada
- ✅ Há comando separado para validar API
- ✅ Há comando separado para validar Web
- ✅ Há comando separado para validar E2E
- ✅ Secret scan básico existe e é executado
- ✅ CI chama os scripts (API e Web)
- ✅ Documentação explica como rodar localmente
- ✅ Nenhum secret real é incluído
- ✅ Draft PR aberto

---

## 6. O Que Ainda Depende do BETA-004

### 6.1 Migrations Rollback Completo

**Status:** ⏳ Pendente

**Limitação Atual:**
- `validate_migrations.sh` apenas verifica que migrations podem ser importadas
- Não testa upgrade/rollback em banco limpo
- Não valida que dados não são perdidos

**Planejamento BETA-004:**
- Criar ambiente de teste isolado
- Testar upgrade → downgrade → upgrade cycle
- Validar integridade de dados
- Documentar procedimento de rollback seguro

---

## 7. Riscos e Mitigações

### 7.1 Riscos

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|--------------|-----------|
| Scripts não funcionam em Windows | Alto | Alta | Documentar uso via WSL/Git Bash |
| Scripts dependem de ambiente específico | Médio | Média | Scripts verificam pré-requisitos |
| CI não consegue executar scripts | Alto | Baixa | Scripts testados localmente antes |
| Secret scan falso positivo | Baixo | Baixa | Padrões permitidos bem definidos |

### 7.2 Rollback

**Se scripts causarem problemas:**
1. Reverter commit dos scripts
2. Restaurar workflows CI originais
3. Investigar causa raiz
4. Corrigir scripts
5. Reaplicar após validação

**Comando de rollback:**
```bash
git revert <commit-hash>
git push origin feature/beta-002-smoke-ci-scripts
```

---

## 8. Referências

- **Plano de Execução:** docs/BETA_DEVIN_EXECUTION_PLAN.md
- **BETA-001:** PR #7 - Smoke UI Automatizado com Playwright
- **Playwright Docs:** https://playwright.dev

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ✅ Implementação concluída, aguardando validação
