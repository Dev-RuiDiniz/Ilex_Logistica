# BETA KNOWN LIMITATIONS

Limitações conhecidas do projeto Ilex Logística na fase beta.

## Cobertura

### Web Coverage Baixa
**Limitação:** Web coverage atual: 20.8%

**Impacto:** Baixa cobertura pode indicar falta de testes em componentes críticos

**Arquivos com Baixa Cobertura:**
- lib/api.ts - Baixa cobertura
- login/page.tsx - Baixa cobertura

**Mitigação:**
- Documentado em docs/BETA_TEST_COVERAGE_REPORT.md
- Prioridade pós-beta: aumentar cobertura
- Foco em componentes críticos primeiro

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Migrations

### Downgrade para Base Destrói Dados
**Limitação:** O comando `alembic downgrade base` destrói todas as tabelas e dados

**Impacto:** Perda de dados se rollback for executado sem backup

**Causa:** Comportamento esperado do Alembic por design

**Mitigação:**
- Documentado em docs/BETA_ROLLBACK.md
- Backup obrigatório antes de rollback
- Procedimento de restore documentado
- Validação de migrations antes de beta

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

### Preservação de Dados
**Limitação:** Não há validação de preservação real de dados

**Impacto:** Roundtrip downgrade/upgrade não garante preservação de dados

**Causa:** Downgrade para base destrói dados por design

**Mitigação:**
- Documentado em docs/BETA_ROLLBACK.md
- test_data_preservation valida roundtrip, não preservação
- Para preservação real, seriam necessárias migrations incrementais reversíveis

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Scripts

### Bash Wrappers Removidos
**Limitação:** Bash wrappers removidos ou não oficiais

**Impacto:** Comandos Bash não são recomendados para validação

**Causa:** Bash wrappers instáveis no Windows/Git Bash

**Mitigação:**
- Python oficial implementado
- scripts/validate_migrations.py (Python oficial)
- scripts/beta_validate.py (Python oficial)
- Documentação atualizada para usar Python oficial

**Status:** Limitação mitigada

---

## E2E

### Mocks de Autenticação
**Limitação:** Mocks E2E usados para autenticação/localStorage

**Impacto:** Testes não validam fluxo de autenticação real

**Causa:** Autenticação real depende de backend e banco

**Mitigação:**
- Documentado em docs/BETA_AUTOMATED_VALIDATION_MAP.md
- Testes marcados como skip para UI não implementada
- Prioridade pós-beta: implementar autenticação real em E2E

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

### Testes Marcados como Skip
**Limitação:** Testes marcados como skip para UI não implementada

**Impacto:** Cobertura de E2E incompleta

**Causa:** UI não implementada para alguns fluxos

**Mitigação:**
- Documentado em PR #8 (BETA-001-FIX)
- Prioridade pós-beta: implementar UI completa
- Prioridade pós-beta: remover skips

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Ambiente

### Validação Local Específica
**Limitação:** Algumas validações dependem de ambiente local específico

**Impacto:** Validação pode não funcionar em todos os ambientes

**Causa:** Dependências de ambiente (Python, Node.js, etc.)

**Mitigação:**
- Python oficial para máxima portabilidade
- Documentação clara de dependências
- Scripts de validação com detecção automática

**Status:** Limitação mitigada

---

## Segurança

### Secret Scan
**Limitação:** Secret scan pode ter falsos positivos

**Impacto:** Falsos positivos podem bloquear desenvolvimento

**Causa:** Padrões de detecção podem ser muito amplos

**Mitigação:**
- Allowlist configurada
- Self-test real implementado
- Revisão manual de falsos positivos

**Status:** Limitação mitigada

### RBAC Incompleto (BETA-020A) - RESOLVIDO EM BETA-020B
**Limitação:** Endpoints de Shipments, Imports, Carriers e Users não protegidos com RBAC granular

**Impacto:** Esses endpoints dependem apenas de autenticação JWT, sem verificação de permissão granular

**Causa:** Priorização de endpoints críticos (audit, reports, alerts, SLA) em BETA-020A

**Mitigação:**
- Documentado em docs/BETA_020A_SECURITY_RBAC_BACKEND_API.md
- BETA-020B: Proteger endpoints restantes
- Não há bypass de autenticação - apenas falta de verificação de permissão granular
- Testes existentes continuam funcionando sem RBAC granular

**Status:** Limitação resolvida em BETA-020B

### Frontend Testes Preexistentes (BETA-020B)
**Limitação:** 42 testes frontend falhando são preexistentes na base BETA-020A

**Impacto:** 268/310 testes frontend passando

**Causa:** Falhas são preexistentes, não causadas por BETA-020B ou autenticação de imports

**Mitigação:**
- Documentado em docs/BETA_020B_RBAC_OPERATIONAL_ENDPOINTS_BACKEND.md
- Comparação executada: BETA-020A (base) vs BETA-020B mostrou mesma quantidade de falhas
- Falhas são em componentes não relacionados a imports (SlaBadge, dashboard, alerts, audit, exceptions)
- 7 errors de lint preexistentes corrigidos (any → unknown em types.ts)
- BETA-020C: Corrigir testes frontend preexistentes

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Performance

### Não Monitorada
**Limitação:** Performance não é monitorada

**Impacto:** Gargalos de performance podem não ser detectados

**Causa:** Ferramentas de monitoramento não implementadas

**Mitigação:**
- Prioridade pós-beta: implementar monitoramento
- Prioridade pós-beta: implementar profiling

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Acessibilidade

### Não Implementada
**Limitação:** Acessibilidade não é implementada

**Impacto:** Usuários com deficiências podem ter dificuldades

**Causa:** Prioridade não definida para acessibilidade

**Mitigação:**
- Prioridade pós-beta: implementar acessibilidade
- Prioridade pós-beta: testar com screen readers
- Prioridade pós-beta: validar contraste

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Internacionalização

### Não Implementada
**Limitação:** Internacionalização não é implementada

**Impacto:** Aplicação limitada a um idioma

**Causa:** Prioridade não definida para internacionalização

**Mitigação:**
- Prioridade pós-beta: implementar i18n
- Prioridade pós-beta: suporte a múltiplos idiomas
- Prioridade pós-beta: formatação localizada

**Status:** Limitação documentada

---

## BETA-021A — QA/CI/CD Final e Readiness Beta

**Status:** Sem limitações críticas

**Limitações Restantes:**
- check_secrets: 1 falso positivo em validate_docs.py (documentado)
- lint frontend: 12 warnings preexistentes (não críticas)
- Pydantic deprecation warnings (não críticas)

**Correções Aplicadas:**
- scripts/validate_web.sh: npm test → npm run test (correção para Web CI)

---

## BETA-021B — Auditoria Final de Integração e Release Candidate

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- Git push funciona (autenticação SSH)
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- PRs pendentes por bloqueio técnico de credencial GitHub. Deve ser criado pela IA/agente assim que houver credencial técnica válida disponível.

---

## BETA-021C — Preparação Automatizada dos PRs Pendentes e Pacote Final de Integração

**Status:** Sem limitações críticas

**Limitações Restantes:**
- Credencial GitHub: não disponível (bloqueio técnico documentado)
- PRs pendentes: BETA-021A e BETA-021B sem PR por bloqueio técnico

**Mitigação:**
- Bloqueio documentado em docs/BETA_021A_PR_BLOQUEIO.md
- Bloqueio documentado em docs/BETA_021B_PR_BLOQUEIO.md
- PR bodies versionados em docs/prs/
- Comentários finais versionados em docs/prs/
- Script auxiliar seguro (scripts/prepare_pending_prs.py)
- Pacote final de integração consolidado em docs/BETA_021C_PENDING_PRS_INTEGRATION_PACKAGE.md

---



## Resumo de Limitações

| Categoria | Limitação | Impacto | Mitigação | Status |
|-----------|-----------|---------|-----------|--------|
| Cobertura | Web coverage baixa (20.8%) | Médio | Documentado, prioridade pós-beta | Documentado |
| Migrations | Downgrade destrói dados | Alto | Backup obrigatório, documentado | Documentado |
| Migrations | Não valida preservação de dados | Médio | Documentado, migrations incrementais | Documentado |
| Scripts | Bash wrappers instáveis | Baixo | Python oficial implementado | Mitigado |
| E2E | Mocks de autenticação | Médio | Documentado, prioridade pós-beta | Documentado |
| E2E | Testes marcados como skip | Baixo | Documentado, prioridade pós-beta | Documentado |
| Ambiente | Validação local específica | Baixo | Python oficial, documentado | Mitigado |
| Segurança | Secret scan falsos positivos | Baixo | Allowlist, self-test real | Mitigado |
| Performance | Não monitorada | Médio | Prioridade pós-beta | Documentado |
| Acessibilidade | Não implementada | Médio | Prioridade pós-beta | Documentado |
| Internacionalização | Não implementada | Baixo | Prioridade pós-beta | Documentado |

---

## Próximas Ações

### Pós-Beta
1. Aumentar cobertura Web (foco em lib/api.ts e login/page.tsx)
2. Implementar migrations incrementais reversíveis
3. Implementar autenticação real em E2E
4. Implementar UI completa (remover skips)
5. Implementar monitoramento de performance
6. Implementar acessibilidade
7. Implementar internacionalização

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** 🔄 Em execução (BETA-009S - Revalidação Empilhada)
