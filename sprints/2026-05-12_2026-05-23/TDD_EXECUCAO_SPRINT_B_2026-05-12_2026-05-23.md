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

### B-05
- RED:
  - Comando: `npm run test -- src/lib/permissions.test.ts`
  - Falha observada: `getCarriersAccessMode is not a function`.
- GREEN:
  - Implementado modo de acesso textual (`edit`/`read`) para RBAC de UI.
  - Comando: `npm run test -- src/lib/permissions.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `test(web): B-05 valida modo de acesso por perfil`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/30
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/12

### B-06
- RED:
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Falha observada: `filterCarriersByQuery is not a function`.
- GREEN:
  - Extraido helper de filtro por nome em `carriers/page.tsx`.
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `feat(web): B-06 B-07 B-08 extrai helpers e valida fluxo de carriers`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/31
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/13

### B-07
- RED:
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Falha observada: `validateCarrierName/parseIntegrationMetadata is not a function`.
- GREEN:
  - Implementadas validacoes minimas de nome e parse de metadata JSON.
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `feat(web): B-06 B-07 B-08 extrai helpers e valida fluxo de carriers`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/32
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/14

### B-08
- RED:
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Falha observada: `removeCarrierById is not a function`.
- GREEN:
  - Implementado helper para remover item inativado da lista em memoria.
  - Comando: `npm run test -- src/app/(private)/carriers/page.helpers.test.ts`
  - Resultado GREEN: passando.
- Commit Web: `feat(web): B-06 B-07 B-08 extrai helpers e valida fluxo de carriers`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/33
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/15

### B-09
- TDD documental:
  - Primeiro: checklist de criterios verificaveis de fluxo/permissoes.
  - Depois: consolidacao de evidencias reais de testes executados.
- Artefato oficial:
  - `sprints/2026-05-12_2026-05-23/FLUXO_WEB_PERMISSOES_B09_2026-05-12_2026-05-23.md`
- Commit Docs: `docs(docs): B-09 publica fluxo oficial de navegacao e permissoes`.
- Issue Docs: https://github.com/ilex-logistica/Docs/issues/34
- Issue Execucao Web: https://github.com/ilex-logistica/Web/issues/16
