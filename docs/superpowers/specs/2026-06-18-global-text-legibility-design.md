# Normalização Global de Legibilidade de Texto

## Objetivo

Melhorar a legibilidade de texto em todo o frontend do Ilex Logistica, reforçando contraste e hierarquia sem reescurecer as superfícies principais.

## Escopo

- Ajustar a escala textual do design system em `globals.css`
- Reforçar subtítulos, labels, notas e estados auxiliares
- Normalizar páginas e componentes legados que ainda usam `gray/slate` suaves demais
- Preservar cores semânticas de alerta, erro, sucesso e status

## Fora de Escopo

- Não alterar fluxos, contratos de API ou comportamento de negócio
- Não redesenhar o shell do produto
- Não reverter a base clara das superfícies principais

## Resultado Esperado

- Texto secundário mais nítido
- Títulos, labels e conteúdo tabular mais fáceis de escanear
- Menor variação arbitrária entre telas novas e antigas

## Validação

- `cd apps/web && npm test`
- `cd apps/web && npm run build`
