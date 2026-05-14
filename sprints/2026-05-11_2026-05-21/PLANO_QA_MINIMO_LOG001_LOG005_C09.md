# C-09 - Plano de QA mínimo para LOG-001..005

## Objetivo

Definir validação mínima, executável e rastreável para os itens LOG-001 a LOG-005 da Sprint 1 do Ilex Logística.

## Escopo

| Item | Foco de QA | Tipo de validação |
|---|---|---|
| LOG-001 | Organização inicial dos repositórios | Revisão estrutural e documentação |
| LOG-002 | Fundação da API | Testes automatizados e healthcheck |
| LOG-003 | Configuração de banco/migrations | Teste de migration e conexão |
| LOG-004 | Fundação do Web | Lint, testes e build |
| LOG-005 | Governança mínima de sprint | Templates, DoD e evidências |

## Estratégia

- Validar primeiro comandos automatizados.
- Registrar evidências por comando, resultado e data.
- Bloquear merge quando critério P0 falhar.
- Não validar deploy produtivo nesta sprint sem ambiente definido.

## Casos mínimos

| Caso | Item | Procedimento | Resultado esperado | Evidência |
|---|---|---|---|---|
| QA-001 | LOG-001 | Conferir repositórios `Api`, `Web`, `Infra`, `Docs`, `Integrations`, `.github` | Responsabilidades documentadas e branch da sprint criada | `git branch --show-current` e README |
| QA-002 | LOG-002 | Executar `python -m pytest -q` no `Api` | Suíte automatizada passa | Saída `11 passed` |
| QA-003 | LOG-002 | Acessar `/health` e `/api/v1/health` com API em execução | Resposta `{"status":"ok"}` | `curl` ou teste manual |
| QA-004 | LOG-003 | Executar `alembic upgrade head` contra banco local | Migrations aplicadas sem erro | Log do comando |
| QA-005 | LOG-003 | Subir banco via compose quando Docker disponível | PostgreSQL saudável | `docker compose ps` |
| QA-006 | LOG-004 | Executar `npm run lint` no `Web` | Lint sem erro | Log do comando |
| QA-007 | LOG-004 | Executar `npm run test` no `Web` | Testes passam | Saída Vitest |
| QA-008 | LOG-004 | Executar `npm run build` no `Web` | Build Next.js concluído | Log do build |
| QA-009 | LOG-005 | Criar issue/PR usando templates | Campos de ID, critérios e evidência disponíveis | Preview ou arquivo de template |
| QA-010 | LOG-005 | Revisar PR antes do merge | Checklist completo e sem merge automático | PR aberta aguardando revisão |

## Critérios de saída

- API com testes passando localmente e workflow criado.
- Web com lint, testes e build passando localmente e workflow criado.
- Infra com compose e templates de ambiente versionados.
- Riscos P0/P1 documentados.
- PR da Sprint C aberta para revisão técnica.

## Evidências já coletadas

- API: `python -m pytest -q` com 11 testes passando em validação local.
- Web: `npm run lint`, `npm run test` e `npm run build` concluídos em validação local.
- Docker: validação bloqueada por ausência do comando `docker` no workstation atual.

## Pendências

- Validar `docker compose config` e `docker compose up --build` em máquina com Docker disponível.
- Executar `npm audit` e triar vulnerabilidades moderadas do Web em tarefa separada.
