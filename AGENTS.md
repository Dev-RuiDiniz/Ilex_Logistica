# AGENTS.md — Governança de Execução do Ilex Logística

**Versão:** 2.0
**Atualizado em:** 2026-07-02
**Aplicação:** agentes de IA, automações e colaboradores técnicos

## 1. Objetivo

Este arquivo define como investigar, especificar, implementar, testar, documentar e entregar mudanças no monorepo. As fontes de verdade são, nesta ordem: código e migrations; testes; documentação raiz; documentação específica ainda vigente; requisitos aprovados. Nunca transformar uma intenção em fato implementado sem evidência.

## 2. Princípios obrigatórios

- Inspecionar o repositório, o histórico e o estado do Git antes de alterar.
- Fazer mudanças pequenas, focadas e rastreáveis; não misturar tarefas.
- Preservar alterações preexistentes do usuário e não restaurar arquivos sem autorização.
- Atualizar documentação junto com código e registrar decisões no `CONTEXTO.md`.
- Não inventar endpoints, schemas, regras, integrações, métricas ou dados.
- Marcar incertezas como `A CONFIRMAR`, `PENDENTE DE VALIDAÇÃO` ou `NÃO IDENTIFICADO NO REPOSITÓRIO`.
- Não mascarar falhas com mocks, stubs ou fallbacks falsos.
- Nunca expor `.env`, tokens, senhas, chaves ou credenciais.
- Não deixar API, Web, migrations ou testes em estado quebrado.
- Não fazer commit ou push sem autorização explícita do usuário.

## 3. SDD — Specification-Driven Development

Antes de codificar:

1. Ler `ESCOPO.md`, `ROADMAP.md`, `CONTEXTO.md`, arquitetura, banco e documentação relacionada.
2. Confirmar problema, entradas, saídas, regras de negócio e limites.
3. Criar ou atualizar a especificação antes do código.
4. Definir critérios de aceite verificáveis.
5. Mapear impactos em arquitetura, banco, API, Web, testes, segurança e infraestrutura.
6. Registrar decisões relevantes no contexto e vincular a tarefa ao roadmap.

Uma especificação deve conter objetivo, contexto, regras, fluxo, critérios de aceite, impacto técnico, testes, riscos e dependências.

## 4. TDD — Test-Driven Development

Fluxo obrigatório para feature ou correção:

1. **RED:** criar teste que demonstra o comportamento ausente ou o bug.
2. **GREEN:** implementar o mínimo para passar.
3. **REFACTOR:** melhorar sem quebrar a suíte.

Toda regra crítica, endpoint e bug corrigido requer teste. Mudanças de schema requerem migration e validação. Não reduzir cobertura sem justificativa em `RELATORIO.md`.

Comandos reais:

```powershell
cd apps/api
python -m pytest -q

cd ../web
npm test
npm run lint
npm run build

cd ../..
python scripts/validate_migrations.py
python scripts/validate_docs.py
python scripts/check_secrets.py --repo-root . --self-test
```

Fluxos críticos do Web também devem usar `npm run test:e2e` quando o ambiente E2E estiver disponível.

## 5. Commits em pt-BR

Formato:

```text
<tipo>(<escopo>): <descrição curta em pt-BR>

<corpo opcional com motivo e impacto>
```

Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`, `ci`, `perf`, `build`, `revert`. Escopos usuais: `api`, `web`, `auth`, `banco`, `docs`, `infra`, `scripts`, `ci`, `migrations`, `tests`, `dashboard`.

- Um commit por tarefa concluída.
- Usar branch `feature/<descricao>`, `fix/<descricao>` ou `chore/<descricao>`; `main` exige autorização explícita.
- Validar testes, build, migrations, documentação e secrets antes do commit.
- Commit e push dependem de autorização explícita.

## 6. Documentação obrigatória

- `ARQUITETURA.md`: módulos, fluxos, integrações ou estrutura.
- `BANCO_DADOS.md`: models, tabelas, migrations, índices ou constraints.
- `ESCOPO.md`: requisitos, regras e limites.
- `ROADMAP.md`: fase, épico, prioridade, tarefa e aceite.
- `CONTEXTO.md`: estado, decisão, risco, bloqueio e próximo passo.
- `RELATORIO.md`: trabalho executado na sessão.

Checklist por tarefa:

- [ ] Requisito e evidências compreendidos
- [ ] Especificação e critérios de aceite atualizados
- [ ] Teste criado/ajustado em RED
- [ ] Implementação validada em GREEN
- [ ] Refatoração segura concluída
- [ ] Documentação de impacto atualizada
- [ ] Contexto e relatório atualizados
- [ ] Migrations, build e secrets validados quando aplicável

## 7. Segurança e integridade

Validar entradas, respeitar autenticação JWT e RBAC, não criar bypasses e não registrar dados sensíveis. Exemplos devem usar valores inequivocamente fictícios. Riscos críticos devem entrar no `CONTEXTO.md`. Alterações em permissões precisam de testes de acesso autorizado, `401` e `403`.

## 8. Conduta operacional

Preferir padrões existentes, não reescrever módulos sem necessidade, não substituir bibliotecas centrais sem decisão documentada e não remover testes. Investigar antes de perguntar; se a evidência continuar insuficiente, registrar a dúvida. Ao encontrar worktree sujo, separar alterações da tarefa e nunca sobrescrever trabalho alheio.
