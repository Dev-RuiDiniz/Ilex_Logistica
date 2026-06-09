# BETA NEXT ACTIONS

Próximas ações pós BETA-005 para o projeto Ilex Logística.

## Ações Imediatas (Antes de Merge dos PRs Beta)

### 1. Revisar Draft PRs na Ordem Correta
**Ordem Sugerida:**
1. PR #6: BETA-000 - Plano de Execução TDD Fase Beta
2. PR #7: BETA-001 - Smoke UI Automatizado com Playwright
3. PR #8: BETA-001-FIX - Marca Testes E2E como Skip
4. PR #9: BETA-002 - Scripts de Smoke/CI e Validação Beta Automatizada
5. PR #10: BETA-003 - Cobertura de Testes e Relatórios
6. PR #11: BETA-004 - Testes de Migrations e Rollback
7. PR #12: BETA-005 - Documentação Final, Checklists e Consolidação Beta

**Comando:**
```bash
gh pr list --draft
gh pr view <pr-number>
```

**Responsável:** Mantenedor
**Status:** Pendente

---

### 2. Garantir CI Verde em Todos os PRs
**Validação:**
- Todos os workflows de CI passam
- Nenhum teste falha
- Nenhum erro de build

**Comando:**
```bash
gh workflow list
gh run list --workflow=<workflow-name>
```

**Responsável:** Mantenedor
**Status:** Pendente

---

### 3. Resolver Conflitos Entre PRs
**Validação:**
- Nenhum conflito entre PRs
- Merge limpo possível
- Branches atualizadas

**Comando:**
```bash
git checkout <branch>
git pull origin main
git merge main
# Resolver conflitos se houver
git push
```

**Responsável:** Mantenedor
**Status:** Pendente

---

### 4. Validar Documentação
**Validação:**
- Documentos obrigatórios existem
- Documentos são consistentes entre si
- Comandos oficiais documentados
- Limitações conhecidas documentadas

**Comando:**
```bash
python scripts/validate_docs.py
```

**Responsável:** Mantenedor
**Status:** Pendente

---

## Ações de Merge (Se Aprovado pelo Mantenedor)

### 1. Merge Manual Planejado
**Processo:**
1. Merge PR #6 (BETA-000) primeiro
2. Merge PR #7 e PR #8 (BETA-001) juntos
3. Merge PR #9 (BETA-002)
4. Merge PR #10 (BETA-003)
5. Merge PR #11 (BETA-004)
6. Merge PR #12 (BETA-005)

**Comando:**
```bash
gh pr merge <pr-number> --merge --delete-branch
```

**Responsável:** Mantenedor
**Status:** Pendente aprovação

---

### 2. Backup Antes de Merge
**Processo:**
1. Criar tag de backup antes do merge
2. Documentar estado do repositório
3. Criar branch de fallback

**Comando:**
```bash
git tag pre-beta-backup-$(date +%Y%m%d_%H%M%S)
git push origin --tags
```

**Responsável:** Mantenedor
**Status:** Pendente

---

### 3. Monitoramento Após Merge
**Processo:**
1. Validar que CI verde após merge
2. Validar que documentação está correta
3. Validar que comandos funcionam
4. Comunicar com equipe

**Comando:**
```bash
gh run list
python scripts/beta_validate.py
```

**Responsável:** Mantenedor
**Status:** Pendente

---

## Ações Pós-Beta (Iniciar Roadmap Funcional Restante)

### 1. Aumentar Cobertura Web
**Objetivo:** Aumentar cobertura de 20.8% para pelo menos 50%

**Foco:**
- lib/api.ts
- login/page.tsx
- Componentes críticos

**Comando:**
```bash
cd apps/web
npm run test:coverage
```

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 2. Implementar Migrations Incrementais Reversíveis
**Objetivo:** Implementar migrations que preservam dados

**Foco:**
- Migrations incrementais
- Downgrade seguro
- Preservação de dados

**Comando:**
```bash
cd apps/api
python -m pytest tests/test_migrations.py -v
```

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 3. Implementar Autenticação Real em E2E
**Objetivo:** Implementar autenticação real em testes E2E

**Foco:**
- Autenticação real com backend
- Banco de dados real para E2E
- Remover mocks de localStorage

**Comando:**
```bash
cd apps/web
npx playwright test
```

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 4. Implementar UI Completa
**Objetivo:** Implementar UI para fluxos não implementados

**Foco:**
- Remover testes marcados como skip
- Implementar UI faltante
- Validar todos os fluxos

**Comando:**
```bash
cd apps/web
npx playwright test
```

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 5. Implementar Monitoramento de Performance
**Objetivo:** Implementar monitoramento de performance

**Foco:**
- Profiling de API
- Profiling de Web
- Alertas de gargalos

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 6. Implementar Acessibilidade
**Objetivo:** Implementar acessibilidade

**Foco:**
- Contraste
- Navegação por teclado
- Screen reader

**Responsável:** Desenvolvedor
**Status:** Pendente

---

### 7. Implementar Internacionalização
**Objetivo:** Implementar suporte a múltiplos idiomas

**Foco:**
- i18n
- Traduções
- Formatação localizada

**Responsável:** Desenvolvedor
**Status:** Pendente

---

## Ações de Manutenção

### 1. Atualizar Documentação
**Frequência:** Após cada merge significativo

**Tarefas:**
- Atualizar docs/BETA_CHECKLIST.md
- Atualizar docs/BETA_VALIDATION_EVIDENCE.md
- Atualizar docs/BETA_COMMANDS.md

**Responsável:** Desenvolvedor
**Status:** Recorrente

---

### 2. Manter CI Verde
**Frequência:** Contínua

**Tarefas:**
- Monitorar workflows
- Corrigir falhas
- Atualizar dependências

**Responsável:** Desenvolvedor
**Status:** Recorrente

---

### 3. Manter Secret Scan Passando
**Frequência:** Contínua

**Tarefas:**
- Rodar secret scan regularmente
- Revisar falsos positivos
- Atualizar allowlist se necessário

**Responsável:** Desenvolvedor
**Status:** Recorrente

---

## Ações de Comunicação

### 1. Comunicar com Equipe
**Frequência:** Após merge dos PRs beta

**Tarefas:**
- Comunicar estado beta
- Compartilhar documentação
- Compartilhar comandos oficiais

**Responsável:** Mantenedor
**Status:** Pendente

---

### 2. Documentar Decisões
**Frequência:** Após cada decisão significativa

**Tarefas:**
- Documentar decisões de arquitetura
- Documentar decisões de tecnologia
- Documentar decisões de processo

**Responsável:** Desenvolvedor
**Status:** Recorrente

---

## Resumo de Ações

| Ação | Responsável | Status | Prioridade |
|------|-------------|--------|-----------|
| Revisar Draft PRs | Mantenedor | Pendente | Alta |
| Garantir CI verde | Mantenedor | Pendente | Alta |
| Resolver conflitos | Mantenedor | Pendente | Alta |
| Validar documentação | Mantenedor | Pendente | Alta |
| Merge manual planejado | Mantenedor | Pendente aprovação | Alta |
| Backup antes de merge | Mantenedor | Pendente | Alta |
| Monitoramento após merge | Mantenedor | Pendente | Alta |
| Aumentar cobertura Web | Desenvolvedor | Pendente | Média |
| Migrations incrementais | Desenvolvedor | Pendente | Média |
| Autenticação real E2E | Desenvolvedor | Pendente | Média |
| UI completa | Desenvolvedor | Pendente | Média |
| Monitoramento performance | Desenvolvedor | Pendente | Baixa |
| Acessibilidade | Desenvolvedor | Pendente | Baixa |
| Internacionalização | Desenvolvedor | Pendente | Baixa |
| Atualizar documentação | Desenvolvedor | Recorrente | Média |
| Manter CI verde | Desenvolvedor | Recorrente | Alta |
| Manter secret scan | Desenvolvedor | Recorrente | Alta |
| Comunicar com equipe | Mantenedor | Pendente | Alta |
| Documentar decisões | Desenvolvedor | Recorrente | Média |

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** 🔄 Em execução (BETA-005)
