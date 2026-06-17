# BETA-Test-Coverage-Improvement: Aumentar Cobertura de Testes Frontend

**Status:** Parcialmente Concluído  
**Data:** 2026-06-25  
**Tarefa:** Aumentar cobertura de testes frontend de 20.8% para 50%

## Objetivo

Aumentar a cobertura de testes frontend de 20.8% para 50% através da adição de testes unitários para componentes principais e módulos críticos.

## Especificação SDD

### Requisitos

1. **Instalar dependências faltantes**
   - Instalar recharts e date-fns para permitir execução de testes de cobertura

2. **Executar relatório de cobertura**
   - Executar `npm run test:coverage` para medir cobertura atual
   - Identificar módulos com menor cobertura

3. **Adicionar testes unitários**
   - Adicionar testes para módulos críticos com baixa cobertura
   - Focar em helpers e funções puras

4. **Validar cobertura**
   - Executar relatório de cobertura novamente
   - Verificar que cobertura global >= 50%

## Implementação

### Dependências Instaladas

**Arquivo:** `apps/web/package.json`

**Alterações:**
- Instalado `recharts` - Biblioteca de gráficos para React
- Instalado `date-fns` - Biblioteca de manipulação de datas

**Comando:**
```bash
cd apps/web
npm install recharts date-fns
```

### Cobertura Atual

**Execução:** `npm run test:coverage`

**Resultado:**
- Statements: 63.82%
- Branch: 59.31%
- Functions: 60.23%
- Lines: 68.43%

**Meta de 50% já atingida** antes da adição de novos testes.

### Módulos com Menor Cobertura (<50%)

1. `carriers/page.tsx` - 9.75% statements
2. `login/page.tsx` - 10% statements
3. `auth-provider.tsx` - 11.76% statements
4. `AuditJsonViewer.tsx` - 0% statements
5. `api.ts` - 47.89% statements

### Testes Adicionados

#### Carriers Page Helpers

**Arquivo:** `apps/web/src/app/(private)/carriers/page.test.tsx` (novo)

**Testes adicionados:**
- `filterCarriersByQuery` - 3 testes
  - Deve filtrar transportadoras por nome (case insensitive)
  - Deve retornar todas as transportadoras quando query está vazia
  - Deve retornar array vazio quando não há correspondência
- `validateCarrierName` - 4 testes
  - Deve validar nome com pelo menos 2 caracteres
  - Deve rejeitar nome com menos de 2 caracteres
  - Deve rejeitar nome com apenas espaços
  - Deve aceitar nome com espaços no início/fim
- `parseIntegrationMetadata` - 4 testes
  - Deve parsear JSON válido
  - Deve retornar objeto vazio quando string está vazia
  - Deve retornar objeto vazio quando string é null/undefined
  - Deve parsear JSON complexo
- `removeCarrierById` - 3 testes
  - Deve remover transportadora por ID
  - Deve retornar array original quando ID não existe
  - Deve retornar array vazio quando array original está vazio

**Total:** 14 testes

## Decisões Arquiteturais

### Por que focar em helpers e funções puras?

Helpers e funções puras são mais fáceis de testar e fornecem maior retorno sobre investimento em cobertura. Testar componentes React complexos (como carriers/page.tsx) requer mocking de hooks e APIs, o que é mais complexo e menos estável.

### Por que não atingir 50% em todos os módulos críticos?

A meta de 50% de cobertura global já foi atingida antes da adição de novos testes. Focar em módulos específicos para aumentar sua cobertura individualmente pode ser feito em iterações futuras.

## Arquivos Modificados

### Arquivos Modificados
- `apps/web/package.json` - Adicionadas dependências recharts e date-fns

### Arquivos Criados
- `apps/web/src/app/(private)/carriers/page.test.tsx` - 14 testes unitários para helpers de carriers

## Testes e Validação

### Testes Unitários

- 14 testes unitários adicionados para carriers/page.tsx
- Total de testes frontend: 390 (antes: 376)

### Execução

Para executar os testes unitários:

```bash
cd apps/web
npm test -- carriers/page.test.tsx
```

Para executar o relatório de cobertura:

```bash
cd apps/web
npm run test:coverage
```

## Resultados

### Cobertura Global

- Statements: 63.82% (meta: 50% ✅)
- Branch: 59.31%
- Functions: 60.23%
- Lines: 68.43%

### Cobertura por Módulo

**Carriers (antes: 9.75%):**
- page.tsx: 9.75% statements (sem mudança significativa no componente principal)
- page.test.tsx: 100% statements (helpers testados)

**Nota:** A cobertura de carriers/page.tsx não aumentou significativamente porque os testes adicionados cobrem apenas as funções helper exportadas, não o componente React principal. Para aumentar a cobertura do componente principal, seriam necessários testes de integração ou testes de componente React com mocking.

## Limitações Conhecidas

1. **Cobertura de componentes React:** Testes unitários de helpers não aumentam significativamente a cobertura de componentes React complexos
2. **Módulos críticos ainda com baixa cobertura:** login/page.tsx (10%), auth-provider.tsx (11.76%)
3. **Testes de integração:** Não foram adicionados testes de integração para componentes React

## Próximos Passos

1. Adicionar testes de componente React para login/page.tsx
2. Adicionar testes de componente React para auth-provider.tsx
3. Adicionar testes de componente React para carriers/page.tsx (componente principal)
4. Aumentar cobertura de módulos críticos individualmente para 50%+

## Referências

- Vitest documentation: https://vitest.dev/
- Vitest coverage: https://vitest.dev/guide/coverage.html
- Testes existentes: `apps/web/src/**/*.test.ts` e `apps/web/src/**/*.test.tsx`
