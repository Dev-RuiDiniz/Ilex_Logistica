# BETA_DEVIN_EXECUTION_PLAN - Plano de Execução TDD Fase Beta

**Data:** 2026-06-08  
**Agente:** Devin (SWE-1.6)  
**Repositório:** Dev-RuiDiniz/Ilex_Logistica  
**Branch Base:** origin/main (commit 27ca526)  
**Objetivo:** Concluir 100% do Roadmap TDD para Fase Beta sem depender de testes humanos

---

## 1. RESUMO EXECUTIVO

### 1.1 Estado Atual (pós-sync com origin/main)

O projeto Ilex Logística está **OPERACIONALMENTE COMPLETO** com todas as funcionalidades do roadmap implementadas:

- ✅ **113 testes de API** passando (pytest)
- ✅ **60 testes de Web** passando (vitest)
- ✅ **27 endpoints** implementados
- ✅ **11 telas** implementadas
- ✅ **6 migrations** aplicadas
- ✅ **Todos os LOGs (LOG-007 a LOG-029)** concluídos
- ✅ **PRs #1 a #5** mergeados em main

### 1.2 Gaps Identificados para Fase Beta

Apesar de operacionalmente completo, o projeto ainda depende de **validações manuais** que violam a regra "sem depender de testes humanos":

| Gap | Descrição | Impacto | Prioridade |
|-----|-----------|---------|------------|
| **Smoke UI Manual** | LOG-028 smoke UI foi validado manualmente por Rafael | 🔴 Alta | Crítico |
| **Testes E2E Headless** | Não há testes E2E automatizados do fluxo completo | 🔴 Alta | Crítico |
| **Cobertura de Testes** | Cobertura não medida ativamente | 🟡 Média | Importante |
| **Scripts de Smoke/CI** | Smoke não automatizado em CI | 🟡 Média | Importante |
| **Validação de Secrets** | Secrets não verificados sistematicamente | 🟡 Média | Importante |
| **Testes de Migrations** | Migrations não testadas em rollback | 🟢 Baixa | Desejável |

### 1.3 Estratégia de Execução

Transformar todas as validações manuais em **testes automatizados** seguindo TDD estrito:

1. **Red:** Criar teste automatizado que falha (ou que valida o comportamento esperado)
2. **Green:** Implementar o mínimo para passar (ou ajustar infraestrutura)
3. **Refactor:** Limpar sem quebrar testes

---

## 2. DIVISÃO DE PRs

### PR #BETA-001: Smoke UI Automatizado (Playwright)

**Objetivo:** Automatizar o smoke UI que foi realizado manualmente no LOG-028

**Branch:** `feature/beta-smoke-ui-automatizado`  
**Base:** `origin/main`  
**Tipo:** Draft PR

**Escopo:**
- Adicionar Playwright ao projeto Web
- Criar testes E2E headless para fluxo de promoção Delivery → Shipment
- Cobrir todos os 16 itens do checklist do LOG-028
- Mockar serviços externos (não usar APIs reais)

**Arquivos a criar/modificar:**
- `apps/web/package.json` - Adicionar @playwright/test
- `apps/web/playwright.config.ts` - Configuração do Playwright
- `apps/web/e2e/smoke-promocao-delivery-shipment.spec.ts` - Testes E2E
- `apps/web/e2e/fixtures/auth.fixture.ts` - Fixture de autenticação
- `apps/web/e2e/fixtures/api.fixture.ts` - Fixture de API mockada

**Cenários de Teste:**
1. Login com usuário autorizado
2. Navegação para listagem de deliveries
3. Acesso ao detalhe de uma delivery
4. Confirmação de dados da delivery
5. Abertura da seção "Promover para Shipment"
6. Confirmação de carregamento do select de transportadora
7. Seleção de transportadora
8. Preenchimento de campos obrigatórios
9. Submissão da promoção
10. Confirmação de mensagem de sucesso
11. Confirmação de dados do Shipment criado
12. Teste de erro com tracking_code duplicado
13. Teste de erro com campo obrigatório vazio
14. Confirmação de que Delivery original permanece acessível
15. Confirmação de que não aparece stack trace na UI

**Dependências:**
- Nenhuma (executa isoladamente)

**Riscos de Sobrescrita:**
- Baixo - arquivos novos em `apps/web/e2e/`
- Moderado - `apps/web/package.json` (adicionar dependência)

**Comandos de Validação:**
```bash
cd apps/web
npm install
npx playwright install --with-deps
npm run test:e2e  # Novo script
```

---

### PR #BETA-002: Scripts de Smoke/CI

**Objetivo:** Automatizar execução de smoke tests em CI

**Branch:** `feature/beta-smoke-ci-scripts`  
**Base:** `origin/main`  
**Tipo:** Draft PR

**Escopo:**
- Criar script de smoke para API
- Criar script de smoke para Web
- Integrar smoke nos workflows de CI
- Adicionar verificação de secrets

**Arquivos a criar/modificar:**
- `apps/api/scripts/smoke_api.py` - Script de smoke API
- `apps/web/scripts/smoke_web.sh` - Script de smoke Web
- `apps/api/.github/workflows/api-ci.yml` - Adicionar step de smoke
- `apps/web/.github/workflows/web-ci.yml` - Adicionar step de smoke
- `scripts/verify_secrets.sh` - Script de verificação de secrets

**Cenários de Teste:**
1. Smoke API: health check, login, listagem de deliveries
2. Smoke Web: build, health check da aplicação
3. Verificação de secrets: scanner de hardcoded secrets

**Dependências:**
- PR #BETA-001 (para smoke Web completo)

**Riscos de Sobrescrita:**
- Baixo - arquivos novos em `scripts/`
- Moderado - workflows de CI (adicionar steps)

**Comandos de Validação:**
```bash
cd apps/api
python scripts/smoke_api.py

cd apps/web
bash scripts/smoke_web.sh

bash scripts/verify_secrets.sh
```

---

### PR #BETA-003: Cobertura de Testes e Relatórios

**Objetivo:** Ativar medição de cobertura e gerar relatórios

**Branch:** `feature/beta-test-coverage`  
**Base:** `origin/main`  
**Tipo:** Draft PR

**Escopo:**
- Ativar coverage no pytest (API)
- Ativar coverage no vitest (Web)
- Configurar threshold mínimo de cobertura
- Gerar relatórios de cobertura em HTML
- Integrar coverage nos workflows de CI

**Arquivos a criar/modificar:**
- `apps/api/pyproject.toml` - Adicionar pytest-cov
- `apps/web/package.json` - Configurar vitest coverage
- `apps/api/.github/workflows/api-ci.yml` - Adicionar step de coverage
- `apps/web/.github/workflows/web-ci.yml` - Adicionar step de coverage
- `.github/workflows/coverage-report.yml` - Workflow de relatório

**Cenários de Teste:**
1. Executar testes com coverage
2. Verificar threshold mínimo (80%)
3. Gerar relatório HTML
4. Falhar CI se coverage < threshold

**Dependências:**
- Nenhuma (executa isoladamente)

**Riscos de Sobrescrita:**
- Baixo - arquivos de configuração
- Moderado - workflows de CI (adicionar steps)

**Comandos de Validação:**
```bash
cd apps/api
pytest --cov=app --cov-report=html --cov-fail-under=80

cd apps/web
npm run test -- --coverage
```

---

### PR #BETA-004: Testes de Migrations e Rollback

**Objetivo:** Testar migrations em rollback para garantir segurança

**Branch:** `feature/beta-migration-tests`  
**Base:** `origin/main`  
**Tipo:** Draft PR

**Escopo:**
- Criar testes de rollback de migrations
- Testar upgrade + downgrade cycle
- Garantir que dados não são perdidos
- Documentar procedimento de rollback seguro

**Arquivos a criar/modificar:**
- `apps/api/tests/test_migration_rollback.py` - Testes de rollback
- `apps/api/scripts/test_migration_cycle.sh` - Script de ciclo completo
- `docs/ops/migration-rollback-procedure.md` - Documentação

**Cenários de Teste:**
1. Upgrade para head
2. Verificar dados
3. Downgrade -1
4. Verificar dados
5. Upgrade novamente
6. Verificar dados

**Dependências:**
- Nenhuma (executa isoladamente)

**Riscos de Sobrescrita:**
- Baixo - arquivos novos
- Nenhum risco de dados (ambiente de teste)

**Comandos de Validação:**
```bash
cd apps/api
pytest tests/test_migration_rollback.py
bash scripts/test_migration_cycle.sh
```

---

### PR #BETA-005: Documentação Final e Checklists

**Objetivo:** Documentar gaps pós-beta e procedimentos operacionais

**Branch:** `feature/beta-documentation-final`  
**Base:** `origin/main`  
**Tipo:** Draft PR

**Escopo:**
- Documentar gaps pós-beta (LOG-A04, CI/CD)
- Criar checklist de operação beta
- Documentar procedimentos de emergência
- Atualizar README com comandos de smoke

**Arquivos a criar/modificar:**
- `docs/BETA_GAPS_POST_BETA.md` - Gaps pós-beta
- `docs/BETA_OPERATION_CHECKLIST.md` - Checklist operacional
- `docs/BETA_EMERGENCY_PROCEDURES.md` - Procedimentos de emergência
- `README.md` - Adicionar seção de smoke tests

**Dependências:**
- PRs #BETA-001 a #BETA-004 (para referenciar implementações)

**Riscos de Sobrescrita:**
- Baixo - arquivos de documentação novos
- Moderado - README.md (adicionar seção)

**Comandos de Validação:**
```bash
# Apenas verificação de markdown
npx markdownlint docs/BETA_*.md
```

---

## 3. ORDEM DE EXECUÇÃO

### Sequência Recomendada

1. **PR #BETA-001** - Smoke UI Automatizado (Playwright)
   - Prioridade: 🔴 Crítica
   - Motivo: Elimina dependência de teste humano (LOG-028)
   - Tempo estimado: 2-3 horas

2. **PR #BETA-002** - Scripts de Smoke/CI
   - Prioridade: 🔴 Alta
   - Motivo: Automatiza validações em CI
   - Depende: #BETA-001
   - Tempo estimado: 1-2 horas

3. **PR #BETA-003** - Cobertura de Testes
   - Prioridade: 🟡 Média
   - Motivo: Melhora qualidade e visibilidade
   - Depende: Nenhuma
   - Tempo estimado: 1 hora

4. **PR #BETA-004** - Testes de Migrations
   - Prioridade: 🟢 Baixa
   - Motivo: Segurança adicional
   - Depende: Nenhuma
   - Tempo estimado: 1-2 horas

5. **PR #BETA-005** - Documentação Final
   - Prioridade: 🟡 Média
   - Motivo: Governança e operação
   - Depende: #BETA-001, #BETA-002, #BETA-003, #BETA-004
   - Tempo estimado: 1 hora

**Tempo Total Estimado:** 6-9 horas

---

## 4. COMANDOS DE VALIDAÇÃO POR PR

### PR #BETA-001

```bash
# Setup
cd apps/web
npm install
npx playwright install --with-deps

# Executar testes E2E
npm run test:e2e

# Executar em modo headless (default)
npm run test:e2e -- --headed

# Executar com debug
npm run test:e2e -- --debug

# Ver relatório
npx playwright show-report
```

### PR #BETA-002

```bash
# Smoke API
cd apps/api
python scripts/smoke_api.py

# Smoke Web
cd apps/web
bash scripts/smoke_web.sh

# Verificar secrets
bash scripts/verify_secrets.sh

# Validar workflows (local)
act push  # Se usar act para testar GitHub Actions localmente
```

### PR #BETA-003

```bash
# Coverage API
cd apps/api
pytest --cov=app --cov-report=html --cov-report=term --cov-fail-under=80

# Coverage Web
cd apps/web
npm run test -- --coverage

# Ver relatório HTML
# Abrir apps/api/htmlcov/index.html
# Abrir apps/web/coverage/index.html
```

### PR #BETA-004

```bash
# Testes de rollback
cd apps/api
pytest tests/test_migration_rollback.py

# Ciclo completo de migrations
bash scripts/test_migration_cycle.sh
```

### PR #BETA-005

```bash
# Verificar markdown
npx markdownlint docs/BETA_*.md

# Verificar links
npx markdown-link-check docs/BETA_*.md
```

---

## 5. RISCOS DE SOBRESCRITA

### Análise de Arquivos Compartilhados

| Arquivo | PRs que modificam | Risco | Estratégia |
|---------|-------------------|-------|------------|
| `apps/web/package.json` | #BETA-001, #BETA-003 | Moderado | Merge sequencial, verificar conflitos de dependências |
| `apps/api/.github/workflows/api-ci.yml` | #BETA-002, #BETA-003 | Moderado | Merge sequencial, adicionar steps sem conflito |
| `apps/web/.github/workflows/web-ci.yml` | #BETA-002, #BETA-003 | Moderado | Merge sequencial, adicionar steps sem conflito |
| `README.md` | #BETA-005 | Baixo | Apenas adicionar seção, baixo risco |
| `apps/api/pyproject.toml` | #BETA-003 | Baixo | Apenas adicionar dependência dev |

### Estratégia de Merge Seguro

1. **Manter origin/main atualizado:** Sempre sincronizar antes de criar branch
2. **Branches pequenas e focadas:** Cada PR tem escopo limitado
3. **Merge sequencial:** #BETA-001 → #BETA-002 → #BETA-003 → #BETA-004 → #BETA-005
4. **Rebase seguro:** Se houver conflito, fazer rebase com `--rebase-merges`
5. **Documentar conflitos:** Se conflito ambíguo, parar e documentar no PR

### Procedimento em Caso de Conflito

```bash
# 1. Sincronizar com origin/main
git fetch origin
git rebase origin/main

# 2. Se houver conflito:
git status  # Ver arquivos conflitantes
# Resolver conflitos manualmente
git add <arquivos>
git rebase --continue

# 3. Se conflito ambíguo:
git rebase --abort
# Documentar no PR e aguardar decisão humana
```

---

## 6. COMO FLUXOS MANUAIS SERÃO AUTOMATIZADOS

### 6.1 Smoke UI Manual (LOG-028)

**Estado Atual:**
- Checklist de 16 itens validado manualmente por Rafael
- Sem evidência automatizada
- Não repetível em CI

**Solução (PR #BETA-001):**
- Playwright E2E tests cobrem todos os 16 itens
- Executável em headless mode
- Integrável em CI
- Repetível e determinístico

**Mapeamento:**
| Item Manual | Teste Automatizado |
|-------------|-------------------|
| Abrir login | `test('login com usuario autorizado')` |
| Login com usuário autorizado | `test('login com usuario autorizado')` |
| Abrir listagem de deliveries | `test('navegacao para listagem de deliveries')` |
| Acessar detalhe de uma Delivery | `test('acesso ao detalhe de delivery')` |
| Confirmar dados da Delivery | `test('confirmacao de dados da delivery')` |
| Abrir seção "Promover para Shipment" | `test('abertura da secao de promocao')` |
| Confirmar carregamento do select | `test('carregamento do select de transportadora')` |
| Selecionar transportadora | `test('selecao de transportadora')` |
| Preencher campos obrigatórios | `test('preenchimento de campos obrigatorios')` |
| Submeter promoção | `test('submissao da promocao')` |
| Confirmar mensagem de sucesso | `test('confirmacao de mensagem de sucesso')` |
| Confirmar dados do Shipment criado | `test('confirmacao de dados do shipment criado')` |
| Testar erro com tracking_code duplicado | `test('erro com tracking_code duplicado')` |
| Testar erro com campo obrigatório vazio | `test('erro com campo obrigatorio vazio')` |
| Confirmar Delivery original acessível | `test('delivery original permanece acessivel')` |
| Confirmar sem stack trace na UI | `test('sem stack trace na ui')` |

### 6.2 Validação de Secrets

**Estado Atual:**
- Secrets não verificados sistematicamente
- Risco de commits acidentais com secrets

**Solução (PR #BETA-002):**
- Script `verify_secrets.sh` com trufflehog ou similar
- Executado em pre-commit hook
- Integração em CI

**Mapeamento:**
- Scanner de hardcoded secrets (API keys, tokens, passwords)
- Scanner de dados sensíveis (emails, CPFs, CNPJs)
- Scanner de credenciais de banco

### 6.3 Smoke Tests em CI

**Estado Atual:**
- Smoke executado manualmente
- Não integrado em CI

**Solução (PR #BETA-002):**
- Scripts de smoke automatizados
- Integração em workflows de CI
- Execução em cada PR

**Mapeamento:**
| Smoke Manual | Script Automatizado |
|--------------|-------------------|
| Verificar API rodando | `smoke_api.py` |
| Verificar Web rodando | `smoke_web.sh` |
| Verificar login | `smoke_api.py` |
| Verificar listagem | `smoke_api.py` |

---

## 7. CRITÉRIOS DE CONCLUSÃO GLOBAL

O projeto estará **100% completo para Fase Beta** quando:

### 7.1 Critérios Técnicos

- ✅ Todos os PRs #BETA-001 a #BETA-005 abertos como Draft PRs
- ✅ Todos os testes E2E headless passando (Playwright)
- ✅ Smoke scripts integrados em CI
- ✅ Coverage ativo com threshold ≥ 80%
- ✅ Testes de migrations passando
- ✅ Secrets verificados sistematicamente
- ✅ Documentação completa de gaps pós-beta

### 7.2 Critérios de Qualidade

- ✅ Nenhum teste humano como critério de aceite
- ✅ Todas as validações manuais transformadas em testes automatizados
- ✅ CI validando API, Web e Infra
- ✅ Migrations testadas em rollback
- ✅ Secrets verificados em pre-commit e CI

### 7.3 Critérios de Governança

- ✅ Todos os PRs em Draft (sem merge)
- ✅ Branches criadas a partir de origin/main atualizado
- ✅ Commits em pt-BR com Conventional Commits e ID beta
- ✅ Documentação atualizada com comportamentos cobertos por teste
- ✅ Nenhum segredo exposto em logs, fixtures, docs ou PRs

### 7.4 Critérios de Rastreabilidade

- ✅ Cada PR vinculado a um gap específico
- ✅ Cada teste vinculado a um requisito manual
- ✅ Documentação de gaps pós-beta clara
- ✅ Procedimentos de emergência documentados

---

## 8. GAPS PÓS-BETA (Documentados, não implementados)

### 8.1 LOG-A04 Docker/WSL2

**Status:** ⏳ Bloqueado por infraestrutura  
**Impacto:** Infraestrutura local  
**Planejamento:** Resolver quando WSL2/Hyper-V estiver disponível  
**Workaround:** Usar Docker Desktop ou ambiente cloud

### 8.2 CI/CD Avançado

**Status:** ⏳ Não implementado  
**Impacto:** DevOps  
**Planejamento:** Implementar pós-beta com:
- Deploy automatizado (staging/produção)
- Rollback automatizado
- Monitoramento e alertas
- Integração com serviços de cloud

### 8.3 Integrações com Transportadoras

**Status:** ⏳ Não implementado  
**Impacto:** Operações  
**Planejamento:** Implementar pós-beta com:
- Conectores de API de transportadoras
- Bots/scraping controlado
- Webhooks de atualização de status

### 8.4 Auditoria de Alterações

**Status:** ⏳ Não implementado  
**Impacto:** Compliance  
**Planejamento:** Implementar pós-beta com:
- Trilha de change log por usuário/ação
- Auditoria de alterações críticas
- Relatórios de compliance

---

## 9. PROCEDIMENTOS DE EMERGÊNCIA

### 9.1 Rollback de Migration

```bash
# 1. Identificar migration problemática
alembic history

# 2. Reverter para versão anterior
alembic downgrade <target>

# 3. Verificar dados
# (queries manuais ou scripts de verificação)

# 4. Se dados corrompidos:
# - Restaurar backup
# - Reaplicar migrations até versão segura
```

### 9.2 Rollback de Deploy

```bash
# 1. Identificar commit problemático
git log --oneline

# 2. Reverter para commit anterior
git revert <commit>
git push origin <branch>

# 3. Se reverter não for possível:
git reset --hard <commit-safe>
git push --force  # ÚLTIMO RECURSO
```

### 9.3 Recuperação de Secrets

```bash
# 1. Se secret exposto em commit:
# - Rotacionar secret imediatamente
# - Revogar access tokens
# - Invalidar sessões

# 2. Remover secret do histórico:
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <arquivo>" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (APENAS após rotação)
git push origin --force --all
```

---

## 10. REFERÊNCIAS

### 10.1 Documentação Existente

- `docs/qa/encerramento-roadmap-final.md` - Status final do roadmap
- `docs/qa/log-028-smoke-autenticado-promocao-delivery-shipment.md` - Smoke manual
- `docs/qa/log-029-encerramento-operacional-e-proxima-fase.md` - Próxima fase
- `apps/api/README.md` - Documentação da API
- `apps/web/README.md` - Documentação do Web
- `infra/LOCAL_SETUP.md` - Setup local

### 10.2 Comandos de Referência

```bash
# API
cd apps/api
python -m pytest -q
python -m ruff check .
uvicorn app.main:app --reload

# Web
cd apps/web
npm run dev
npm run test
npm run lint
npm run build

# Infra
cd infra
docker compose up -d
docker compose down
```

---

## 11. ASSINATURA

**Plano criado por:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ⏳ Aguardando aprovação humana  
**Próximo passo:** Abrir Draft PR inicial com este plano

---

**NOTA IMPORTANTE:** Este plano segue estritamente as regras absolutas:
- ✅ Nenhum merge em main, develop ou branch protegida
- ✅ Nenhum auto-merge habilitado
- ✅ Nenhum git push --force ou comando destrutivo
- ✅ Draft PRs pequenos e rastreáveis
- ✅ Sincronização com origin/main antes de iniciar trabalho
- ✅ Não sobrescrever atualizações existentes
- ✅ Não pedir teste humano como critério de aceite
- ✅ Não usar serviços externos reais em testes
- ✅ TDD obrigatório (Red-Green-Refactor)
- ✅ Centralizar regra de negócio em services/domínio
- ✅ Não expor secrets em logs, fixtures, docs ou PRs
- ✅ Atualizar documentação apenas quando comportamento coberto por teste
- ✅ Commits em pt-BR com Conventional Commits e ID beta
