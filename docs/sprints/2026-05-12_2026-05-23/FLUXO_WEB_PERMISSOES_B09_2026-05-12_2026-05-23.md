# Fluxo Web e Permissoes - Sprint B (B-09)

## Janela oficial
- Sprint 1 oficial: 12/05/2026 a 23/05/2026.
- Reconciliação historica: documento derivado do artefato legado `2026-05-11_2026-05-21`.

## Fluxo de navegacao
1. Usuario acessa `/login`.
2. Login valido consome `POST /api/v1/auth/login`.
3. Sessao e salva localmente e o usuario e redirecionado para `/`.
4. Rotas privadas (`/` e `/carriers`) exigem sessao autenticada.
5. Usuario sem sessao e redirecionado para `/login`.
6. Usuario autenticado em `/login` e redirecionado para `/`.

## Perfis e permissoes
| Perfil | Visualizar transportadoras | Criar/Editar/Inativar |
|---|---|---|
| admin | Sim | Sim |
| logistica | Sim | Sim |
| gestor | Sim | Sim |
| auditoria | Sim | Nao |

## Regras aplicadas na interface
- Menu exibe modulos privados para usuario autenticado.
- Label de perfil indica `edicao` para admin/logistica/gestor e `somente leitura` para auditoria.
- Botoes de editar/inativar ficam indisponiveis para auditoria.
- Formulario de create/update aparece apenas para perfil com edicao.
- Mensagens de erro mantem feedback claro sem quebrar o fluxo da pagina.

## Evidencias
- Teste RED/GREEN de helper de RBAC UI: `src/lib/permissions.test.ts`.
- Teste RED/GREEN de shell autenticado: `src/components/app-shell.test.tsx`.
- Teste RED/GREEN de guardas: `middleware.test.ts`.
