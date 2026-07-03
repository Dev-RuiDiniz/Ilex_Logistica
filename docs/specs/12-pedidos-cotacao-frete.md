# SPEC-12 — Pedidos ERP e Cotação de Frete

**Estado:** Especificado; implementação pendente
**Rastreabilidade:** LOG-036, LOG-037, LOG-038, LOG-039, LOG-040

## Objetivo e contexto

Comparar cotações de transportadoras antes da expedição e manter histórico auditável por pedido. Atores: logística opera; gestor compara; administrador configura transportadoras/regras; auditoria consulta.

## Estado atual e evidências

Não existem ainda models, migrations, endpoints ou telas. Os contratos abaixo foram aprovados para o MVP assistido; integrações automáticas continuam pós-MVP.

## Entradas, saídas e fluxo

1. Importar pedido ERP por CSV/XLSX com `source`, `external_number`, `order_date`, `customer_name`, `origin_zip`, `origin_uf`, `destination_zip`, `destination_uf`, `weight_kg`, `volume_count`, `goods_value` e `currency`.
2. Validar e persistir pedido idempotentemente.
3. Criar uma rodada de cotação com validade padrão de 24 horas para todas as transportadoras ativas.
4. Registrar por transportadora valor ou status `pendente`, `cotado`, `indisponivel`, `erro` ou `vencido`, com mensagem operacional sanitizada.
5. Selecionar e destacar melhor opção entre cotações válidas.
6. Preservar rodadas anteriores para auditoria.

Saída Web: tabela por pedido, cotações comparáveis, melhor opção, estados de falha e acesso ao histórico.

## Regras, dados e permissões

- Chave do pedido combina `source` e `external_number`; reimportação atualiza somente campos importáveis, sem duplicar ou apagar rodadas.
- CEP contém oito dígitos; UF é válida; peso, volumes e valor são positivos; moeda aceita no MVP é somente `BRL`.
- Cotações entram por Web ou CSV com `round_id`, `carrier_external_code`, `status`, `amount`, `transit_days` e `message`.
- `quoted` exige valor positivo; `unavailable` e `error` não aceitam valor; mensagens são sanitizadas e limitadas.
- Regra automática: menor valor válido; empate por menor prazo, maior eficiência confirmada e menor `carrier_id`.
- Override é permitido apenas para cotação válida, com justificativa e auditoria, preservando a recomendação automática.
- Cotação vencida não pode ser escolhida como atual.
- Falha de uma transportadora não invalida resultados válidos das demais.
- Somente perfis autorizados importam, executam ou selecionam; leitura gerencial/auditoria é separada.
- Integração automática exige contrato, autenticação segura, timeout, retry com backoff e idempotência.

## Contratos persistidos

- Pedido: campos do layout ERP, estado `active|cancelled`, histórico de importação, autoria e timestamps.
- Rodada: pedido, sequência, validade, estado `open|completed|no_valid_quotes|expired`, recomendação, seleção final, modo, justificativa e autoria.
- Cotação: rodada, transportadora, estado `pending|quoted|unavailable|error|expired`, valor/prazo opcionais, mensagem, origem `web|csv`, validade e autoria.
- Unicidade: `(source, external_number)`, `(order_id, sequence)` e `(round_id, carrier_id)`.

## Contratos HTTP

- `POST /orders/imports/preview`, `POST /orders/imports/confirm`, `GET /orders/imports/{id}`, `GET /orders`.
- `POST/GET /orders/{id}/quote-rounds`, `GET /quote-rounds/{id}`.
- `POST /quote-rounds/{id}/quotes`, preview/confirm CSV e seleção manual por `quote_id`.
- Rotas privadas usam `orders:read|write` e `quotes:read|write|override`, distinguindo `401` e `403`.

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

Depende das SPEC-01, SPEC-02, SPEC-03, SPEC-07 e SPEC-11. Retenção segue auditoria de cinco anos; arquivos de importação seguem política operacional. O MVP não automatiza ERP, transportadoras, portais ou captcha.
