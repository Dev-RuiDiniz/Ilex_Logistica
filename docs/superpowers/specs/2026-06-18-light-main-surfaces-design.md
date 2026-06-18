# Ajuste Visual Claro das Superfícies Principais

## Objetivo

Reduzir a sensação escura do frontend sem alterar a identidade do produto no `header` e na `sidebar`.

## Escopo

- Clarear as superfícies compartilhadas principais:
  - `surface-panel`
  - `surface-panel-strong`
  - `surface-muted`
  - `metric-card`
  - `table-shell`
  - `empty-state`
  - `loading-state`
  - `error-state`
  - `page-hero`
- Clarear o bloco principal da tela de login, preservando o layout e o fluxo.

## Fora de Escopo

- Não alterar rotas, contratos de API ou comportamento do produto.
- Não trocar a identidade escura do `AppShell` no `header` e na `sidebar`.
- Não redesenhar fluxos.

## Resultado Esperado

- Conteúdo principal mais leve e luminoso.
- Melhor leitura de formulários, cards, tabelas e painéis.
- Shell continua com a assinatura premium atual, mas o centro do produto deixa de parecer pesado.

## Validação

- `cd apps/web && npm test`
- `cd apps/web && npm run build`
