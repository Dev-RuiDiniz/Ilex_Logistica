# ROADMAP.md — Conclusão do Ilex Logística por SDD

**Atualizado em:** 2026-07-02
**Marco de conclusão:** MVP assistido completo, homologado e preparado para produção
**Método:** spec antes do código; TDD RED/GREEN/REFACTOR; evidência antes de status

## 1. Regras de execução

- Executar fases na ordem; P0 bloqueia todo trabalho funcional novo.
- Cada item começa pela atualização da spec e termina com documentação/evidência.
- **Confirmado** exige código, testes e gate aplicável; **homologado** exige aceite operacional.
- Um commit por tarefa, em pt-BR, conforme `AGENTS.md`.
- Integrações automáticas externas ficam pós-MVP até existirem contratos homologados.

## 2. Visão das fases

| Fase | Objetivo | Saída obrigatória |
|---|---|---|
| P0 | recuperar baseline verde | testes, lint, build, migrations, infra e CI verdes |
| P1 | homologar monitoramento | LOG-027–035 aceitos com dados controlados |
| P2 | endurecer operação | alertas, relatórios, auditoria, RBAC e Braspress confiáveis |
| P3 | entregar cotação assistida | LOG-036–040 completos via CSV/XLSX |
| P4 | preparar produção | segurança, desempenho, E2E, backup e deploy validados |
| P5 | encerrar e homologar | aceite, release e go-live documentados |

## 3. P0 — Recuperar baseline verde

**Estado em 2026-07-02:** gates locais concluídos para Web, API, Alembic, infraestrutura e governança. Pendente apenas confirmar os workflows e aplicar os checks obrigatórios na `main` remota.

### P0.1 Web build e runtime — SPEC-03/SPEC-04

- **Evidência:** import ausente e filtro de NF indefinido.
- **RED:** testes reproduzem import/execução e estado dos filtros.
- **GREEN:** corrigir imports e inicialização mínima sem alterar contrato.
- **Aceite:** página abre; `npm test`, lint e build avançam sem esses erros.

### P0.2 Suíte Web e lint

- Agrupar as 74 falhas por causa raiz: navegação/rótulos, dashboard, filtros e mocks.
- Corrigir implementação quando divergir da spec; atualizar teste somente quando o comportamento aprovado mudou.
- Remover `any`, dependências de hooks incorretas, imports/estados mortos e análise de artefatos de coverage.
- **Gate:** zero falhas, zero erros ESLint e build aprovado.

### P0.3 Histórico Alembic único — SPEC-09/BANCO_DADOS

- Especificar a relação entre as duas migrations de alert delivery logs.
- Criar teste que falha com múltiplos heads.
- Implementar merge/correção sem editar migration aplicada.
- Validar banco novo, upgrade existente e downgrade seguro.
- **Gate:** `validate_migrations.py` e testes de roundtrip aprovados com um head.

### P0.4 API determinística

- Medir duração por teste e localizar travamento/lentidão.
- Corrigir isolamento de SQLite, locks/journals e teardown de recursos.
- Substituir testes-placeholder por casos RED reais ou removê-los com justificativa de cobertura.
- Migrar configurações Pydantic depreciadas.
- **Gate:** 659+ testes executados, sem timeout e sem warnings deprecados conhecidos.

### P0.5 Infra e CI

- Tornar `infra_checks` importável e corrigir testes para caminhos `apps/api` e `apps/web`.
- Criar workflows para API, Web, migrations, docs, secrets e infra com cache apropriado.
- Proteger branch contra merge com gate vermelho.
- **Gate:** testes infra locais e CI de PR aprovados.

## 4. P1 — Homologar monitoramento LOG-027–035

### P1.1 Dados fiscais/financeiros — SPEC-04

- LOG-027–031: validar NF, data de coleta, valor da NF, frete e percentual em import, API, lista, detalhe e exportação.
- Cobrir nulos, zero, decimais, datas inválidas e compatibilidade com registros antigos.
- **Aceite:** valores reconciliam com fixtures homologadas e nenhuma divisão inválida ocorre.

### P1.2 Busca e filtros — SPEC-04

- LOG-028/032/033: busca por NF, cliente, rastreio, UF e transportadora; filtros por status, cliente, transportadora, UF, mês, ano e todo período.
- Cobrir combinações, paginação, ordenação, limpeza, URL/estado e erro.
- **Aceite:** API e Web retornam o mesmo universo e Playwright cobre o fluxo crítico.

### P1.3 Eficiência e indicadores — SPEC-07/SPEC-08

- LOG-034/035: reconciliar total, prazo, atraso, extravio, frete total e percentual médio.
- Aplicar a mesma janela de filtros a listagem, KPIs e ranking.
- Homologar fórmula de SLA/eficiência com o cliente.
- **Aceite:** resultados batem com dataset de homologação e ranking é determinístico.

## 5. P2 — Endurecer a operação existente

### P2.1 Segurança e RBAC — SPEC-01

- Cobrir todas as rotas/páginas com sucesso, `401` e `403`.
- Integrar tratamento de sessão/acesso negado sem código morto.
- Definir política de senha, expiração, revogação/rotação e auditoria.

### P2.2 Imports e Braspress — SPEC-03

- Implementar fixture XLSX Web e E2E de preview/confirm.
- Homologar layout Braspress com amostra sanitizada e versionar mapper.
- Validar tamanho, tipo, encoding, duplicidade, atomicidade e fórmulas perigosas.

### P2.3 Exceções e tratativas — SPEC-05/SPEC-06

- Substituir placeholders por testes de SLA/exceções reais.
- Homologar taxonomia, autoria, ordenação e histórico.
- Cobrir painel → detalhe → tratativa em E2E.

### P2.4 Alertas, relatórios e auditoria — SPEC-09/10/11

- Reconciliar UI e APIs, estados vazios/erro e permissões.
- Definir canais, retries, destinatários, agendamento e retenção ou marcar explicitamente fora do MVP.
- Garantir sanitização e correlação de logs.
- **Gate P2:** suítes unitárias/integradas/E2E verdes e UAT operacional aprovado.

## 6. P3 — MVP assistido de cotação LOG-036–040

### P3.1 Contrato e dados — SPEC-12

- LOG-038: homologar layout mínimo do pedido ERP por CSV/XLSX.
- Definir `orders`, rodadas e `freight_quotes`, constraints, índices, status e auditoria.
- Criar migration reversível e contratos API antes da implementação.

### P3.2 Importação de pedidos — LOG-037

- RED para arquivo válido, erro por linha, duplicidade e reimportação.
- GREEN com preview/confirm transacional e idempotente, reutilizando padrões da SPEC-03.

### P3.3 Motor comparativo — LOG-039/040

- Registrar valor/status por transportadora sem perder falhas individuais.
- Regra inicial: menor valor válido; aplicar desempate definido na SPEC-12.
- Preservar rodadas, validade e explicação da melhor opção.

### P3.4 Experiência Web — LOG-036

- Criar subaba/tela de pedidos, tabela comparativa, filtros, estados e histórico.
- Aplicar RBAC, acessibilidade, responsividade e E2E completo.
- **Gate P3:** pedido importado, comparação auditável e melhor opção determinística com UAT aprovado.

## 7. P4 — Prontidão de produção

- Rejeitar JWT default fora de desenvolvimento; parametrizar CORS e validar secrets.
- Definir rate limiting, headers, política de sessão e dependências.
- Testar PostgreSQL real, backup, restore, migration e rollback.
- Estabelecer metas e testes de desempenho para imports, listagens e analytics.
- Validar acessibilidade e principais navegadores/resoluções.
- Instrumentar health, logs, métricas, alertas e runbooks sem dados sensíveis.
- Executar E2E autenticado completo em ambiente semelhante à produção.
- **Gate:** checklist de segurança, operação, continuidade e deploy aprovado.

## 8. P5 — Homologação e encerramento

- Executar UAT por perfil com evidências e aceite formal.
- Fechar todas as specs do MVP como confirmadas/homologadas ou registrar exclusão aprovada.
- Atualizar escopo, arquitetura, banco, contexto, relatório e README comercial.
- Produzir release notes, plano de implantação, treinamento, suporte e rollback.
- Fazer release candidata, smoke pós-deploy e decisão de go-live.

## 9. Pós-MVP dependente de terceiros

- Integração automática com ERP.
- APIs de cotação/rastreio de transportadoras.
- Regras avançadas por prazo, eficiência, restrição e múltiplas moedas.
- Automação externa somente com contrato, sandbox, credenciais seguras e SLA do fornecedor.

## 10. Definition of Done do projeto

- [ ] P0 a P5 concluídas e evidenciadas.
- [ ] Todas as specs do MVP homologadas.
- [ ] API, Web, E2E, migrations, infra, docs e secrets verdes na CI.
- [ ] Um único head Alembic e restore/rollback testados.
- [ ] Nenhum erro crítico/alto aberto sem aceite formal de risco.
- [ ] UAT, segurança, operação e go-live aprovados.
