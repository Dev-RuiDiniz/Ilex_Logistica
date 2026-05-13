# Fluxo Web e Permissões - Sprint B (B-09)

## Fluxo de navegação

1. Usuário acessa `/login`.
2. Login válido consome `POST /api/v1/auth/login`.
3. Sessão é armazenada localmente e o usuário é redirecionado para `/`.
4. Rotas privadas (`/` e `/carriers`) exigem sessão autenticada.
5. Usuário sem sessão é redirecionado para `/login`.

## Perfis e permissões

| Perfil | Visualizar transportadoras | Criar/Editar/Inativar |
|---|---|---|
| admin | Sim | Sim |
| logistica | Sim | Sim |
| gestor | Sim | Sim |
| auditoria | Sim | Não |

## Regras aplicadas na interface

- O menu exibe o módulo de transportadoras para perfis com leitura.
- Botões de edição e inativação ficam ocultos para `auditoria`.
- Formulário de create/update só aparece para perfis com edição.
- Mensagens de erro mantêm feedback claro sem quebrar fluxo da página.
