# SPEC-04 — Entregas Monitoradas e Dados Fiscais

**Estado:** Baseline Web estabilizado; API e dados parcialmente homologados; edge cases fiscais/financeiros cobertos em P1.1
**Rastreabilidade:** LOG-027, LOG-028, LOG-029, LOG-030, LOG-031, LOG-032, LOG-033

## Objetivo e contexto

Oferecer visão operacional pesquisável de cada entrega, com dados logísticos, fiscais, financeiros e SLA. Atores: logística, gestor, administrador e auditoria conforme permissão.

## Estado atual e evidências

Models, migrations, schemas, rotas, páginas e testes confirmam shipment, delivery, detalhe, filtros, promoção e campos fiscais/financeiros. A aderência integral de ordenação, busca global e filtros combinados do apêndice requer homologação.

Na execução P0 de 2026-07-02, a página Web e os filtros voltaram a compilar e a suíte Web ficou verde. LOG-027–033 permanecem abertos até reconciliação funcional e UAT.

Em P1.1 (2026-07-02), edge cases de precisão decimal, datas inválidas, exportação e compatibilidade via API foram cobertos com dataset de homologação sanitizado em `tests/fixtures/homologation_fiscal_financial.csv`.

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

Cenários adicionais P1.1:
- Decimal com precisão máxima (10,2): frete e NF com 99999.99
- Decimal com mais de 2 casas: arredondamento ou rejeição definida
- Percentual com NF muito pequena: frete 100.00 / NF 0.01 = 10000% (sem erro)
- Datas inválidas: 2026-02-30, 2026-13-01 (rejeição 400)
- Registro antigo via API: GET retorna null nos campos fiscais
- Exportação CSV/XLSX inclui colunas fiscais com valores ou vazio
- Renderização Web: null/zero mostram "Indisponível" ou "—", nunca NaN/Infinity

Cenários adicionais P1.2 (Confirmado):
- Busca multicampo (search) retorna resultados de NF, cliente, rastreio, UF e transportadora
- Combinação de 3+ filtros simultâneos (status + carrier + UF + mês) sem divergência de totais
- Ordenação por created_at, estimated_delivery, due_date, amount, criticality (asc/desc)
- Filtro inválido (month=13, page=0) retorna erro 422
- URL reflete filtros ativos (query params) e recarregar restaura estado
- Limpar filtros volta para estado inicial (URL sem params)
- Combinação de filtros fiscais e operacionais (freight_value_min + status + carrier)
- E2E: filtros combinados, persistência URL, ordenação, paginação, estado vazio

> **Evidência P1.2:** 19 testes API (`test_shipments_list.py`), 6 testes Web URL sync (`shipments-url-sync.test.tsx`), 7 testes E2E adicionais (`shipments-filters.spec.ts`). Validação month 1-12 no router. Build, lint e vitest green.

## Riscos, dependências e rastreabilidade

Origem autoritativa de NF/frete e semântica da data de coleta exigem homologação. Evidências: `modules/shipments`, `modules/imports`, migrations fiscais e páginas de shipments/deliveries.
