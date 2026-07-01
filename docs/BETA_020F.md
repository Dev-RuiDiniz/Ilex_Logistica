# BETA-020F: Remover Error-Handler Legacy

**Status:** Concluído  
**Data:** 2026-06-25  
**Tarefa:** Remover arquivos legacy de error-handler após completa migração para useApiErrorHandler

## Objetivo

Remover arquivos legacy de tratamento de erros que foram substituídos pelo hook `useApiErrorHandler` no BETA-020D.

## Especificação SDD

### Requisitos

1. **Remover arquivos legacy** - `error-handler.ts` e `error-handler.test.ts`
2. **Verificar dependências** - Confirmar que não há imports de error-handler no código
3. **Validar testes** - Confirmar que testes frontend ainda passam após remoção

### Justificativa

- `error-handler.ts` foi substituído por `useApiErrorHandler` hook no BETA-020D
- Todas as 18 páginas foram migradas para o novo hook
- O arquivo legacy só era usado pelo seu próprio teste
- Manter arquivos legacy gera confusão e aumenta manutenção

## Implementação

### Verificação de Dependências

Antes da remoção, foi verificado que não há imports de `error-handler` no código:

```bash
grep -r "from.*error-handler" apps/web/src
```

Resultado: Apenas `error-handler.test.ts` importava de `error-handler.ts`

### Arquivos Removidos

1. `apps/web/src/lib/error-handler.ts` - Função legacy de tratamento de erros
2. `apps/web/src/lib/error-handler.test.ts` - Testes do error-handler legacy

### Validação

Após remoção, os testes frontend continuam passando (320 testes).

## Decisões Arquiteturais

### Por que remover em vez de manter?

- Reduz confusão sobre qual error-handler usar
- Evita uso acidental de código legacy
- Simplifica manutenção do código
- Segue princípio de YAGNI (You Aren't Gonna Need It)

### Por que não fazer backup?

- Código está no git (histórico preservado)
- Se necessário, pode ser restaurado do git
- Não há necessidade de backup adicional

## Arquivos Modificados

### Arquivos Removidos
- `apps/web/src/lib/error-handler.ts`
- `apps/web/src/lib/error-handler.test.ts`

## Limitações Conhecidas

Nenhuma limitação conhecida.

## Próximos Passos

Nenhum próximo passo específico para esta tarefa. Continuação com BETA-029.

## Referências

- BETA-020D: Integração de Tratamento de Erros RBAC no Frontend
- Hook `useApiErrorHandler`: `apps/web/src/lib/useApiErrorHandler.ts`
