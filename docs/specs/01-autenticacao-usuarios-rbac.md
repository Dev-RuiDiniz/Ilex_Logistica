# SPEC-01 — Autenticação, Usuários e RBAC

**Estado:** Confirmado

## Objetivo e contexto

Autenticar pessoas, renovar sessões e restringir operações por papéis e permissões. Atores: administrador, logística/operador, gestor e auditoria/viewer.

## Estado atual e evidências

FastAPI possui login/refresh, dependências de autenticação e CRUD/inativação de usuários. Models representam usuário, papel, permissão e associação. O Web possui sessão, middleware, helpers de permissão, `AccessDenied` e testes de navegação/RBAC.

## Entradas, saídas e fluxo

- Login recebe credenciais e retorna access/refresh token sem expor hash ou segredo.
- Refresh recebe token válido e retorna sessão renovada.
- Operações de usuário recebem dados validados e retornam representação sem credenciais.
- Web sem sessão segue para login; API sem autenticação responde `401`; usuário autenticado sem permissão recebe `403`.

## Regras, dados e permissões

- Senhas são armazenadas somente como hash seguro.
- Access tokens expiram em 15 minutos e refresh tokens em 7 dias, com valores configuráveis por ambiente.
- Cada refresh rotaciona o par de tokens por `token_version`; tokens anteriores e sessões de usuários inativos são rejeitados.
- Novas senhas têm no mínimo 12 caracteres e incluem maiúscula, minúscula, número e símbolo; hashes legados continuam válidos para login até troca controlada.
- Administrador gerencia usuários; demais acessos dependem da permissão real do endpoint.
- Inativação impede novo acesso sem apagar histórico.
- Secrets e tokens não entram em logs, respostas de erro ou documentação.

## Falhas esperadas

Credencial inválida, token ausente/malformado/expirado, usuário inativo, conflito de identificação e permissão insuficiente devem produzir erro explícito e não alterar estado.

## Critérios de aceite

- Login e refresh válidos funcionam; credenciais inválidas não revelam qual campo falhou.
- Cada rota privada diferencia `401` e `403`.
- Navegação oculta ações não autorizadas sem substituir a proteção da API.
- Criação, edição e inativação deixam o estado consistente.

## Cenários TDD

1. RED: login inválido e token expirado são rejeitados; GREEN: validação mínima; REFACTOR: centralizar erros.
2. RED: matriz de papéis testa permitido/proibido por rota; GREEN: dependência de permissão; REFACTOR: helpers compartilhados.
3. RED: Web redireciona `401` e renderiza acesso negado em `403`.

## Riscos, dependências e rastreabilidade

Rotação/revogação por versão e política de senha estão confirmadas por migration e testes. Revogação administrativa dedicada pode incrementar a versão em evolução futura. Evidências: `modules/auth`, `modules/users`, migration, middleware e testes RBAC.
