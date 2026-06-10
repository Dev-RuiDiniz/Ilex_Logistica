# AGENTS.md — Regras de Execucao para Agentes no Projeto Ilex Logistica

**Versao:** 1.0  
**Data:** 2026-06-10  
**Projeto:** Ilex Logistica Monorepo  
**Aplicavel a:** Todos os agentes/automacaoes que executam tarefas no repositorio

---

## 1. COMMIT POR TAREFA (PT/BR)

- **Um commit por tarefa concluida.** Nao acumular multiplas mudancas nao relacionadas no mesmo commit.
- **Mensagens em portugues (pt-BR)** seguindo as convencoes do projeto (convencional commits adaptado):
  - `feat:` nova funcionalidade
  - `fix:` correcao de bug
  - `docs:` documentacao
  - `test:` testes
  - `refactor:` refatoracao
  - `chore:` tarefas de infra, config, scripts
  - `ci:` mudancas em CI/CD
  - `style:` formatacao, sem mudanca logica
- **Formato obrigatorio:**
  ```
  <tipo>(<escopo>): <descricao curta em pt-BR>

  <corpo opcional com detalhes>
  ```
  Exemplo: `feat(api): adiciona endpoint de eficiencia por transportadora`
- **Escopos validos:** `api`, `web`, `infra`, `docs`, `scripts`, `ci`, `migrations`, `tests`

---

## 2. SDD + TDD EM TODAS AS TAREFAS

### SDD — Specification-Driven Development

1. **Antes de codificar**, o agente deve:
   - Compreender o requisito a partir da documentacao existente (`docs/`, ADRs, roadmaps)
   - Se o requisito nao estiver documentado, criar/escrever a especificacao primeiro
   - Definir criterios de aceite claros
   - Documentar decisoes arquiteturais se aplicavel (novo ADR ou atualizacao)

2. **A especificacao vive antes do codigo.** Nenhuma implementacao sem:
   - Descricao do problema/solucao
   - Entradas, saidas e comportamentos esperados
   - Regras de negocio aplicaveis

### TDD — Test-Driven Development

1. **Para toda nova funcionalidade ou correcao:**
   - Escrever o teste que falha primeiro (RED)
   - Implementar o codigo minimo para passar (GREEN)
   - Refatorar se necessario (REFACTOR)
2. **Backend (Python/FastAPI):**
   - Testes unitarios com `pytest`
   - Testes de integracao para endpoints
   - Testes de migration quando houver mudanca de schema
3. **Frontend (Next.js/TypeScript):**
   - Testes unitarios com `vitest` + `@testing-library/react`
   - Testes E2E com Playwright para fluxos criticos
4. **Metrica minima:** nao reduzir cobertura de testes sem justificativa documentada.

---

## 3. INTEGRIDADE TECNICA E VERACIDADE DE DADOS

- **Nunca gerar dados falsos** ou inventar informacoes em documentacao, testes ou codigo.
- **Nunca criar stubs ou mocks** que mascarem comportamentos reais sem indicar claramente que sao provisorios.
- **Verificar antes de afirmar:** se nao tiver certeza sobre uma funcao, parametro ou comportamento, usar ferramentas de busca/inspecao para confirmar.
- **Nao deixar o codigo quebrado:** toda mudanca deve manter a API funcional, o build do Web passando e os testes existentes verdes.
- **Validar localmente antes de commitar:**
  - Backend: `cd apps/api && python -m pytest -q`
  - Frontend: `cd apps/web && npm test`
  - Migrations: `python scripts/validate_migrations.py`
  - Secret scan: `python scripts/check_secrets.py --repo-root . --self-test`

---

## 4. CONTEXTO DO PROJETO (CONTEXTO.md)

### Objetivo
Manter um registro vivo do estado do projeto, decisoes tomadas, arquitetura atual e pendencias.

### Regras de atualizacao
- **Atualizar a cada sessao de trabalho** ou quando houver mudanca significativa (nova feature, refactor, decisao arquitetural)
- **Nunca apagar informacao historica** — adicionar novas secoes no topo ou anexar, mantendo a linha do tempo
- **Conteudo obrigatorio:**
  - Estado atual do projeto (o que esta pronto, o que esta em andamento)
  - Decisoes arquiteturais recentes
  - Dependencias e bloqueios
  - Proximos passos pendentes
  - Notas tecnicas importantes

### Local
`c:\Users\RUI FRANCISCO\Documents\GitHub\Ilex_Logistica\CONTEXTO.md`

---

## 5. RELATORIO DO DIA (RELATORIO_DIA.md)

### Objetivo
Registrar diariamente o que foi feito, problemas encontrados e proximos passos.

### Regras de atualizacao
- **Atualizar no final de cada dia de trabalho** ou ao terminar uma sessao significativa
- **Criar nova secao por dia** com data no formato `YYYY-MM-DD`
- **Conteudo obrigatorio:**
  - Tarefas executadas (lista)
  - Arquivos modificados/criados
  - Testes adicionados ou atualizados
  - Bugs encontrados e correcoes aplicadas
  - Documentacao atualizada
  - Bloqueios ou dependencias
  - Proximos passos para o dia seguinte

### Local
`c:\Users\RUI FRANCISCO\Documents\GitHub\Ilex_Logistica\RELATORIO_DIA.md`

---

## 6. ATUALIZACAO DE DOCUMENTACAO

**Toda tarefa gera ou atualiza documentacao.** Nenhuma excecao.

### O que documentar:
- **Novas features:** criar documento em `docs/` descrevendo o que foi implementado, como usar e como testar
- **Mudancas de API:** atualizar documentacao de endpoints, contratos de request/response
- **Mudancas de schema:** atualizar documentacao de modelo de dados e migrations
- **Novas telas:** descrever a tela, fluxo de usuario e integracao com API
- **Correcoes de bug:** documentar causa raiz e solucao aplicada
- **Mudancas arquiteturais:** atualizar ADRs existentes ou criar novos

### Checklist de documentacao por tarefa:
- [ ] README atualizado se necessario
- [ ] Documentacao de feature criada/atualizada em `docs/`
- [ ] ADR atualizado se houver decisao arquitetural
- [ ] Comentarios de codigo adicionados apenas quando necessario (autoexplicativo e preferido)
- [ ] Changelog ou release notes atualizado se aplicavel

---

## 7. PUSH AO FINAL

- **Ao final de cada sessao de trabalho**, fazer push das alteracoes para o remoto
- **Branch de trabalho:** usar branches feature (`feature/<descricao>`) para novas tarefas; nunca commitar direto em `main` sem autorizacao explicita
- **Antes do push:**
  - [ ] Commit com mensagem em pt-BR conforme secao 1
  - [ ] Testes passando localmente
  - [ ] Secret scan limpo
  - [ ] Documentacao atualizada
  - [ ] `CONTEXTO.md` e `RELATORIO_DIA.md` atualizados
- **Fluxo:**
  1. `git add <arquivos da tarefa>`
  2. `git commit -m "<tipo>(<escopo>): <descricao>"`
  3. `git push origin <branch>`
  4. Se houver conflitos, resolver localmente e revalidar antes de finalizar

---

## 8. REGRAS GERAIS DE CONDUTA

- **Minimalismo:** preferir edicoes minimas e focadas. Evitar criar arquivos desnecessarios.
- **Buscar contexto:** sempre usar ferramentas de busca/inspecao para entender o codigo existente antes de modificar.
- **Nao assumir:** se algo nao esta claro, perguntar ao usuario ou investigar com ferramentas.
- **Seguranca:** nunca expor secrets, tokens ou credenciais. Validar com `check_secrets.py`.
- **Consistencia:** seguir padroes de codigo e estilo existentes no projeto (PEP 8, ruff, ESLint, Tailwind).
- **Nao deixar deveres pendentes:** se uma tarefa for grande demais para uma sessao, deixar a continuacao clara no `RELATORIO_DIA.md` e `CONTEXTO.md`.

---

**Assinatura:** Regras estabelecidas para execucao de agentes no projeto Ilex Logistica  
**Ultima atualizacao:** 2026-06-10
