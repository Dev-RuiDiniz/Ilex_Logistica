# SPEC-04 — Entregas Monitoradas e Dados Fiscais

**Estado:** Parcialmente homologado
**Rastreabilidade:** LOG-027, LOG-028, LOG-029, LOG-030, LOG-031, LOG-032, LOG-033

## Objetivo e contexto

Oferecer visão operacional pesquisável de cada entrega, com dados logísticos, fiscais, financeiros e SLA. Atores: logística, gestor, administrador e auditoria conforme permissão.

## Estado atual e evidências

Models, migrations, schemas, rotas, páginas e testes confirmam shipment, delivery, detalhe, filtros, promoção e campos fiscais/financeiros. A aderência integral de ordenação, busca global e filtros combinados do apêndice requer homologação.

## Entradas, saídas e fluxo

Entrada por importação ou promoção de delivery. Listagem paginada aceita busca/filtros; detalhe retorna dados e tratativas autorizadas. Saída apresenta rastreio, cliente, UF, transportadora, status, datas, NF, valor da NF, coleta, frete e percentual.

## Regras, dados e permissões

- `percentual_frete = frete / valor_nf * 100` somente quando ambos existem e `valor_nf > 0`.
- Ausência/zero exibe indisponível; nunca `Infinity`, `NaN` ou erro 500.
- Busca cobre NF, cliente, rastreio, UF e transportadora.
- Filtros por status, transportadora, cliente, UF, mês, ano e todo período são combináveis.
- A mesma janela filtrada alimenta listagem, KPIs e eficiência.
- Valores monetários usam precisão decimal; datas respeitam o contrato da API.

## Falhas esperadas

Filtro inválido retorna erro de validação; registro inexistente retorna `404`; ausência de dados mostra estado vazio; falta de autorização segue `401/403`.

## Critérios de aceite

- LOG-027–030 aparecem na API, listagem, detalhe e exportação aplicável.
- LOG-028 permite busca e ordenação de NF.
- LOG-031 cobre nulos e zero.
- LOG-032/033 funcionam isolados e combinados sem divergência de totais.
- Paginação e ordenação permanecem estáveis.

## Cenários TDD

Testes API para cada filtro e combinação relevante; cálculo com valores válidos/nulos/zero; busca multicampo; paginação. Vitest valida renderização e interação; Playwright cobre importação até consulta filtrada.

## Riscos, dependências e rastreabilidade

Origem autoritativa de NF/frete e semântica da data de coleta exigem homologação. Evidências: `modules/shipments`, `modules/imports`, migrations fiscais e páginas de shipments/deliveries.
