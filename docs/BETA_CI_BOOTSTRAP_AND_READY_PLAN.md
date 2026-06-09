# BETA CI BOOTSTRAP AND READY PLAN

Plano de bootstrap de CI base e conversão de Draft PRs para Ready para Review.

## 1. Por Que Este PR Existe

O BETA-007 concluiu a convergência dos PRs BETA-000 a BETA-006 e identificou que **nenhum PR beta tem CI verde**. Workflows de CI foram adicionados dentro dos próprios PRs, mas não foram configurados para rodar nas branches.

Antes de mergear vários PRs com mudanças em scripts, docs e workflows, precisamos de **CI base mínimo na branch principal** ou em uma branch de bootstrap, para validar os PRs seguintes de forma observável.

Este PR (BETA-008) cria um **bootstrap de CI base** usando os comandos Python oficiais consolidados no BETA-007, permitindo que os PRs BETA-000 a BETA-007 sejam revalidados com CI observável antes de qualquer merge funcional.

## 2. O Que Este PR Valida

Este PR valida:

1. **Secret Scan**
   - `python scripts/check_secrets.py --repo-root .`
   - `python scripts/check_secrets.py --repo-root . --self-test`

2. **Migrations**
   - `python scripts/validate_migrations.py`

3. **Documentação**
   - `python scripts/validate_docs.py`

4. **Validação Agregada**
   - `python scripts/beta_validate.py`

## 3. O Que Este PR Não Valida

Este PR **NÃO** valida:

1. **Playwright/E2E** - Será validado no PR #7 (BETA-001)
2. **Cobertura de Testes** - Será validado no PR #10 (BETA-003)
3. **API/Web Completos** - Serão validados nos PRs #7 e #10
4. **Features Funcionais** - Não há features funcionais neste PR
5. **SLA, Importação, Dashboard, Alertas** - Serão implementados em PRs posteriores

## 4. Comandos Oficiais do CI Base

### Comandos Python Oficiais
```bash
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/beta_validate.py
```

### Comandos Bash (Não Oficiais)
```bash
bash scripts/validate_api.sh  # ❌ Não oficial (instável)
bash scripts/validate_web.sh  # ❌ Não oficial (instável)
bash scripts/validate_e2e.sh  # ❌ Não oficial (instável)
bash scripts/validate_migrations.sh  # ❌ Não oficial (instável)
bash scripts/beta_validate.sh  # ❌ Não oficial (instável)
```

## 5. Como Revalidar Localmente

```bash
# Secret scan
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test

# Migrations
python scripts/validate_migrations.py

# Documentação
python scripts/validate_docs.py

# Validação agregada
python scripts/beta_validate.py
```

## 6. Critérios para Converter Cada Draft PR para Ready

### Pré-Condies Gerais
1. CI verde no PR
2. Secret scan passando
3. Migrations passando
4. Documentação consistente
5. Nenhum artefato gerado

### Critérios por PR

#### PR #6 - BETA-000 Plano de Execução
- [ ] CI verde
- [ ] Aprovação do plano pelo mantenedor
- [ ] Documentação consistente

#### PR #7 - BETA-001 Smoke UI Automatizado
- [ ] CI verde (incluindo Playwright)
- [ ] Playwright passando
- [ ] E2E passando
- [ ] Documentação consistente

#### PR #8 - BETA-001 Fix E2E
- [ ] **OBSOLETO** - Não converter para Ready
- [ ] Incorporado ao PR #7

#### PR #9 - BETA-002 Scripts de Smoke/CI
- [ ] CI verde
- [ ] Scripts Python oficiais passando
- [ ] Workflows usando comandos Python oficiais
- [ ] Documentação consistente

#### PR #10 - BETA-003 Cobertura
- [ ] CI verde
- [ ] Cobertura de testes passando
- [ ] Relatórios de cobertura gerados
- [ ] Documentação consistente

#### PR #11 - BETA-004 Migrations/Rollback
- [ ] CI verde
- [ ] Migrations passando
- [ ] Rollback documentado
- [ ] Documentação consistente

#### PR #12 - BETA-005 Docs/Checklists
- [ ] CI verde
- [ ] Documentação beta completa
- [ ] Comandos oficiais documentados
- [ ] Documentação consistente

#### PR #13 - BETA-006 Auditoria
- [ ] CI verde
- [ ] Relatório de auditoria completo
- [ ] Conflitos documentados
- [ ] Documentação consistente

#### PR #14 - BETA-007 Convergência
- [ ] CI verde
- [ ] Relatório de convergência completo
- [ ] Conflitos resolvidos
- [ ] Documentação consistente

#### PR #15 - BETA-008 CI Bootstrap
- [ ] CI verde
- [ ] Workflow beta-ci.yml passando
- [ ] Scripts Python oficiais passando
- [ ] Documentação de conversão Draft → Ready criada

## 7. Ordem Recomendada

### Fase 1: Bootstrap CI
1. **Merge Manual do BETA-008** (se aprovado pelo mantenedor)
   - Ativa CI base na branch principal
   - Permite validação observável dos PRs seguintes

### Fase 2: Rebase/Update dos PRs Beta
2. **Rebase/Update dos PRs BETA-000 a BETA-007**
   - Atualizar branches para incluir CI base
   - Validar CI verde em cada PR

### Fase 3: Conversão Draft → Ready
3. **Converter Draft → Ready somente com CI verde**
   - #6 BETA-000 (após aprovação do plano)
   - #7 BETA-001 (após CI verde)
   - #9 BETA-002 (após CI verde)
   - #10 BETA-003 (após CI verde)
   - #11 BETA-004 (após CI verde)
   - #12 BETA-005 (após CI verde)
   - #13 BETA-006 (após CI verde)
   - #14 BETA-007 (após CI verde)

### Fase 4: Merge Manual
4. **Merge manual na ordem recomendada**
   - #6 BETA-000
   - #7 BETA-001
   - #9 BETA-002
   - #10 BETA-003
   - #11 BETA-004
   - #12 BETA-005
   - #13 BETA-006
   - #14 BETA-007

## 8. Status do PR #8

**Status:** **OBSOLETO**
- Base branch é feature/beta-001-smoke-ui-playwright (não main)
- Poucos arquivos alterados (3 arquivos E2E)
- Fix do PR #7
- Recomendação: **Não mergear**
- Ação: Fechar apenas por decisão do mantenedor

## 9. Plano de Rollback

### Se CI Bootstrap Quebrar
1. **Reverter apenas este PR**
   - Revert commit do BETA-008
   - Remover workflow beta-ci.yml
   - Remover scripts Python oficiais
2. **Validar que main está funcional**
   - Validar que não há impacto em main
3. **Investigar causa**
   - Revisar logs de CI
   - Corrigir issue
4. **Reaplicar BETA-008**
   - Reaplicar com correção
   - Validar CI verde

### Se Merge dos PRs Beta Quebrar
1. **Rollback para tag de backup**
   - Criar tag de backup antes de merge
   - Revert para tag de backup
2. **Investigar causa**
   - Revisar logs de CI
   - Corrigir issue
3. **Rebase/Update PRs**
   - Atualizar PRs com correção
   - Validar CI verde
4. **Reaplicar merge**
   - Merge manual na ordem recomendada

## 10. Gates

### Gates Obrigatórios
1. ✅ **Nenhum PR beta sem CI verde**
   - CI deve ser verde antes de converter Draft → Ready
   - CI deve ser verde antes de merge

2. ✅ **Nenhum PR beta com secret**
   - Secret scan deve passar
   - Self-test real deve passar

3. ✅ **Nenhum PR beta com artefato gerado**
   - git status deve estar limpo
   - Nenhum artefato gerado commitado

4. ✅ **Nenhum PR beta com docs apontando para script removido**
   - Documentação não deve referenciar scripts removidos como oficiais
   - Documentação deve apontar para comandos Python oficiais

5. ✅ **Nenhum PR beta com validação humana como requisito técnico**
   - Validação técnica deve ser automatizada
   - Validação humana apenas para aprovação de plano

## 11. Workflow Beta CI

### Arquivo
`.github/workflows/beta-ci.yml`

### Triggers
- `pull_request` em branches `main`
- `push` em branches `main`

### Steps
1. Checkout code
2. Set up Python 3.11
3. Install dependencies (pytest, alembic)
4. Secret scan
5. Secret self-test
6. Validate migrations
7. Validate docs
8. Beta validation

### Características
- ✅ Usa comandos Python oficiais
- ✅ Não usa wrappers Bash instáveis
- ✅ Não depende de secrets
- ✅ Não depende de banco real
- ✅ Não publica artefatos sensíveis
- ✅ Funciona em CI Linux

## 12. Scripts Mínimos

### Scripts Criados
1. `scripts/check_secrets.py` - Wrapper Python para secret scan
2. `scripts/check_secrets_core.py` - Lógica real do secret scan com self-test
3. `scripts/validate_migrations.py` - Validação oficial de migrations
4. `scripts/validate_docs.py` - Validação documental automatizada
5. `scripts/beta_validate.py` - Validação beta agregada

### Características
- ✅ Portátil (Python)
- ✅ Output ASCII
- ✅ Exit code correto
- ✅ Não depende de caminhos locais
- ✅ Não vaza secrets
- ✅ Funciona em CI Linux

## 13. Validações Locais Obrigatórias

```bash
# Secret scan
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test

# Migrations
python scripts/validate_migrations.py

# Documentação
python scripts/validate_docs.py

# Validação agregada
python scripts/beta_validate.py

# Git status
git status
```

## 14. Próximos Passos

### Imediatos
1. Validar CI verde no BETA-008
2. Revisar workflow beta-ci.yml
3. Revisar scripts Python oficiais
4. Revisar documentação de conversão Draft → Ready

### Pós-Aprovação do BETA-008
1. Merge manual do BETA-008 (se aprovado)
2. Rebase/Update dos PRs BETA-000 a BETA-007
3. Validar CI verde em cada PR
4. Converter Draft → Ready com CI verde
5. Merge manual na ordem recomendada

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** 🔄 Em execução (BETA-008)
