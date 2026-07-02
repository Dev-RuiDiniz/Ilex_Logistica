# SPEC-08 — Dashboard e Indicadores

**Estado:** Implementado; bloqueado por testes Web e homologação de LOG-035
**Rastreabilidade:** LOG-035

## Objetivo e contexto

Fornecer panorama executivo e operacional com KPIs, tendência, eficiência e exceções. Atores: gestão e perfis autorizados.

## Estado atual e evidências

API oferece summary e trend com schemas/filtros; Web possui dashboard e testes, integrado a alertas e eficiência.

Na auditoria de 2026-07-02, testes do dashboard falharam; nenhum indicador deve ser considerado homologado até reconciliação com a mesma janela de filtros das entregas.

## Entradas, saídas e fluxo

Filtros delimitam período e dimensões suportadas. A API calcula resumo e tendência server-side; o Web apresenta cartões, gráficos, eficiência e exceções sem recomputar regras de domínio.

## Regras, dados e permissões

- Todos os componentes usam a mesma definição de período e filtros aplicados.
- Totais devem reconciliar com listagens equivalentes.
- Ausência de dados gera zero/vazio identificado, não dados demonstrativos.
- Tendência ordena períodos cronologicamente e explicita granularidade.
- Dados são somente leitura e exigem permissão de dashboard.

## Falhas esperadas

Filtros inválidos retornam validação; falha parcial não deve exibir números antigos como atuais; UI oferece erro e nova tentativa.

## Critérios de aceite

- Alterar período recalcula KPIs, tendência, eficiência e exceções aplicáveis.
- Filtro aplicado é visível e reproduzível.
- Loading, vazio, erro, `401` e `403` são tratados.
- Valores do dashboard conferem com endpoints/fontes do mesmo período.

## Cenários TDD

Datas limite, período vazio, múltiplas transportadoras, tendência ordenada, erro da API e permissões; teste de integração com filtros e navegação para detalhe.

## Riscos, dependências e rastreabilidade

Metas e frequência de atualização estão A CONFIRMAR. Depende das SPEC-04, SPEC-05, SPEC-07 e SPEC-09. Evidência: `modules/dashboard`, `dashboard-api.ts` e página/testes.
