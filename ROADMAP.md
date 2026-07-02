# ROADMAP.md — Conclusão do Ilex Logística por SDD

**Atualizado em:** 2026-07-02
**Marco de conclusão:** MVP assistido completo, homologado e preparado para produção
**Método:** spec antes do código; TDD RED/GREEN/REFACTOR; evidência antes de status

## 0. Legenda de status

- [x] **Concluído** — código, testes e gate aplicável aprovados com evidência fresca.
- [ ] **Pendente** — não iniciado, em andamento ou sem evidência de aceite.
- [~] **Parcial** — existe implementação, mas falta aceite, homologação ou cobertura.

## 1. Regras de execução

- Executar fases na ordem; P0 bloqueia todo trabalho funcional novo.
- Cada item começa pela atualização da spec e termina com documentação/evidência.
- **Confirmado** exige código, testes e gate aplicável; **homologado** exige aceite operacional.
- Um commit por tarefa, em pt-BR, conforme `AGENTS.md`.
- Integrações automáticas externas ficam pós-MVP até existirem contratos homologados.

## 2. Visão das fases

| Fase | Objetivo | Saída obrigatória | Status |
|---|---|---|---|
| P0 | recuperar baseline verde | testes, lint, build, migrations, infra e CI verdes | [x] Concluído |
| P1 | homologar monitoramento | LOG-027–035 aceitos com dados controlados | [~] Parcial |
| P2 | endurecer operação | alertas, relatórios, auditoria, RBAC e Braspress confiáveis | [~] Parcial |
| P3 | entregar cotação assistida | LOG-036–040 completos via CSV/XLSX | [ ] Pendente |
| P4 | preparar produção | segurança, desempenho, E2E, backup e deploy validados | [ ] Pendente |
| P5 | encerrar e homologar | aceite, release e go-live documentados | [ ] Pendente |

## 3. P0 — Recuperar baseline verde

**Estado em 2026-07-02:** P0 concluído. Gates locais e workflows remotos de Web, API e governança estão verdes; a `main` exige os três checks estritos e bloqueia force-push/exclusão, com bypass administrativo para manutenção explícita.

### P0.1 Web build e runtime — SPEC-03/SPEC-04  `[x]`

- [x] **Evidência:** import ausente e filtro de NF indefinido.
- [x] **RED:** testes reproduzem import/execução e estado dos filtros.
- [x] **GREEN:** corrigir imports e inicialização mínima sem alterar contrato.
- [x] **Aceite:** página abre; `npm test`, lint e build avançam sem esses erros.

### P0.2 Suíte Web e lint  `[x]`

- [x] Agrupar as 74 falhas por causa raiz: navegação/rótulos, dashboard, filtros e mocks.
- [x] Corrigir implementação quando divergir da spec; atualizar teste somente quando o comportamento aprovado mudou.
- [x] Remover `any`, dependências de hooks incorretas, imports/estados mortos e análise de artefatos de coverage.
- [x] **Gate:** zero falhas, zero erros ESLint e build aprovado.

### P0.3 Histórico Alembic único — SPEC-09/BANCO_DADOS  `[x]`

- [x] Especificar a relação entre as duas migrations de alert delivery logs.
- [x] Criar teste que falha com múltiplos heads.
- [x] Implementar merge/correção sem editar migration aplicada.
- [x] Validar banco novo, upgrade existente e downgrade seguro.
- [x] **Gate:** `validate_migrations.py` e testes de roundtrip aprovados com um head.

### P0.4 API determinística  `[x]`

- [x] Medir duração por teste e localizar travamento/lentidão.
- [x] Corrigir isolamento de SQLite, locks/journals e teardown de recursos.
- [x] Substituir testes-placeholder por casos RED reais ou removê-los com justificativa de cobertura.
- [x] Migrar configurações Pydantic depreciadas.
- [x] **Gate:** 664 testes executados em 72,52s, sem timeout e sem warnings deprecados conhecidos.

### P0.5 Infra e CI  `[x]`

- [x] Tornar `infra_checks` importável e corrigir testes para caminhos `apps/api` e `apps/web`.
- [x] Criar workflows para API, Web, migrations, docs, secrets e infra com cache apropriado.
- [x] Proteger branch contra merge com gate vermelho.
- [x] **Gate:** 5 testes infra locais aprovados e CI de PR aprovado (checks `api`, `web`, `governance`).

## 4. P1 — Homologar monitoramento LOG-027–035

### P1.1 Dados fiscais/financeiros — SPEC-04  `[x]`

- [x] LOG-027–031: validar NF, data de coleta, valor da NF, frete e percentual em import, API, lista, detalhe e exportação.
- [x] Cobrir nulos, zero, decimais, datas inválidas e compatibilidade com registros antigos.
- [x] **Aceite:** valores reconciliam com fixtures homologadas e nenhuma divisão inválida ocorre.

> **Evidência:** 17 testes API (decimal, datas inválidas, compat API, reconciliação com dataset), 15 testes Web (null/zero/undefined), bug corrigido em `get_shipment_detail` (campos fiscais ausentes). Dataset em `tests/fixtures/homologation_fiscal_financial.csv`.

### P1.2 Busca e filtros — SPEC-04  `[~]`

- [~] LOG-028/032/033: busca por NF, cliente, rastreio, UF e transportadora; filtros por status, cliente, transportadora, UF, mês, ano e todo período.
- [ ] Cobrir combinações, paginação, ordenação, limpeza, URL/estado e erro.
- [ ] **Aceite:** API e Web retornam o mesmo universo e Playwright cobre o fluxo crítico.

> **Evidência atual:** implementação parcial de busca e filtros existe na API e Web; aceite e E2E completos pendentes (ESCOPO.md §13, SPEC-04).

### P1.3 Eficiência e indicadores — SPEC-07/SPEC-08  `[~]`

- [~] LOG-034/035: reconciliar total, prazo, atraso, extravio, frete total e percentual médio.
- [~] Aplicar a mesma janela de filtros a listagem, KPIs e ranking.
- [ ] Homologar fórmula de SLA/eficiência com o cliente.
- [ ] **Aceite:** resultados batem com dataset de homologação e ranking é determinístico.

> **Evidência atual:** módulos de analytics e dashboard implementados; métricas complementares e homologação operacional pendentes (ESCOPO.md §13, SPEC-07 "Parcial/UAT pendente").

## 5. P2 — Endurecer a operação existente

### P2.1 Segurança e RBAC — SPEC-01  `[~]`

- [~] Cobrir todas as rotas/páginas com sucesso, `401` e `403`.
- [~] Integrar tratamento de sessão/acesso negado sem código morto.
- [ ] Definir política de senha, expiração, revogação/rotação e auditoria.

> **Evidência atual:** RBAC implementado com testes por módulo; tratamento 401/403 integrado no Web; hardening produtivo pendente (SPEC-01 "Parcialmente validado", AUDITORIA AUD-008).

### P2.2 Imports e Braspress — SPEC-03  `[~]`

- [ ] Implementar fixture XLSX Web e E2E de preview/confirm.
- [~] Homologar layout Braspress com amostra sanitizada e versionar mapper.
- [~] Validar tamanho, tipo, encoding, duplicidade, atomicidade e fórmulas perigosas.

> **Evidência atual:** mapper Braspress e testes API presentes; fixture XLSX Web marcada como TODO; E2E de preview/confirm pendente (SPEC-03 "Implementado; UAT pendente", AUDITORIA AUD-009).

### P2.3 Exceções e tratativas — SPEC-05/SPEC-06  `[~]`

- [ ] Substituir placeholders por testes de SLA/exceções reais.
- [~] Homologar taxonomia, autoria, ordenação e histórico.
- [ ] Cobrir painel → detalhe → tratativa em E2E.

> **Evidência atual:** módulo de tratativas implementado; `test_exceptions_panel_sla.py` contém testes-placeholder sem asserções efetivas; E2E pendente (SPEC-06 "Implementado; testes incompletos", AUDITORIA AUD-009).

### P2.4 Alertas, relatórios e auditoria — SPEC-09/10/11  `[~]`

- [~] Reconciliar UI e APIs, estados vazios/erro e permissões.
- [ ] Definir canais, retries, destinatários, agendamento e retenção ou marcar explicitamente fora do MVP.
- [~] Garantir sanitização e correlação de logs.
- [ ] **Gate P2:** suítes unitárias/integradas/E2E verdes e UAT operacional aprovado.

> **Evidência atual:** módulos de alertas, relatórios e auditoria implementados com testes; canais externos e retenção pendentes; UAT não realizado (SPEC-09 "Confirmado/Parcial", SPEC-10/11 "Implementado; UAT pendente").

## 6. P3 — MVP assistido de cotação LOG-036–040

### P3.1 Contrato e dados — SPEC-12  `[ ]`

- [ ] LOG-038: homologar layout mínimo do pedido ERP por CSV/XLSX.
- [ ] Definir `orders`, rodadas e `freight_quotes`, constraints, índices, status e auditoria.
- [ ] Criar migration reversível e contratos API antes da implementação.

> **Evidência atual:** SPEC-12 criada; nenhuma migration, model ou rota de pedidos/cotações existe (SPEC-12 "Planejado", ARQUITETURA "Planejado").

### P3.2 Importação de pedidos — LOG-037  `[ ]`

- [ ] RED para arquivo válido, erro por linha, duplicidade e reimportação.
- [ ] GREEN com preview/confirm transacional e idempotente, reutilizando padrões da SPEC-03.

### P3.3 Motor comparativo — LOG-039/040  `[ ]`

- [ ] Registrar valor/status por transportadora sem perder falhas individuais.
- [ ] Regra inicial: menor valor válido; aplicar desempate definido na SPEC-12.
- [ ] Preservar rodadas, validade e explicação da melhor opção.

### P3.4 Experiência Web — LOG-036  `[ ]`

- [ ] Criar subaba/tela de pedidos, tabela comparativa, filtros, estados e histórico.
- [ ] Aplicar RBAC, acessibilidade, responsividade e E2E completo.
- [ ] **Gate P3:** pedido importado, comparação auditável e melhor opção determinística com UAT aprovado.

## 7. P4 — Prontidão de produção  `[ ]`

- [ ] Rejeitar JWT default fora de desenvolvimento; parametrizar CORS e validar secrets.
- [ ] Definir rate limiting, headers, política de sessão e dependências.
- [ ] Testar PostgreSQL real, backup, restore, migration e rollback.
- [ ] Estabelecer metas e testes de desempenho para imports, listagens e analytics.
- [ ] Validar acessibilidade e principais navegadores/resoluções.
- [ ] Instrumentar health, logs, métricas, alertas e runbooks sem dados sensíveis.
- [ ] Executar E2E autenticado completo em ambiente semelhante à produção.
- [ ] **Gate:** checklist de segurança, operação, continuidade e deploy aprovado.

## 8. P5 — Homologação e encerramento  `[ ]`

- [ ] Executar UAT por perfil com evidências e aceite formal.
- [ ] Fechar todas as specs do MVP como confirmadas/homologadas ou registrar exclusão aprovada.
- [ ] Atualizar escopo, arquitetura, banco, contexto, relatório e README comercial.
- [ ] Produzir release notes, plano de implantação, treinamento, suporte e rollback.
- [ ] Fazer release candidata, smoke pós-deploy e decisão de go-live.

## 9. Pós-MVP dependente de terceiros

- Integração automática com ERP.
- APIs de cotação/rastreio de transportadoras.
- Regras avançadas por prazo, eficiência, restrição e múltiplas moedas.
- Automação externa somente com contrato, sandbox, credenciais seguras e SLA do fornecedor.

## 10. Definition of Done do projeto

- [ ] P0 a P5 concluídas e evidenciadas. _(P0 concluído; P1–P5 pendentes)_
- [ ] Todas as specs do MVP homologadas. _(nenhuma homologada)_
- [x] API, Web, migrations, infra, docs e secrets verdes na CI. _(gates P0 aprovados em 2026-07-02; E2E e gates P4 pendentes)_
- [x] Um único head Alembic e restore/rollback testados. _(merge migration criada; roundtrip aprovado)_
- [ ] Nenhum erro crítico/alto aberto sem aceite formal de risco.
- [ ] UAT, segurança, operação e go-live aprovados.
