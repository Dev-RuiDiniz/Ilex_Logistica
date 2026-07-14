# BETA_DEV_USERS_SEEDS

## Objetivo

Padronizar um seed oficial de usuarios para desenvolvimento, QA tecnico e homologacao local, evitando criacao manual de contas e divergencia entre perfis testados por backend, frontend e operacao.

## Problema

O projeto ja possuia RBAC, roles e testes usando usuarios recorrentes, mas nao havia um seed operacional versionado para:

- subir o ambiente local com acessos prontos
- validar login real contra a API
- alinhar README, QA e desenvolvimento em torno dos mesmos perfis

## Solucao Implementada

- Criado modulo [`apps/api/app/modules/users/seed_dev_users.py`](../apps/api/app/modules/users/seed_dev_users.py) com:
  - lista oficial de usuarios seed
  - senha padrao de desenvolvimento
  - execucao idempotente
  - garantia de roles e permissoes antes de popular usuarios
- Criado script [`scripts/seed_dev_users.py`](../scripts/seed_dev_users.py) para uso direto na raiz do monorepo
- Adicionado ajuste automatico para ler `infra/.env` e adaptar `db:5432` para `127.0.0.1:<POSTGRES_PORT>` quando o script roda fora do container
- Adicionada migration [`apps/api/migrations/versions/20260627_02_add_role_description.py`](../apps/api/migrations/versions/20260627_02_add_role_description.py) para alinhar o schema real do Postgres ao modelo `Role`

## Usuarios Registrados

| Perfil | E-mail | Senha |
|--------|--------|-------|
| Admin | `admin@ilex.com` | `123456` |
| Manager | `manager@ilex.com` | `123456` |
| Operator | `operator@ilex.com` | `123456` |
| Viewer | `viewer@ilex.com` | `123456` |
| Logistica | `logistica@ilex.com` | `123456` |
| Gestor | `gestor@ilex.com` | `123456` |
| Auditoria | `audit@ilex.com` | `123456` |

## Criterios de Aceite

- seed cria os 7 usuarios padrao
- execucao repetida nao duplica registros
- roles do usuario sao restauradas na reexecucao
- login real funciona com o usuario admin seed
- README expone como usar os acessos no ambiente local

## Testes

- `python -m pytest tests/test_dev_user_seeds.py -q`
- `python scripts/validate_migrations.py`

## Observacoes

- Credenciais destinam-se apenas a desenvolvimento e homologacao controlada
- Em producao, os usuarios devem ser criados com senhas seguras e governanca apropriada
