# SPEC-05 — SLA, Atrasos e Criticidade

**Estado:** Implementação confirmada; regra operacional final A CONFIRMAR

## Objetivo e contexto

Calcular prazo, atraso e criticidade de forma determinística para priorizar entregas. Atores: administrador configura; logística e gestão consomem resultados.

## Estado atual e evidências

Há model e rotas de regras SLA, recálculo global/individual, serviços, filtros, badges e testes backend/frontend.

## Entradas, saídas e fluxo

Regras recebem parâmetros suportados pelo schema. O recálculo usa dados da entrega e regra aplicável, atualiza indicadores derivados e os expõe em listagens, detalhe, exceções, dashboard e relatórios.

## Regras, dados e permissões

- Seleção de regra deve ser determinística e auditável.
- Entrega sem dados suficientes fica sem cálculo ou com estado explícito, nunca recebe atraso inventado.
- Datas realizadas prevalecem para encerrar a avaliação quando aplicável.
- Alterar regra e recalcular exige permissão administrativa.
- Definições exatas de no prazo, atraso, extravio e faixas de criticidade precisam de homologação do cliente.

## Falhas esperadas

Regra conflitante/inválida, data inconsistente ou shipment inexistente produz erro explícito sem corromper cálculos anteriores.

## Critérios de aceite

- Mesmo conjunto de entradas gera o mesmo resultado.
- Casos antes, no limite e após o prazo são cobertos.
- Recálculo individual e em lote são consistentes.
- UI apresenta estado e criticidade sem recalcular regra divergente no cliente.

## Cenários TDD

Tabela de casos de fronteira temporal, ausência de datas, entrega concluída, regra inexistente e permissões. Testes de integração verificam reflexo em filtros/dashboard.

## Riscos, dependências e rastreabilidade

Timezone, calendário útil/feriados e precedência entre regras estão A CONFIRMAR. Evidências: `modules/sla`, helpers/badges/filtros SLA e testes relacionados.
