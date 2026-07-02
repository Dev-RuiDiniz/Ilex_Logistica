# AUDITORIA.md — Estado Técnico do Ilex Logística

**Data da auditoria:** 2026-07-02
**Branch auditada:** `chore/governanca-agentes`
**Objetivo:** estabelecer o estado comprovado do repositório e orientar sua conclusão por SDD.

## 1. Sumário executivo

O repositório possui uma base funcional ampla, 12 specs de domínio, API modular, Web com telas operacionais, 659 testes Python coletáveis e infraestrutura Docker. Entretanto, o projeto **não está pronto para produção**: o Web não fecha testes, lint nem build; Alembic possui dois heads; os testes de infraestrutura não coletam pela forma documentada; CI não está ativa; e a execução completa da API não terminou dentro da janela observada.

Classificação atual: **MVP avançado em estabilização**.

| Dimensão | Estado | Severidade dominante |
|---|---|---|
| Documentação/SDD | Estruturada e validada | Baixa |
| API | Ampla cobertura coletada; suíte completa inconclusiva | Alta |
| Web | Testes, lint e build bloqueados | Crítica |
| Banco/migrations | Dois heads Alembic | Crítica |
| Infra/CI | Testes quebrados e workflows ausentes | Alta |
| Segurança | Base JWT/RBAC presente; configuração produtiva pendente | Alta |
| Operação/UAT | Regras externas e homologação pendentes | Alta |
| Cotação assistida | Especificada, não implementada | Planejada |

## 2. Método e limitações

A auditoria combinou inspeção de código, manifests, migrations, specs e execução dos gates disponíveis. Não foram utilizados dados reais, ambiente produtivo, credenciais externas ou integrações com ERP/transportadoras. Resultados “confirmados” significam evidência local, não homologação de produção.

O script `scripts/audit_beta_epics.py` foi considerado **não confiável para status executivo**: sua heurística depende de documentos removidos e classificou como ausentes módulos que existem no código. O JSON gerado por ele não foi mantido como evidência oficial.

## 3. Evidências executadas

| Comando/inspeção | Resultado observado |
|---|---|
| `python -m pytest --collect-only -q` em `apps/api` | 659 testes coletados; 3 avisos Pydantic |
| `python -m pytest -q` em `apps/api` | não concluiu dentro de aproximadamente 120 segundos |
| `npm test` em `apps/web` | 74 testes falhando antes do timeout |
| `npm run lint` | 7 erros e 50 avisos |
| `npm run build` | falhou por import inexistente `@/lib/error-handler` |
| `alembic heads` | dois heads: `20260620_02` e `20260627_01` |
| pytest de `infra/tests` a partir da raiz | 4 erros de importação de `infra_checks` |
| `python scripts/validate_docs.py` | aprovado |
| secret scan com self-test | aprovado |

## 4. Achados críticos

### AUD-001 — Web não compila

- **Evidência:** import inexistente em `shipments/import/page.tsx`.
- **Impacto:** não há artefato de produção confiável.
- **Ação:** criar teste de regressão/checagem de módulo, corrigir o import seguindo a API de erro vigente e executar testes, lint e build.

### AUD-002 — Erro de runtime na listagem de envios

- **Evidência:** `invoiceNumberFilter` é referenciado sem definição em `shipments/page.tsx`.
- **Impacto:** a página quebra e gera uma cascata de falhas nos testes de filtros.
- **Ação:** alinhar o estado dos filtros à SPEC-04 por TDD e revalidar todos os filtros fiscais/SLA.

### AUD-003 — Histórico Alembic bifurcado

- **Evidência:** dois heads ativos relacionados à evolução de alert delivery logs.
- **Impacto:** deploy/migration não possui caminho único.
- **Ação:** diagnosticar intenção das duas branches, criar migration de merge ou correção segura e testar upgrade/downgrade.

### AUD-004 — Baseline Web vermelho

- **Evidência:** 74 testes falhando; navegação espera rótulos antigos, dashboard e filtros apresentam falhas; lint tem 7 erros.
- **Impacto:** regressões não são distinguíveis de novas mudanças.
- **Ação:** corrigir por grupos causais, começando por runtime/build, depois contratos de UI/testes e lint.

## 5. Achados altos

### AUD-005 — Execução completa da API inconclusiva

659 testes são coletados, mas a suíte completa excedeu a janela observada. É necessário identificar teste lento/travado com tempos por teste, corrigir isolamento do banco e estabelecer limite reproduzível em CI.

### AUD-006 — Testes de infraestrutura não são portáveis

Os testes importam `infra_checks` sem um caminho de pacote estável e procuram workflows históricos em `Api/` e `Web/`, enquanto o monorepo atual usa `apps/`. O gate documentado no `AGENTS.md` precisa funcionar a partir da raiz.

### AUD-007 — CI/CD ausente

Não há workflow ativo em `.github/workflows`. Testes, lint, build, migrations, docs e secrets não são protegidos no remoto.

### AUD-008 — Configuração de segurança apenas para desenvolvimento

`jwt_secret` possui valor padrão local. Produção deve falhar de forma segura se o segredo não for fornecido. Origens CORS são fixas para localhost; configuração produtiva, rotação/revogação e rate limiting permanecem pendentes de decisão.

### AUD-009 — Testes-placeholder e dívida de qualidade

`test_exceptions_panel_sla.py` contém testes sem asserções efetivas (`pass`), e o fixture XLSX do Web está marcado como TODO. Esses itens não podem contar como cobertura.

## 6. Achados médios

- Schemas de audit/alerts usam configuração Pydantic v2 depreciada.
- ESLint analisa artefatos de coverage, gerando ruído; inputs/exclusões precisam ser corrigidos.
- Diversas páginas importam tratamento `401/403` sem utilizá-lo integralmente.
- Hooks possuem dependências incompletas e efeitos com atualizações síncronas sinalizadas pelo React.
- Regras de timezone, calendário útil, retenção e métricas operacionais seguem A CONFIRMAR.
- O status histórico “pronto para produção” não era sustentado pelos gates e foi removido da comunicação raiz.

## 7. Estado por domínio SDD

| Spec | Estado auditado | Lacuna principal |
|---|---|---|
| SPEC-01 Auth/RBAC | Parcialmente validada | hardening produtivo e E2E |
| SPEC-02 Transportadoras | Implementada, não homologada | UAT/RBAC ponta a ponta |
| SPEC-03 Imports/Braspress | Implementada, não homologada | XLSX Web e amostra operacional |
| SPEC-04 Entregas | Bloqueada | runtime, filtros e LOG-027–033 |
| SPEC-05 SLA | Implementada, regra a confirmar | homologação operacional |
| SPEC-06 Tratativas | Implementada, não homologada | E2E e taxonomia |
| SPEC-07 Eficiência | Parcial | reconciliação/LOG-034–035 |
| SPEC-08 Dashboard | Bloqueada por testes Web | consistência e filtros |
| SPEC-09 Alertas | Parcial | UI, canais e migration |
| SPEC-10 Relatórios | Parcial | UI/export/UAT |
| SPEC-11 Auditoria | Parcial | cobertura operacional e retenção |
| SPEC-12 Cotações | Planejada | implementação integral do MVP assistido |

## 8. Riscos para implantação

- Deploy com migration ambígua.
- Tela central de envios indisponível em runtime.
- Ausência de bloqueio automático de regressões no GitHub.
- Configuração local usada acidentalmente em produção.
- Indicadores divergirem da regra operacional ainda não homologada.
- Dependência de layouts externos sem contrato/versionamento.

## 9. Recomendação

Interromper novas funcionalidades até concluir a fase P0 do `ROADMAP.md`. Após baseline verde, homologar o monitoramento atual antes de iniciar cotações. O go-live depende dos gates P4/P5, incluindo segurança, migração única, E2E, UAT, backup e rollback.
