# SPEC-06 — Tratativas e Painel de Exceções

**Estado:** Confirmado

## Objetivo e contexto

Priorizar entregas problemáticas e registrar ações humanas sem perder histórico. Atores: logística trata; gestão acompanha; auditoria consulta.

## Estado atual e evidências

Shipments possuem tratativas e rotas associadas; analytics fornece painel de exceções; o Web possui páginas e testes de exceções e detalhe.

## Entradas, saídas e fluxo

O painel recebe filtros e retorna resumo/lista priorizada. No detalhe, usuário autorizado registra uma tratativa com conteúdo validado; a API persiste autoria e data e devolve o histórico ordenado.

## Regras, dados e permissões

- Exceções derivam de status/SLA reais, não de estado local do Web.
- Tratativas são acrescentadas ao histórico; edição/exclusão não é presumida.
- Autoria deve vir da sessão, não de campo confiado ao cliente.
- Consulta e escrita obedecem permissões distintas quando definidas.
- Dados sensíveis não devem ser incluídos em texto livre.

## Falhas esperadas

Shipment inexistente, texto inválido, concorrência e falta de permissão não criam registro parcial. Painel sem resultados mostra zero/vazio coerente.

## Critérios de aceite

- Totais do painel conferem com a lista filtrada.
- Tratativa válida aparece no histórico com autor e timestamp.
- Usuário somente leitura não cria tratativa.
- Alteração de SLA/status reflete na próxima consulta do painel.

## Cenários TDD

Exceções por atraso/criticidade/status, filtros combinados, criação e ordenação de tratativas, `404`, `401` e `403`; teste Web do fluxo painel → detalhe → tratativa.

## Riscos, dependências e rastreabilidade

Taxonomia formal de motivo/resultado e SLA de atendimento estão A CONFIRMAR. Evidências: `shipments/exceptions_service.py`, analytics, rotas de treatments e páginas de exceções.
