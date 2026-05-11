# Integrations

Camada de integrações externas do Ilex Logística para coleta de status de entrega por API, importação e bots controlados.

## Objetivo no MVP

Criar base segura e extensível para conectar transportadoras sem acoplar o core a uma única fonte de dados.

## Responsabilidades do repositório

- Clientes de API por transportadora
- Adaptadores e mapeadores de payload
- Fluxos de coleta controlada por bots/scraping
- Normalização de dados para consumo da API central
- Testes de contratos e conectores

## Stack prevista

- Python workers
- Clients HTTP de APIs
- Playwright (quando necessário para portais)
- Suporte a filas/jobs para execução agendada

## Estrutura sugerida

```text
connectors/
  api_clients/
  bots/
parsers/
mappers/
tests/
docs/
examples/
```

## Backlog prioritário (LOG-*)

- LOG-020: Criar logs de coleta
- LOG-021: Preparar conectores de API
- LOG-022: Preparar bots/scraping controlado
- LOG-025: Testes integrados e QA

## Critérios de aceite iniciais

- Interface base de conector padronizada
- Conector de exemplo testável em ambiente controlado
- Logs de sucesso/falha por fonte de dados

## Convenção de commits

`<tipo>(integrations): <ID> <resumo em pt-BR>`

Exemplo: `docs(integrations): LOG-021 documenta interface base de conectores`
