# SPEC-10 — Relatórios Diários e Exportações

**Estado:** Confirmado

## Objetivo e contexto

Gerar um snapshot diário auditável com KPIs, exceções, alertas, eficiência e falhas de importação, além de disponibilizar consulta e exportação. Atores: logística, gestão e auditoria autorizada.

## Estado atual e evidências

API possui model, geração, listagem, consulta por id/data e exportação; Web possui página de relatório diário e testes.

## Entradas, saídas e fluxo

Solicitação informa data/filtros suportados. Serviço agrega fontes, persiste estado/resultado e retorna relatório estruturado. Consulta não recalcula silenciosamente um snapshot. Exportação recebe referência/filtros definidos pelo schema e retorna artefato ou representação suportada.

## Regras, dados e permissões

- Relatório identifica data, período, status de geração e filtros.
- Totais reconciliam com fontes no momento do snapshot.
- Geração repetida para a mesma chave segue a idempotência definida pelo model/serviço.
- Falha fica registrada sem apresentar relatório incompleto como concluído.
- Exportação não inclui secrets nem campos fora da permissão.

## Falhas esperadas

Data inválida, relatório inexistente, geração concorrente e falha de agregação/exportação retornam erro operacional e estado consistente.

## Critérios de aceite

- Gerar, listar, consultar e exportar funcionam para usuário autorizado.
- Snapshot contém resumo, KPIs, exceções, alertas, eficiência e falhas disponíveis.
- Estado vazio/falha é distinguível de relatório gerado.
- Dados fiscais previstos na SPEC-04 entram em exportações aplicáveis após homologação.

## Cenários TDD

Geração com/sem dados, idempotência, falha intermediária, consulta por data/id, exportação e RBAC; teste Web de gerar e consultar.

## Riscos, dependências e rastreabilidade

Política inicial: geração diária às 06:00 em `America/Sao_Paulo` e retenção de 365 dias. Envio externo permanece desabilitado sem destinatários configurados. Evidência: configuração, `modules/reports`, migration e página daily report.
