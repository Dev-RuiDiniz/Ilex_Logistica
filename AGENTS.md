# AGENTS.md — Manual Operacional do Ilex Logística

**Versão:** 3.0
**Atualizado em:** 2026-07-02
**Escopo:** todo o monorepo

## 1. Finalidade

Este arquivo define como agentes de IA, automações e colaboradores devem investigar, especificar, implementar, testar, documentar e entregar mudanças no Ilex Logística. O objetivo é concluir o produto com alterações pequenas, verificáveis, seguras e rastreáveis, sem transformar intenção em fato nem apagar trabalho preexistente.

As instruções se aplicam à raiz e a todos os diretórios. Um `AGENTS.md` mais próximo do arquivo alterado pode acrescentar regras específicas, mas não pode reduzir segurança, SDD, TDD, validação ou documentação exigidos aqui. Em `apps/web`, respeitar também a regra local de consultar a documentação instalada do Next.js antes de usar APIs sujeitas a mudança.

## 2. Hierarquia e fontes de verdade

Em caso de divergência, usar esta ordem:

1. Instrução explícita e atual do usuário.
2. `AGENTS.md` aplicável ao caminho alterado.
3. Especificação aprovada em `docs/specs/` e critérios de aceite.
4. `ESCOPO.md`, `ROADMAP.md` e decisões registradas em `CONTEXTO.md`.
5. Código, migrations e configuração executável vigentes.
6. Testes automatizados e evidências de validação atuais.
7. Documentação histórica e comentários.

Quando código e spec divergirem, não escolher silenciosamente um lado: registrar a divergência, determinar se é defeito ou mudança de requisito e atualizar a fonte correta antes de prosseguir.

### 2.1 Estados documentais

- **Confirmado:** comportamento sustentado por evidência atual no repositório.
- **Parcial:** parte do comportamento existe, mas algum aceite ou integração falta.
- **Planejado:** comportamento desejado sem implementação identificada.
- **A confirmar:** depende de decisão de negócio ou informação externa.

Nunca declarar como concluído algo parcial, planejado ou não validado. Nunca inventar dados, endpoints, schemas, integrações, métricas, resultados de teste ou estado de produção.

## 3. Stack e fronteiras do monorepo

| Área | Caminho | Responsabilidade |
|---|---|---|
| API | `apps/api` | FastAPI, Pydantic, SQLAlchemy, regras de domínio e pytest |
| Web | `apps/web` | Next.js App Router, React, TypeScript, Tailwind, Vitest e Playwright |
| Banco | `apps/api/migrations` | Alembic e evolução versionada do schema |
| Infra | `infra` | Docker Compose, imagens, ambiente local e observabilidade |
| Specs | `docs/specs` | comportamento normativo e critérios de aceite SDD |
| Governança | raiz e `scripts` | escopo, contexto, roadmap, relatórios e gates |

Módulos confirmados da API: autenticação, usuários/RBAC, transportadoras, imports/deliveries, shipments/tratativas, SLA, dashboard, alertas, relatórios, auditoria e health. Pedidos ERP e cotações estão planejados na SPEC-12 e não devem ser tratados como implementados.

## 4. Fluxo obrigatório de toda tarefa

### 4.1 Antes de alterar

1. Ler o pedido, este arquivo e instruções locais aplicáveis.
2. Executar `git status --short`, confirmar branch e identificar alterações preexistentes.
3. Inspecionar os arquivos, testes, migrations, manifests e histórico relevantes.
4. Localizar a spec do domínio em `docs/specs/README.md`.
5. Confirmar objetivo, entradas, saídas, regras, aceite, riscos e dependências.
6. Se o requisito não estiver especificado, atualizar ou criar a spec antes do código.
7. Delimitar arquivos da tarefa e evitar refatorações sem relação com o objetivo.

Não restaurar, apagar, mover, formatar ou incluir no commit alterações do usuário sem autorização. Se o worktree estiver sujo, separar a tarefa por staging seletivo ou pedir direção quando houver sobreposição impossível de resolver com segurança.

### 4.2 Durante a implementação

1. Executar TDD em RED, GREEN e REFACTOR.
2. Fazer a menor mudança que satisfaz a spec.
3. Seguir padrões existentes de módulo, schema, service, router, página e testes.
4. Validar incrementalmente a área afetada.
5. Manter contratos, migrations e documentação sincronizados.
6. Registrar decisão arquitetural quando a mudança criar uma fronteira, dependência ou política duradoura.

### 4.3 Antes de concluir

1. Executar todos os gates proporcionais da seção 11.
2. Ler a saída completa; não inferir sucesso de comando parcial ou execução antiga.
3. Revisar `git diff` e `git diff --check`.
4. Atualizar documentação, `CONTEXTO.md` e `RELATORIO.md`.
5. Confirmar que critérios de aceite e rastreabilidade estão atendidos.
6. Criar um commit local focado em pt-BR.
7. Fazer push somente com autorização explícita do usuário.

## 5. SDD — Specification-Driven Development

Toda feature, correção com impacto de comportamento, mudança de contrato ou alteração arquitetural começa na spec.

### 5.1 Conteúdo mínimo da spec

- Identificador e estado.
- Objetivo, contexto e atores.
- Estado atual com evidências.
- Entradas, saídas e fluxo esperado.
- Regras de negócio e invariantes.
- Contratos de API/evento/arquivo quando aplicável.
- Dados, relacionamentos e migrations esperados.
- Permissões e requisitos de segurança.
- Estados vazios e falhas esperadas.
- Critérios de aceite verificáveis.
- Cenários TDD.
- Riscos, dependências e rastreabilidade com LOG-IDs.

Specs ficam em `docs/specs/`; o índice obrigatório é `docs/specs/README.md`. Mudança funcional deve atualizar a spec correspondente no mesmo commit. Um requisito planejado só passa para confirmado após código, testes e documentação fornecerem evidência.

### 5.2 Mudança de escopo

Atualizar `ESCOPO.md` quando houver inclusão, remoção ou mudança relevante de requisito, ator, regra ou limite. Atualizar `ROADMAP.md` quando prioridade, fase, dependência ou status mudar. Não ampliar escopo por conveniência técnica.

## 6. TDD — Test-Driven Development

Para feature e correção:

1. **RED:** escrever teste que falha pelo motivo esperado.
2. **GREEN:** implementar o mínimo para fazê-lo passar.
3. **REFACTOR:** melhorar estrutura mantendo a suíte verde.

Todo bug corrigido exige teste de regressão. Toda regra crítica, cálculo, permissão, endpoint, migration e fluxo de importação precisa de cobertura apropriada. Não remover ou enfraquecer teste para fazer a suíte passar. Mocks são permitidos somente em limites externos bem definidos e nunca para esconder comportamento real; documentar limitações relevantes.

Alterações exclusivamente documentais não exigem teste de produto, mas exigem validação documental, secret scan e revisão de diff.

## 7. Regras da API e domínio

- Manter separação vigente entre router, schemas, services e models.
- Schemas Pydantic são contratos: alteração incompatível exige spec, teste e estratégia de compatibilidade.
- Usar status HTTP coerentes e erros estruturados; não converter erro de domínio em `500` genérico.
- Rotas privadas devem testar sucesso, `401` e `403` conforme a matriz RBAC.
- Paginação, filtros e ordenação devem ocorrer server-side quando o volume puder crescer.
- Evitar N+1, consultas não limitadas e transações parciais.
- Não duplicar regra de negócio no Web; cálculos autoritativos pertencem à API/domínio.

### 7.1 Valores, datas e cálculos

- Valores monetários usam decimal, nunca ponto flutuante binário para persistência/cálculo financeiro.
- Divisões tratam base ausente ou zero explicitamente.
- Datas e timestamps têm semântica e timezone definidos no contrato; não misturar data local e UTC silenciosamente.
- Métricas informam população válida e não transformam ausência de dado em zero.

### 7.2 Imports e integrações

- Preview não deve persistir domínio.
- Confirmação precisa ser transacional, idempotente e reportar erro por linha.
- Validar tipo, tamanho, cabeçalhos, encoding, datas, valores e duplicidades.
- Não executar conteúdo ativo de planilhas nem confiar em fórmulas.
- Conectores externos precisam de timeout, retry controlado, idempotência, observabilidade e sanitização.
- Não automatizar captcha, contornar controle de portal ou assumir API não documentada.

## 8. Banco de dados e migrations

- Toda alteração de schema usa nova migration Alembic; não editar migration já aplicada.
- Atualizar model, migration, schema, teste e `BANCO_DADOS.md` juntos.
- Definir nulabilidade, default, foreign key, índice, constraint e estratégia para dados existentes.
- Testar upgrade e downgrade quando tecnicamente reversível.
- Mudança destrutiva exige plano de migração, backup/rollback e autorização explícita.
- Seeds devem ser identificados como demonstração/teste e não podem inserir credenciais reais.
- PostgreSQL é o alvo de Docker/produção; diferenças de SQLite precisam de teste ou documentação.

## 9. Regras do Web

- Respeitar App Router, React 19, TypeScript estrito e padrões existentes.
- Antes de usar API do Next.js sujeita a versão, consultar `apps/web/node_modules/next/dist/docs/`, conforme `apps/web/AGENTS.md`.
- Componentes devem tratar loading, vazio, erro, sucesso, `401` e `403`.
- Acessibilidade mínima: HTML semântico, labels, teclado, foco e feedback compreensível.
- Não expor secret nem depender de variável privada no bundle do cliente.
- Manter tipos e cliente da API alinhados ao contrato backend.
- Evitar fetch duplicado, estado derivado inconsistente e recomputação de regra de domínio.
- Fluxos críticos novos ou alterados exigem Playwright quando o ambiente estiver disponível.

## 10. Segurança, privacidade e auditoria

- Nunca ler para resposta, imprimir, documentar ou commitar secrets, tokens, senhas, chaves privadas ou `.env` real.
- Exemplos usam valores inequivocamente fictícios.
- Validar toda entrada no limite do sistema.
- Não criar backdoor, bypass de autenticação, permissão ampla temporária ou fallback inseguro.
- Logs não contêm token, senha, conteúdo integral de arquivo ou dado pessoal desnecessário.
- Ações críticas preservam autoria, timestamp, alvo e resultado quando previsto pela spec.
- Dependências novas exigem justificativa, compatibilidade e avaliação de manutenção/segurança.
- Achado crítico deve ser registrado em `CONTEXTO.md` sem detalhes exploráveis ou credenciais.

## 11. Matriz de validação

Executar na raiz, adaptando apenas o ambiente, nunca omitindo gate aplicável.

| Impacto | Validações mínimas |
|---|---|
| API/regra | `cd apps/api; python -m pytest -q` e `python -m ruff check .` |
| Web | `cd apps/web; npm test`, `npm run lint` e `npm run build` |
| Fluxo Web crítico | `cd apps/web; npm run test:e2e` com dependências disponíveis |
| Migration/model | testes API afetados, `python scripts/validate_migrations.py` e roundtrip aplicável |
| Infra | `python -m pytest -q infra/tests` e validação Docker aplicável |
| Documentação | `python scripts/validate_docs.py` |
| Qualquer commit | `python scripts/check_secrets.py --repo-root . --self-test` e `git diff --check` |

Comandos auxiliares existentes: `scripts/validate_api.sh`, `scripts/validate_web.sh`, `scripts/validate_e2e.sh`, `scripts/coverage_api.sh`, `scripts/coverage_web.sh` e `scripts/beta_validate.py`. Em Windows, prefira os comandos nativos acima quando Bash não estiver disponível.

Não declarar “passou”, “corrigido” ou “concluído” sem saída fresca do comando correspondente. Se um gate falhar por causa preexistente, registrar comando, erro e distinção entre falha preexistente e mudança da tarefa; não ocultar nem adulterar o gate.

## 12. Documentação obrigatória por impacto

| Arquivo | Atualizar quando |
|---|---|
| `docs/specs/<dominio>.md` | comportamento, regra, contrato, aceite ou estado mudar |
| `docs/specs/README.md` | spec, LOG-ID, estado ou rastreabilidade mudar |
| `ESCOPO.md` | requisito, ator, limite ou resultado do produto mudar |
| `ARQUITETURA.md` | módulo, fluxo, dependência ou integração estrutural mudar |
| `BANCO_DADOS.md` | model, tabela, migration, índice ou constraint mudar |
| `ROADMAP.md` | prioridade, fase, dependência ou status mudar |
| `CONTEXTO.md` | decisão, estado, risco, bloqueio ou próximo passo mudar |
| `RELATORIO.md` | ao final de toda sessão/tarefa significativa |
| `README.md` | instalação, execução ou visão pública mudar |

Preservar histórico útil em contexto/relatório. Não copiar alegações antigas sem verificar. Comentários de código explicam o “porquê” não óbvio; não substituem documentação nem repetem o código.

## 13. Git, branches, commits e push

### 13.1 Branches

- `feature/<descricao>` para funcionalidade.
- `fix/<descricao>` para correção.
- `chore/<descricao>` para manutenção/governança.
- Não iniciar desenvolvimento em `main` sem autorização explícita.
- Não usar `git reset --hard`, checkout destrutivo, force-push ou apagar branch sem autorização explícita.

### 13.2 Commits em pt-BR

Um commit local por tarefa concluída e validada. Não misturar mudanças não relacionadas. Usar staging seletivo e revisar o staged diff.

```text
<tipo>(<escopo>): <descrição curta em pt-BR>

<corpo opcional explicando motivo, impacto e decisões>
```

Tipos permitidos: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`, `ci`, `perf`, `build`, `revert`.

Escopos preferenciais: `api`, `web`, `auth`, `imports`, `shipments`, `sla`, `carriers`, `dashboard`, `alerts`, `reports`, `audit`, `banco`, `migrations`, `infra`, `docs`, `scripts`, `tests`, `ci`.

Exemplos:

```text
feat(shipments): adiciona busca por nota fiscal
fix(api): evita divisão por zero no percentual de frete
test(auth): cobre acesso negado por permissão
docs(docs): atualiza especificação de cotação
chore(infra): ajusta validação do ambiente local
```

Descrição curta no presente ou imperativo, específica e sem ponto final. O corpo deve explicar decisões não óbvias, não listar mecanicamente arquivos.

### 13.3 Push e integração

- Commit local é parte da conclusão normal da tarefa.
- Push, abertura de PR, merge, release ou deploy exigem autorização explícita do usuário.
- Antes do push, confirmar branch, upstream, commits a enviar e worktree limpo.
- Nunca commitar diretamente alterações de outra pessoa ou anexar arquivo fora do escopo só para “limpar” o status.

## 14. Definition of Done

Uma tarefa só está concluída quando:

- [ ] Requisito, spec e critérios de aceite estão claros e atualizados.
- [ ] Estado documental corresponde à evidência real.
- [ ] RED, GREEN e REFACTOR foram executados quando aplicável.
- [ ] API, Web, banco, segurança e compatibilidade foram avaliados.
- [ ] Gates proporcionais passaram ou bloqueio real foi documentado.
- [ ] Não há secrets, dados falsos, bypasses ou alterações alheias no diff.
- [ ] Documentação de impacto, contexto e relatório estão atualizados.
- [ ] Diff e staging foram revisados.
- [ ] Commit local único, focado e em pt-BR foi criado.
- [ ] Push só ocorreu mediante autorização explícita.

Se a tarefa não puder ser concluída, deixar o repositório utilizável, registrar o bloqueio com evidência e indicar o próximo passo concreto. Não declarar conclusão parcial como entrega final.
