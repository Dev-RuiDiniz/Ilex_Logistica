# SPEC-07 — Eficiência por Transportadora

**Estado:** Parcialmente homologado
**Rastreabilidade:** LOG-034, LOG-035

## Objetivo e contexto

Comparar volume, cumprimento de prazo, exceções e custo entre transportadoras usando o mesmo universo filtrado das entregas. Atores: gestor, logística, administrador e auditoria autorizada.

## Estado atual e evidências

API possui endpoint/serviço/schemas de carrier efficiency; Web possui página, filtros, gráficos e testes. Métricas financeiras completas do apêndice ainda requerem validação.

## Entradas, saídas e fluxo

Filtros de período, transportadora, cliente e UF delimitam o conjunto. O serviço agrupa por transportadora e retorna total, no prazo, atrasadas, extraviadas, percentuais e métricas disponíveis de frete.

## Regras, dados e permissões

- Percentuais usam o total válido da própria transportadora; total zero resulta em zero/indisponível conforme contrato, nunca divisão por zero.
- Frete total soma valores disponíveis; percentual médio considera apenas linhas com base calculável e informa a população válida.
- LOG-035 exige que mês, ano e todo período afetem quadro e KPIs igualmente.
- Ranking padrão: maior percentual no prazo; desempate por menor percentual de extravio, menor custo médio e nome estável. Alteração futura deve ser configurável e documentada.

## Falhas esperadas

Intervalo inválido, datas invertidas ou filtro desconhecido retornam validação. Dados incompletos não são convertidos em zero financeiro.

## Critérios de aceite

- Uma linha por transportadora no conjunto filtrado.
- Contagens e percentuais reconciliam com shipments.
- Filtros recalculam todos os indicadores.
- Ranking é determinístico e explica dados indisponíveis.

## Cenários TDD

Transportadoras com volumes distintos, total zero, frete ausente, NF zero, atrasos/extravios e empate; testes API, helpers/gráficos e filtro Web.

## Riscos, dependências e rastreabilidade

Resultado depende da SPEC-04 e SPEC-05. Fórmula final de eficiência e metas contratuais precisam de homologação. Evidência: analytics de shipments e página carrier-efficiency.
