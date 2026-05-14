# TDD Execucao Sprint B (2026-05-12 a 2026-05-23)

## Calendario oficial
- Sprint 1 oficial: 12/05/2026 a 23/05/2026.
- Nota de reconciliacao: artefatos legados em 2026-05-11_2026-05-21 sao mantidos para historico.

## Evidencias por tarefa

### B-01
- RED:
  - Testes adicionados para sessao e base de API.
  - Comando: `npm run test -- src/lib/session.test.ts src/lib/api.test.ts`
  - Resultado RED inicial: cobertura inexistente para os novos cenarios antes da implementacao.
- GREEN:
  - Implementado `getApiBaseUrl`/`buildApiUrl` em `src/lib/api.ts`.
  - Validado ciclo de `save/get/clear` em sessao.
  - Comando: `npm run test -- src/lib/session.test.ts src/lib/api.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `test(web): B-01 valida sessao e configuracao base da API`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/26
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/8

### B-02
- RED:
  - Comando: `npm run test -- src/components/app-shell.test.tsx`
  - Falha observada: `getRoleUiLabel is not a function`.
- GREEN:
  - Implementado helper de rotulo de perfil no shell autenticado.
  - Comando: `npm run test -- src/components/app-shell.test.tsx`
  - Resultado GREEN: passando.
- Commit Web: `test(web): B-02 valida shell autenticado e estado por perfil`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/27
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/9

### B-03
- RED:
  - Comando: `npm run test -- src/app/login/page.test.tsx`
  - Falha observada: `getLoginErrorMessage is not a function`.
- GREEN:
  - Implementado helper de mensagem de erro de login e uso no handler.
  - Comando: `npm run test -- src/app/login/page.test.tsx`
  - Resultado GREEN: passando.
- Commit Web: `test(web): B-03 valida mensagem de erro de autenticacao`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/28
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/10

### B-04
- RED:
  - Comando: `npm run test -- middleware.test.ts`
  - Falha observada: `isPrivatePath/shouldRedirect... is not a function`.
- GREEN:
  - Implementados helpers puros de guarda no `middleware.ts`.
  - Comando: `npm run test -- middleware.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `test(web): B-04 valida regras de guardas de rota`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/29
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/11
