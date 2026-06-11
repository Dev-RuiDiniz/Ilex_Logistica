# BETA-025B — Plano de Retomada Automatizada dos PRs Pendentes

## Pré-Condições para Retomada

A retomada automatizada dos PRs pendentes só deve ocorrer quando TODAS as pré-condições abaixo forem atendidas:

### 1. Conectividade GitHub API

**Comando de Validação:**
```bash
powershell -Command "Test-NetConnection api.github.com -Port 443"
```

**Critério de Sucesso:**
- `TcpTestSucceeded` deve ser `True`
- `PingSucceeded` pode ser `False` (ICMP pode estar bloqueado)

**Comando de Validação:**
```bash
powershell -Command "Invoke-WebRequest -Uri https://api.github.com/ -Method Head -UseBasicParsing"
```

**Critério de Sucesso:**
- Exit code 0
- Response header deve conter status 200

### 2. Autenticação GitHub CLI/API/MCP

**Opção A: GitHub CLI**
```bash
gh auth status
```

**Critério de Sucesso:**
- Output deve mostrar "Logged in to github.com"
- Não deve mostrar "You are not logged into any GitHub hosts"

**Opção B: Variável de Ambiente GH_TOKEN**
```bash
powershell -Command "Test-Path env:GH_TOKEN"
```

**Critério de Sucesso:**
- Output deve ser `True`

**Opção C: Variável de Ambiente GITHUB_TOKEN**
```bash
powershell -Command "Test-Path env:GITHUB_TOKEN"
```

**Critério de Sucesso:**
- Output deve ser `True`

**Opção D: MCP GitHub**
```bash
mcp_call_tool --server-name github-mcp-server --tool-name list_pull_requests --arguments '{"owner":"Dev-RuiDiniz","repo":"Ilex_Logistica","state":"open"}'
```

**Critério de Sucesso:**
- Não deve retornar "Failed to connect to MCP server 'github-mcp-server'"
- Deve retornar lista de PRs

### 3. Validação de API

**Comando de Validação:**
```bash
gh api repos/Dev-RuiDiniz/Ilex_Logistica
```

**Critério de Sucesso:**
- Exit code 0
- Deve retornar JSON com informações do repositório

**Comando de Validação:**
```bash
gh api repos/Dev-RuiDiniz/Ilex_Logistica/pulls --jq '.[].number'
```

**Critério de Sucesso:**
- Exit code 0
- Deve retornar lista de números de PRs

## Comandos de Validação de Conectividade

### Validação Completa de Conectividade e Autenticação

```bash
# 1. Validar DNS
powershell -Command "Resolve-DnsName api.github.com"

# 2. Validar TCP 443
powershell -Command "Test-NetConnection api.github.com -Port 443"

# 3. Validar HTTPS
powershell -Command "Invoke-WebRequest -Uri https://api.github.com/ -Method Head -UseBasicParsing"

# 4. Validar autenticação GitHub CLI
gh auth status

# 5. Validar variáveis de ambiente
powershell -Command "Test-Path env:GH_TOKEN"
powershell -Command "Test-Path env:GITHUB_TOKEN"

# 6. Validar MCP GitHub
mcp_call_tool --server-name github-mcp-server --tool-name list_pull_requests --arguments '{"owner":"Dev-RuiDiniz","repo":"Ilex_Logistica","state":"open"}'

# 7. Validar API
gh api repos/Dev-RuiDiniz/Ilex_Logistica
gh api repos/Dev-RuiDiniz/Ilex_Logistica/pulls --jq '.[].number'
```

## Ordem de Criação dos PRs

Devido à dependência de branches, a ordem segura de criação dos PRs empilhados é:

1. **BETA-021A** — QA CI/CD Beta Readiness
   - Branch: feature/beta-021a-qa-ci-cd-beta-readiness
   - Base: origin/main
   - Título: "BETA-021A: QA CI/CD Beta Readiness"
   - Status: Draft

2. **BETA-021B** — Final Integration Release Candidate
   - Branch: feature/beta-021b-final-integration-release-candidate
   - Base: feature/beta-021a-qa-ci-cd-beta-readiness
   - Título: "BETA-021B: Final Integration Release Candidate"
   - Status: Draft

3. **BETA-021C** — Pending PRs Integration Package
   - Branch: feature/beta-021c-pending-prs-integration-package
   - Base: feature/beta-021b-final-integration-release-candidate
   - Título: "BETA-021C: Pending PRs Integration Package"
   - Status: Draft

4. **BETA-022A** — Functional E2E Homologation
   - Branch: feature/beta-022a-functional-e2e-homologation
   - Base: feature/beta-021c-pending-prs-integration-package
   - Título: "BETA-022A: Functional E2E Homologation"
   - Status: Draft

5. **BETA-022B** — E2E Import Report Contract Hardening
   - Branch: feature/beta-022b-e2e-import-report-contract-hardening
   - Base: feature/beta-022a-functional-e2e-homologation
   - Título: "BETA-022B: E2E Import Report Contract Hardening"
   - Status: Draft

6. **BETA-023A** — Beta Delivery Runbook Handoff
   - Branch: feature/beta-023a-beta-delivery-runbook-handoff
   - Base: feature/beta-022b-e2e-import-report-contract-hardening
   - Título: "BETA-023A: Beta Delivery Runbook Handoff"
   - Status: Draft

7. **BETA-023B** — Release Candidate Manifest Freeze
   - Branch: feature/beta-023b-release-candidate-manifest-freeze
   - Base: feature/beta-023a-beta-delivery-runbook-handoff
   - Título: "BETA-023B: Release Candidate Manifest Freeze"
   - Status: Draft

8. **BETA-024A** — Safe Integration Simulation
   - Branch: feature/beta-024a-safe-integration-simulation
   - Base: origin/main
   - Título: "BETA-024A: Safe Integration Simulation"
   - Status: Draft
   - Nota: Pode ser criado em paralelo com BETA-021A

## Bases e Heads dos PRs

| PR | Head | Base |
|----|------|------|
| BETA-021A | feature/beta-021a-qa-ci-cd-beta-readiness | origin/main |
| BETA-021B | feature/beta-021b-final-integration-release-candidate | feature/beta-021a-qa-ci-cd-beta-readiness |
| BETA-021C | feature/beta-021c-pending-prs-integration-package | feature/beta-021b-final-integration-release-candidate |
| BETA-022A | feature/beta-022a-functional-e2e-homologation | feature/beta-021c-pending-prs-integration-package |
| BETA-022B | feature/beta-022b-e2e-import-report-contract-hardening | feature/beta-022a-functional-e2e-homologation |
| BETA-023A | feature/beta-023a-beta-delivery-runbook-handoff | feature/beta-022b-e2e-import-report-contract-hardening |
| BETA-023B | feature/beta-023b-release-candidate-manifest-freeze | feature/beta-023a-beta-delivery-runbook-handoff |
| BETA-024A | feature/beta-024a-safe-integration-simulation | origin/main |

## Política de Evitar Duplicidade

Antes de criar cada PR, verificar se já existe:

```bash
gh pr list --repo Dev-RuiDiniz/Ilex_Logistica --state open --json number,title,headRefName,baseRefName,isDraft,url
```

**Critério de Duplicidade:**
- Se `headRefName` já existir, não criar novo PR
- Se `title` já existir, não criar novo PR
- Se PR já existir, atualizar comentários finais em vez de criar novo PR

## Uso de Draft PR

Todos os PRs devem ser criados como Draft:

```bash
gh pr create --title "Título" --body "Descrição" --head <head> --base <base> --draft
```

**Motivo:**
- Evitar merge acidental
- Permite revisão antes de tornar ready
- Mantém PRs em estado de revisão

## Publicação de Comentários Finais

Após criar/atualizar cada PR, publicar comentário final:

```bash
gh pr comment <pr-number> --body "Comentário final"
```

**Conteúdo do Comentário Final:**
- Resumo do que foi implementado
- Evidência de validação (gates, backend, frontend)
- Limitações conhecidas
- Pendências antes de merge
- Referência para documentação relevante

## Proibição de Merge

**Regra Fixa:**
- Nenhum PR deve ser mergeado automaticamente
- Merge deve ser manual e aprovado pelo mantenedor
- Nenhum comando de merge deve ser executado pela IA/agente

## Proibição de Auto-Merge

**Regra Fixa:**
- Nenhum PR deve ter auto-merge habilitado
- Auto-merge deve ser desabilitado em todos os PRs
- Nenhum comando de auto-merge deve ser executado pela IA/agente

## Proibição de Force Push

**Regra Fixa:**
- Nenhum force push deve ser executado
- Force push só deve ser executado em caso de emergência e com aprovação explícita
- Nenhum comando de force push deve ser executado pela IA/agente

## Comandos de Criação de PRs

### Exemplo de Criação de PR (GitHub CLI)

```bash
gh pr create \
  --title "BETA-021A: QA CI/CD Beta Readiness" \
  --body "Descrição do PR" \
  --head feature/beta-021a-qa-ci-cd-beta-readiness \
  --base origin/main \
  --draft
```

### Exemplo de Criação de PR (MCP GitHub)

```bash
mcp_call_tool \
  --server-name github-mcp-server \
  --tool-name create_pull_request \
  --arguments '{"owner":"Dev-RuiDiniz","repo":"Ilex_Logistica","title":"BETA-021A: QA CI/CD Beta Readiness","body":"Descrição do PR","head":"feature/beta-021a-qa-ci-cd-beta-readiness","base":"origin/main","draft":true}'
```

## Critérios de Sucesso da Retomada

A retomada automatizada será considerada bem-sucedida quando:

1. Todos os PRs pendentes forem criados/atualizados
2. Todos os PRs estiverem em estado Draft
3. Todos os PRs tiverem comentários finais publicados
4. Nenhum PR tiver auto-merge habilitado
5. Nenhum PR tiver sido mergeado
6. Nenhum force push tiver sido executado
7. Documentação estiver atualizada com URLs dos PRs

## Critérios de Falha da Retomada

A retomada automatizada será considerada falha se:

1. Conectividade GitHub API falhar durante a criação de PRs
2. Autenticação GitHub CLI/API/MCP falhar durante a criação de PRs
3. Validação de API falhar durante a criação de PRs
4. Alguns PRs forem criados e outros não
5. PRs forem criados em ordem incorreta
6. PRs forem criados como ready em vez de draft
7. Auto-merge for habilitado em algum PR
8. Alguns PRs forem mergeados
9. Force push for executado

## Plano de Recuperação em Caso de Falha

Se a retomada automatizada falhar:

1. Documentar exatamente onde falhou
2. Documentar o erro exato
3. Documentar quais PRs foram criados e quais não
4. Documentar o estado dos PRs criados
5. Aguardar conectividade/autenticação ser restaurada
6. Retomar do ponto onde falhou
7. Não duplicar PRs já criados

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-11  
**Status:** 🔄 Em execução (BETA-025B - Plano de Retomada Automatizada dos PRs Pendentes)
