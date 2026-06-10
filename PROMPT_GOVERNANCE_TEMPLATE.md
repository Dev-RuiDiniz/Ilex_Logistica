# Prompt Template: Criar Sistema de Governanca (AGENTS.md + CONTEXTO.md + RELATORIO_DIA.md)

**Copie e cole este prompt em qualquer assistente de IA (Claude, ChatGPT, Cascade, etc.) para gerar os 3 arquivos de governanca em outro projeto.**

---

## Prompt

```
Crie 3 arquivos de governanca para o meu projeto de software. Eles devem ser criados na raiz do repositorio (ou em um diretorio `docs/` se preferir).

Os arquivos sao:
1. AGENTS.md — Regras de execucao para agentes/automacaoes
2. CONTEXTO.md — Estado vivo do projeto (arquitetura, bloqueios, proximos passos)
3. RELATORIO_DIA.md — Registro diario de atividades

---

## INSTRUCOES GERAIS

- Escreva TODO O CONTEUDO em portugues (pt-BR).
- Use Markdown puro (.md).
- Adapte os comandos de teste/build/validacao a stack do meu projeto (pergunte se nao souber).
- Mantenha o nivel de rigor e estrutura do modelo abaixo.

---

## ARQUIVO 1: AGENTS.md

Crie um arquivo chamado `AGENTS.md` com as seguintes 8 secoes obrigatorias:

### 1. COMMIT POR TAREFA (PT/BR)
- Um commit por tarefa concluida. Nao acumular multiplas mudancas nao relacionadas no mesmo commit.
- Mensagens em portugues (pt-BR) seguindo conventional commits adaptado:
  - `feat:` nova funcionalidade
  - `fix:` correcao de bug
  - `docs:` documentacao
  - `test:` testes
  - `refactor:` refatoracao
  - `chore:` tarefas de infra, config, scripts
  - `ci:` mudancas em CI/CD
  - `style:` formatacao, sem mudanca logica
- Formato obrigatorio:
  ```
  <tipo>(<escopo>): <descricao curta em pt-BR>

  <corpo opcional com detalhes>
  ```
  Exemplo: `feat(api): adiciona endpoint de autenticacao JWT`
- Defina escopos validos com base na estrutura do meu projeto.

### 2. SDD + TDD EM TODAS AS TAREFAS

#### SDD — Specification-Driven Development
- Antes de codificar, o agente deve:
  - Compreender o requisito a partir da documentacao existente (`docs/`, ADRs, roadmaps)
  - Se o requisito nao estiver documentado, criar/escrever a especificacao primeiro
  - Definir criterios de aceite claros
  - Documentar decisoes arquiteturais se aplicavel

#### TDD — Test-Driven Development
- Para toda nova funcionalidade ou correcao:
  - Escrever o teste que falha primeiro (RED)
  - Implementar o codigo minimo para passar (GREEN)
  - Refatorar se necessario (REFACTOR)
- Defina quais frameworks de teste usar com base na stack do projeto (ex: pytest, vitest, jest, go test).
- Defina metrica minima: nao reduzir cobertura de testes sem justificativa documentada.

### 3. INTEGRIDADE TECNICA E VERACIDADE DE DADOS
- Nunca gerar dados falsos ou inventar informacoes em documentacao, testes ou codigo.
- Nunca criar stubs ou mocks que mascarem comportamentos reais sem indicar claramente que sao provisorios.
- Verificar antes de afirmar: se nao tiver certeza, usar ferramentas de busca/inspecao para confirmar.
- Nao deixar o codigo quebrado: toda mudanca deve manter a API funcional, o build passando e os testes existentes verdes.
- Validar localmente antes de commitar (defina os comandos de teste/build especificos do projeto).

### 4. CONTEXTO DO PROJETO (CONTEXTO.md)
- Objetivo: manter um registro vivo do estado do projeto, decisoes tomadas, arquitetura atual e pendencias.
- Regras de atualizacao:
  - Atualizar a cada sessao de trabalho ou quando houver mudanca significativa
  - Nunca apagar informacao historica — adicionar novas secoes no topo ou anexar, mantendo a linha do tempo
  - Conteudo obrigatorio: estado atual do projeto, decisoes arquiteturais recentes, dependencias e bloqueios, proximos passos pendentes, notas tecnicas importantes
- Indique o caminho absoluto ou relativo onde o arquivo deve ficar.

### 5. RELATORIO DO DIA (RELATORIO_DIA.md)
- Objetivo: registrar diariamente o que foi feito, problemas encontrados e proximos passos.
- Regras de atualizacao:
  - Atualizar no final de cada dia de trabalho ou ao terminar uma sessao significativa
  - Criar nova secao por dia com data no formato `YYYY-MM-DD`
  - Conteudo obrigatorio:
    - Tarefas executadas (lista)
    - Arquivos modificados/criados
    - Testes adicionados ou atualizados
    - Bugs encontrados e correcoes aplicadas
    - Documentacao atualizada
    - Bloqueios ou dependencias
    - Proximos passos para o dia seguinte
- Indique o caminho absoluto ou relativo onde o arquivo deve ficar.

### 6. ATUALIZACAO DE DOCUMENTACAO
- Toda tarefa gera ou atualiza documentacao. Nenhuma excecao.
- O que documentar:
  - Novas features: criar documento em `docs/` descrevendo o que foi implementado, como usar e como testar
  - Mudancas de API: atualizar documentacao de endpoints, contratos de request/response
  - Mudancas de schema: atualizar documentacao de modelo de dados e migrations
  - Novas telas: descrever a tela, fluxo de usuario e integracao com API
  - Correcoes de bug: documentar causa raiz e solucao aplicada
  - Mudancas arquiteturais: atualizar ADRs existentes ou criar novos
- Checklist de documentacao por tarefa:
  - [ ] README atualizado se necessario
  - [ ] Documentacao de feature criada/atualizada em `docs/`
  - [ ] ADR atualizado se houver decisao arquitetural
  - [ ] Comentarios de codigo adicionados apenas quando necessario (autoexplicativo e preferido)
  - [ ] Changelog ou release notes atualizado se aplicavel

### 7. PUSH AO FINAL
- Ao final de cada sessao de trabalho, fazer push das alteracoes para o remoto.
- Branch de trabalho: usar branches feature (`feature/<descricao>`) para novas tarefas; nunca commitar direto em `main` sem autorizacao explicita.
- Antes do push checklist:
  - [ ] Commit com mensagem em pt-BR conforme secao 1
  - [ ] Testes passando localmente
  - [ ] Secret scan limpo
  - [ ] Documentacao atualizada
  - [ ] CONTEXTO.md e RELATORIO_DIA.md atualizados
- Fluxo:
  1. git add <arquivos da tarefa>
  2. git commit -m "<tipo>(<escopo>): <descricao>"
  3. git push origin <branch>
  4. Se houver conflitos, resolver localmente e revalidar antes de finalizar

### 8. REGRAS GERAIS DE CONDUTA
- Minimalismo: preferir edicoes minimas e focadas. Evitar criar arquivos desnecessarios.
- Buscar contexto: sempre usar ferramentas de busca/inspecao para entender o codigo existente antes de modificar.
- Nao assumir: se algo nao esta claro, perguntar ao usuario ou investigar com ferramentas.
- Seguranca: nunca expor secrets, tokens ou credenciais. Validar com scan de secrets.
- Consistencia: seguir padroes de codigo e estilo existentes no projeto.
- Nao deixar deveres pendentes: se uma tarefa for grande demais para uma sessao, deixar a continuacao clara no RELATORIO_DIA.md e CONTEXTO.md.

---

## ARQUIVO 2: CONTEXTO.md

Crie um arquivo chamado `CONTEXTO.md` com a seguinte estrutura:

```markdown
# CONTEXTO.md — Estado e Contexto do Projeto [NOME_DO_PROJETO]

**Atualizado em:** [DATA_ATUAL]

---

## Visao Geral Atual

[Descricao de 2-3 linhas do projeto: o que faz, stack tecnologica, arquitetura geral.]

**Fase atual:** [ex: MVP, Beta, Producao, Refatoracao, etc.]

---

## Estado dos Componentes

### Backend
- **Status:** [funcional/quebrado/em desenvolvimento]
- **Modulos prontos:** [lista]
- **Migrations:** [N versoes]
- **Testes:** [N passed, N failed]
- **Cobertura:** [%]

### Frontend
- **Status:** [build passando/quebrado]
- **Telas prontas:** [lista]
- **Testes:** [framework e status]
- **Cobertura:** [%]

### Infraestrutura
- **Docker/Compose:** [status]
- **CI/CD:** [status]
- **Scripts utilitarios:** [lista]

### Documentacao
- **Documentos em `docs/`:** [N aproximado]
- **Conflitos de merge:** [RESOLVIDOS/PENDENTES]

---

## Decisoes Arquiteturais Recentes

1. [Decisao 1 — breve descricao]
2. [Decisao 2 — breve descricao]

---

## Dependencias e Bloqueios

| Bloqueio | Severidade | Descricao |
|----------|-----------|-----------|
| [Bloqueio 1] | [CRITICO/ALTO/MEDIO/BAIXO] | [Descricao e status] |

---

## Proximos Passos Pendentes (Macro)

1. [Proximo passo 1]
2. [Proximo passo 2]
3. ...

---

## Notas Tecnicas

- **Banco dev:** [ex: SQLite, PostgreSQL, MongoDB]
- **Auth:** [ex: JWT, OAuth2, Session]
- **Padroes:** [ex: Clean Architecture, MVC, Hexagonal]

---

## Historico de Mudancas (Linha do Tempo)

### [YYYY-MM-DD] (Sessao completa)
- [Mudanca significativa 1]
- [Mudanca significativa 2]

### [YYYY-MM-DD] (Continuacao — [tema])
- [Mudanca significativa]

---

**Arquivo vivo — atualizar a cada sessao de trabalho**
```

Preencha com os dados reais do meu projeto (pergunte-me se nao souber algum dado).

---

## ARQUIVO 3: RELATORIO_DIA.md

Crie um arquivo chamado `RELATORIO_DIA.md` com a seguinte estrutura:

```markdown
# RELATORIO_DIA.md — Registro Diario de Atividades do projeto '[NOME_DO_PROJETO]'

---

## [YYYY-MM-DD]

### Tarefas Executadas

1. **[Descricao da tarefa]**
   - Detalhes do que foi feito
   - Resultado obtido

### Arquivos Modificados/Criados
- `caminho/arquivo.ext` — acao (criado/modificado/deletado)

### Testes
- Testes adicionados/atualizados: [modulo]
- Status: [passando/falhando]

### Documentacao Atualizada
- `docs/<arquivo>.md` — descricao da atualizacao

### Bugs Encontrados / Correcoes
- Descricao do bug e solucao aplicada

### Commit e Push
- **Commit:** `[tipo](escopo): descricao`
- **Hash:** `[hash]`
- **Push:** `[branch] -> [remote]`
- **Arquivos:** [N criados/modificados, N linhas inseridas/deletadas]

### Bloqueios
- Descricao do bloqueio e dependencia

### Proximos Passos
1. Proxima acao planejada

---

**Template para proximos dias:**

## YYYY-MM-DD

### Tarefas Executadas
- [ ] Descricao da tarefa e resultado

### Arquivos Modificados/Criados
- `caminho/arquivo.ext` — acao (criado/modificado/deletado)

### Testes
- Testes adicionados/atualizados: [modulo]
- Status: passando/falhando

### Documentacao Atualizada
- `docs/<arquivo>.md` — descricao da atualizacao

### Bugs Encontrados / Correcoes
- Descricao do bug e solucao aplicada

### Bloqueios
- Descricao do bloqueio e dependencia

### Proximos Passos
1. Proxima acao planejada
```

```

---

## COMO USAR ESTE PROMPT

1. **Copie** todo o texto acima (do `

```
` ao final).
2. **Cole** em qualquer assistente de IA com acesso ao seu projeto (Claude, ChatGPT, Cascade, etc.).
3. **Forneca contexto adicional** se o assistente perguntar sobre sua stack, estrutura de pastas ou estado atual.
4. **Revise** o resultado antes de salvar nos arquivos.
5. **Commite** os 3 arquivos juntos com a mensagem:
   ```
   docs(governance): adiciona sistema de governanca de agentes (AGENTS.md, CONTEXTO.md, RELATORIO_DIA.md)
   ```

---

**Origem:** Sistema de governanca do projeto Ilex Logistica
**Versao:** 1.0
**Data:** 2026-06-10
