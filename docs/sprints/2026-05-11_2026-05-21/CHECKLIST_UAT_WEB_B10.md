# Checklist UAT Web - Sprint B (B-10)

## Cenários de autenticação

| Caso | Pré-condição | Passos | Resultado esperado |
|---|---|---|---|
| Login válido | Usuário ativo na API | Informar credenciais válidas e enviar | Redireciona para `/` e mantém sessão |
| Login inválido | Usuário inexistente ou senha incorreta | Informar credenciais inválidas | Exibe mensagem de erro sem quebrar UI |
| Rota privada sem sessão | Navegador sem cookie/sessão | Acessar `/` ou `/carriers` | Redireciona para `/login` |

## Cenários de transportadoras

| Caso | Pré-condição | Passos | Resultado esperado |
|---|---|---|---|
| Listagem inicial | Sessão autenticada | Abrir `/carriers` | Carrega dados com feedback de loading |
| Filtro por nome | Lista com mais de um item | Buscar por parte do nome | Tabela aplica filtro corretamente |
| Cadastro válido | Perfil com edição | Preencher formulário e salvar | Item aparece na tabela |
| Edição válida | Item existente | Editar campos e salvar | Alteração refletida na lista |
| Inativação confirmada | Item ativo e perfil com edição | Confirmar inativação | Item sai da listagem padrão sem reload |
| Perfil auditoria | Sessão com papel auditoria | Abrir `/carriers` | Visualiza lista sem botões de edição |

## Evidências esperadas

- Captura de tela do login com sucesso.
- Captura de tela de erro de login inválido.
- Captura de tela da listagem com filtro aplicado.
- Captura de tela do fluxo de create/update.
- Captura de tela da confirmação de inativação.
- Captura de tela da visão de auditoria sem ações de edição.
