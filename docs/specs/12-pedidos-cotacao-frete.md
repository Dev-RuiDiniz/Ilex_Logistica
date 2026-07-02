# SPEC-12 — Pedidos ERP e Cotação de Frete

**Estado:** Planejado
**Rastreabilidade:** LOG-036, LOG-037, LOG-038, LOG-039, LOG-040

## Objetivo e contexto

Comparar cotações de transportadoras antes da expedição e manter histórico auditável por pedido. Atores: logística opera; gestor compara; administrador configura transportadoras/regras; auditoria consulta.

## Estado atual e evidências

Não foram identificados models, migrations, endpoints ou telas de pedidos/cotações. Esta spec define comportamento-alvo; nomes físicos e URLs só serão fixados na especificação técnica da implementação.

## Entradas, saídas e fluxo

1. Importar pedido ERP por CSV/XLSX no MVP, com número externo, data, cliente, UF de destino, valor e demais campos mínimos homologados.
2. Validar e persistir pedido idempotentemente.
3. Criar uma rodada de cotação para transportadoras ativas/habilitadas.
4. Registrar por transportadora valor ou status `pendente`, `cotado`, `indisponivel`, `erro` ou `vencido`, com mensagem operacional sanitizada.
5. Selecionar e destacar melhor opção entre cotações válidas.
6. Preservar rodadas anteriores para auditoria.

Saída Web: tabela por pedido, cotações comparáveis, melhor opção, estados de falha e acesso ao histórico.

## Regras, dados e permissões

- Chave do pedido combina origem ERP e número externo; reimportação atualiza conforme política idempotente sem duplicar.
- Valores monetários usam decimal e mesma moeda; moeda múltipla está fora do MVP.
- Regra inicial: menor valor válido. Empate: menor prazo quando disponível, depois melhor eficiência confirmada, depois identificador estável.
- Cotação vencida não pode ser escolhida como atual.
- Falha de uma transportadora não invalida resultados válidos das demais.
- Somente perfis autorizados importam, executam ou selecionam; leitura gerencial/auditoria é separada.
- Integração automática exige contrato, autenticação segura, timeout, retry com backoff e idempotência.

## Contrato mínimo planejado

Pedido: identificador interno, origem, número externo, data, cliente, UF, valor, status e timestamps. Cotação: pedido, transportadora, rodada, valor opcional, prazo opcional, status, mensagem sanitizada, validade, origem e timestamps. Campos adicionais dependem do ERP/transportadora e ficam A CONFIRMAR.

## Falhas esperadas

Arquivo inválido, pedido duplicado, transportadora sem cotação, timeout, resposta inválida, nenhuma opção válida e concorrência de rodadas devem gerar estado auditável, sem inventar preço ou apagar histórico.

## Critérios de aceite

- LOG-036: subaba lista pedidos e comparação por transportadora.
- LOG-037: arquivo homologado importa pedidos com erros por linha/idempotência.
- LOG-038: contrato mínimo, autenticação e formato do ERP estão documentados antes de API automática.
- LOG-039: motor compara resultados válidos e preserva falhas individualmente.
- LOG-040: melhor opção segue regra determinística e explicável.
- Histórico permite reconstruir quando e por que uma opção foi destacada.

## Cenários TDD

Importação válida/inválida/duplicada; rodada com todas, algumas ou nenhuma cotação válida; empate; vencimento; timeout/retry; RBAC; auditoria; API e Web; migration upgrade/downgrade.

## Riscos, dependências e rastreabilidade

Contrato ERP, APIs, prazo cotado, validade, seleção manual e política de retenção estão A CONFIRMAR. Depende das SPEC-01, SPEC-02, SPEC-03, SPEC-07 e SPEC-11. O MVP não automatiza portal/captcha.
