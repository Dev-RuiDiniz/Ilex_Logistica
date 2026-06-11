# BETA RELEASE GATE

Gates objetivos para liberação beta do projeto Ilex Logistica.

## Status Atual

**BETA-025A (Retomada Automatizada de PRs Pendentes):** Bloqueado por falha de conectividade/autenticação GitHub API/MCP no runtime atual do agente. Git push/pull funciona, e refs de PRs podem ser listadas via Git, mas criação de PRs e comentários exige acesso HTTPS à GitHub API ou MCP GitHub funcional. O runtime atual não consegue conectar ao `api.github.com:443` (TCP 443 falha, DNS resolve corretamente) e/ou não consegue iniciar/conectar o `github-mcp-server`. O bloqueio é de conectividade de rede (firewall/rede), não de credencial. Nenhuma etapa operacional foi transferida ao usuário.

## Gates Obrigatórios

### 1. CI Verde

**Gate:** Nenhum PR beta pode ser mergeado sem CI verde.

**Validação:**
- Todos os workflows de CI passam
- Nenhum teste falha
- Nenhum erro de build
- Nenhum warning crítico

**Comando de Validação:**
```bash
gh workflow view <workflow-name>
gh run list --workflow=<workflow-name>
```

**Status:** Obrigatório

---

### 2. Validação Técnica Automatizada

**Gate:** Nenhum PR beta pode depender de teste manual para validação técnica.

**Validação:**
- Todos os testes são automatizados
- Nenhum teste manual é critério de aceite
- Validação é reproduzível
- Scripts de validação existem

**Comando de Validação:**
```bash
python scripts/beta_validate.py
```

**Status:** Obrigatório

---

### 3. Secret Scan

**Gate:** Nenhum PR beta pode expor secret.

**Validação:**
- Nenhum secret exposto no código
- Nenhum token exposto no código
- Nenhuma senha exposta no código
- Secret scan passa

**Comando de Validação:**
```bash
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test
```

**Status:** Obrigatório

---

### 4. Artefatos Gerados

**Gate:** Nenhum PR beta pode commitar artefatos gerados.

**Validação:**
- Nenhum artefato gerado no commit
- .gitignore configurado corretamente
- git status limpo após validação

**Comando de Validação:**
```bash
git status
git diff --cached
```

**Status:** Obrigatório

---

### 5. Migrations

**Gate:** Migrations precisam passar via comando oficial Python.

**Validação:**
- Migrations podem ser aplicadas até head
- Migrations podem ser revertidas
- Roundtrip funciona
- Tabelas críticas são recriadas

**Comando de Validação:**
```bash
python scripts/validate_migrations.py
```

**Alternativa:**
```bash
cd apps/api
python -m pytest tests/test_migrations.py -v
```

**Status:** Obrigatório

---

### 6. E2E

**Gate:** E2E precisa passar via Playwright.

**Validação:**
- Testes E2E implementados
- Testes E2E passam
- Playwright configurado
- Autenticação mockada

**Comando de Validação:**
```bash
cd apps/web
npx playwright test
```

**Status:** Obrigatório

---

### 7. Rollback

**Gate:** Rollback precisa estar documentado antes de beta.

**Validação:**
- Procedimento de rollback documentado
- Backup antes de rollback documentado
- Restore documentado
- Comandos Alembic corretos
- Validação por comando oficial

**Comando de Validação:**
```bash
# Verificar documentação
cat docs/BETA_ROLLBACK.md

# Validar migrations
python scripts/validate_migrations.py
```

**Status:** Obrigatório

---

### 8. PRs Draft

**Gate:** PRs devem permanecer Draft até revisão final.

**Validação:**
- Todos os PRs beta são Draft
- Nenhum PR beta tem auto-merge habilitado
- Nenhum PR beta foi mergeado
- Revisão de PR necessária

**Comando de Validação:**
```bash
gh pr list --draft
gh pr view <pr-number> --json autoMerge
```

**Status:** Obrigatório

---

### 9. Documentação

**Gate:** Documentação obrigatória deve existir.

**Validação:**
- docs/BETA_CHECKLIST.md existe
- docs/BETA_VALIDATION_EVIDENCE.md existe
- docs/BETA_COMMANDS.md existe
- docs/BETA_RELEASE_GATE.md existe
- docs/BETA_KNOWN_LIMITATIONS.md existe
- docs/BETA_NEXT_ACTIONS.md existe
- docs/BETA_ROLLBACK.md existe

**Comando de Validação:**
```bash
python scripts/validate_docs.py
```

**Status:** Obrigatório

---

### 10. Cobertura

**Gate:** Cobertura de testes deve ser aceitável.

**Validação:**
- API coverage: 88% (aceitável)
- Web coverage: 20.8% (limitação documentada)
- Relatórios de cobertura gerados
- Limitações conhecidas documentadas

**Comando de Validação:**
```bash
# API
cd apps/api
python -m pytest --cov=. --cov-report=xml

# Web
cd apps/web
npm run test:coverage
```

**Status:** Obrigatório (com limitações documentadas)

---

## Gates Opcionais

### 1. Performance

**Gate:** Performance deve ser aceitável.

**Validação:**
- Tempo de resposta aceitável
- Uso de memória aceitável
- Nenhum gargalo crítico

**Status:** Opcional (não implementado ainda)

---

### 2. Acessibilidade

**Gate:** Acessibilidade deve ser aceitável.

**Validação:**
- Contraste aceitável
- Navegação por teclado funciona
- Screen reader compatível

**Status:** Opcional (não implementado ainda)


### 3. Internacionalização

**Gate:** Internacionalização deve ser suportada.

**Validação:**
- Suporte a múltiplos idiomas
- Traduções funcionais
- Formatação de datas/horas localizada

**Status:** Opcional (não implementado ainda)

---

## Checklist de Liberação

### Antes de Merge

- [ ] CI verde em todos os PRs
- [ ] Validação técnica automatizada passando
- [ ] Secret scan passando
- [ ] Nenhum artefato gerado commitado
- [ ] Migrations passando via comando oficial
- [ ] E2E passando via Playwright
- [ ] Rollback documentado
- [ ] PRs Draft (sem auto-merge)
- [ ] Documentação obrigatória existe
- [ ] Cobertura aceitável (com limitações documentadas)

### Após Merge

- [ ] Branches beta deletadas
- [ ] Tags criadas (se aplicável)
- [ ] Release notes atualizadas
- [ ] Documentação final atualizada
- [ ] Comunicação com equipe

---

## Processo de Liberação

### 1. Revisão de PRs
- Revisar todos os PRs beta em ordem
- Verificar que todos os gates passam
- Validar documentação
- Confirmar CI verde

### 2. Resolução de Conflitos
- Resolver conflitos entre PRs
- Rebasear se necessário
- Validar novamente
- CI verde

### 3. Merge Planejado
- Merge manual planejado
- Ordem de merge definida
- Backup antes de merge
- Monitoramento após merge

---

## Riscos

### Risco 1: Conflitos entre PRs
- **Mitigação:** Revisão cuidadosa antes de merge
- **Plano B:** Rebase e resolução manual

### Risco 2: CI Instável
- **Mitigação:** Validação local antes de push
- **Plano B:** Rollback manual

### Risco 3: Migrations Falhando
- **Mitigação:** Validação de migrations antes de beta
- **Plano B:** Rollback para versão anterior

### Risco 4: E2E Falhando
- **Mitigação:** Validação de E2E antes de beta
- **Plano B:** Marcar testes como skip temporariamente

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** 🔄 Em execução (BETA-009S - Revalidação Empilhada)

**Nota:** Projeto tecnicamente conclu�do e release candidate em status GO. BETA-025A permanece bloqueada exclusivamente por falha de conectividade GitHub API/MCP no runtime atual do agente. Git push/pull funciona, mas cria��o de PRs e coment�rios exige conectividade HTTPS com pi.github.com:443 e autentica��o GitHub CLI/API/MCP funcional no mesmo processo do agente.
