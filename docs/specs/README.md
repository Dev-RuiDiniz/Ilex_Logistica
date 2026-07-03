# Especificações SDD — Ilex Logística

**Atualizado em:** 2026-07-03

> Auditoria de 2026-07-02: “Confirmado” indica evidência estrutural no repositório, mas os módulos permanecem sujeitos ao baseline P0 e à homologação. Consulte `../../AUDITORIA.md` e `../../ROADMAP.md`.

## Uso

Estas specs definem o comportamento esperado antes da implementação. Para cada mudança: localizar a spec, atualizar regras e aceite, escrever teste RED, implementar GREEN, refatorar e registrar evidências. “Confirmado” significa evidência no repositório; não significa homologação de produção.

## Status

- **Confirmado:** código e testes relevantes identificados.
- **Parcial:** existe implementação, mas falta algum aceite ou homologação.
- **Planejado:** comportamento-alvo ainda sem implementação identificada.
- **A confirmar:** depende de decisão ou informação externa.

## Catálogo

| ID | Especificação | Estado |
|---|---|---|
| SPEC-01 | [Autenticação, usuários e RBAC](01-autenticacao-usuarios-rbac.md) | Confirmado tecnicamente; UAT pendente |
| SPEC-02 | [Transportadoras](02-transportadoras.md) | Implementado; UAT pendente |
| SPEC-03 | [Importações e Braspress](03-importacoes-braspress.md) | Implementado; UAT pendente |
| SPEC-04 | [Entregas monitoradas](04-entregas-monitoradas.md) | Implementado; UAT complementar pendente |
| SPEC-05 | [SLA e criticidade](05-sla-atrasos-criticidade.md) | Confirmado/A confirmar |
| SPEC-06 | [Tratativas e exceções](06-tratativas-excecoes.md) | Testes API confirmados; E2E integrado pendente |
| SPEC-07 | [Eficiência](07-eficiencia-transportadoras.md) | Confirmado por dataset; UAT humano pendente |
| SPEC-08 | [Dashboard](08-dashboard-indicadores.md) | Implementado; UAT pendente |
| SPEC-09 | [Alertas](09-alertas-notificacoes.md) | Confirmado/Parcial |
| SPEC-10 | [Relatórios](10-relatorios-exportacoes.md) | Implementado; UAT pendente |
| SPEC-11 | [Auditoria](11-auditoria-historico.md) | Implementado; UAT pendente |
| SPEC-12 | [Pedidos e cotações](12-pedidos-cotacao-frete.md) | Confirmado tecnicamente; UAT humano pendente |

## Rastreabilidade LOG-027 a LOG-041

| ID | Spec | Critério resumido |
|---|---|---|
| LOG-027 | SPEC-04 | campos fiscais/financeiros disponíveis na API e Web |
| LOG-028 | SPEC-04 | NF exibida, pesquisável e ordenável |
| LOG-029 | SPEC-04 | data de coleta importada, exibida e reportável |
| LOG-030 | SPEC-04 | frete em listagem, detalhe e exportação |
| LOG-031 | SPEC-04 | percentual calculado sem divisão por zero |
| LOG-032 | SPEC-04 | filtros combináveis por transportadora, cliente, UF e período |
| LOG-033 | SPEC-04 | busca por NF, cliente, rastreio, UF e transportadora |
| LOG-034 | SPEC-07 | quadro de eficiência por transportadora |
| LOG-035 | SPEC-07/SPEC-08 | indicadores recalculados pelo período |
| LOG-036 | SPEC-12 | subaba de cotação por pedido |
| LOG-037 | SPEC-12/SPEC-03 | importação assistida de pedidos ERP |
| LOG-038 | SPEC-12 | contrato mínimo de integração ERP |
| LOG-039 | SPEC-12 | motor comparativo por pedido |
| LOG-040 | SPEC-12 | melhor opção por regra configurável |
| LOG-041 | SPEC-03 | fluxo Braspress sem credenciais |

## Cobertura de implementação

| Área do repositório | Specs |
|---|---|
| `modules/auth`, `modules/users`, middleware e sessão Web | SPEC-01 |
| `modules/carriers` e página de transportadoras | SPEC-02, SPEC-07 |
| `modules/imports` e telas de importação/deliveries | SPEC-03, SPEC-04 |
| `modules/shipments`, páginas de envios e analytics | SPEC-04 a SPEC-07 |
| `modules/dashboard` e dashboard Web | SPEC-08 |
| `modules/alerts` e alertas Web | SPEC-09 |
| `modules/reports` e relatório diário Web | SPEC-10 |
| `modules/audit` e auditoria Web | SPEC-11 |
| Domínio futuro de pedidos/cotações | SPEC-12 |
