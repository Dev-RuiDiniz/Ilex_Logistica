# Gate de desempenho

Metas aprovadas: p95 geral até 500 ms, listagens filtradas até 1 s, importação de 10 mil linhas até 60 s, 50 usuários concorrentes e zero erro inesperado.

## Execução HTTP

Em homologação, obtenha um token descartável de teste sem registrá-lo em shell history/artefatos e execute:

```sh
python scripts/performance_gate.py \
  --base-url https://app.exemplo.com.br/api/v1 \
  --token "$ILEX_PERF_TOKEN" \
  --concurrency 50 \
  --requests 500 \
  --output /tmp/ilex-performance.json
```

O comando mede listagem de pedidos, dashboard e listagem de envios, reportando p50/p95/p99, throughput e erros. O JSON pode ser anexado à evidência de homologação após sanitização; nunca versionar token.

## Importação

O teste `apps/api/tests/test_orders_performance.py` usa a fixture sanitizada de 10 mil pedidos e bloqueia duração acima de 60 segundos. A medição de referência local deve informar sistema operacional, CPU, memória, banco e duração; ela não substitui PostgreSQL/VPS.

## Registro obrigatório

| Campo | Valor |
|---|---|
| Tag/build | preencher na execução |
| Hardware/VPS | preencher na execução |
| PostgreSQL/dataset | preencher na execução |
| p50/p95/p99 | preencher na execução |
| Throughput/erros | preencher na execução |
| Import 10 mil | preencher na execução |
| Responsável/data | preencher na execução |

Resultados só aprovam P4 quando coletados no ambiente semelhante à produção. Índices novos exigem `EXPLAIN (ANALYZE, BUFFERS)` anexado à evidência.

## Referência local de 2026-07-03

O preview + confirmação de 10 mil pedidos levou 5,07 s em Windows/Python 3.12 com SQLite em memória e fixture sanitizada. Esse resultado confirma o gate funcional local de 60 s, mas não comprova latência concorrente nem desempenho do PostgreSQL/VPS.
