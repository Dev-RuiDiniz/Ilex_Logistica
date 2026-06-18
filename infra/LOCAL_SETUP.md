# Local setup - Ilex Logística

## Objetivo

Padronizar variáveis locais para executar API e banco com `docker compose` durante a Sprint C.

## Pré-requisitos

- Docker com plugin Compose disponível no terminal.
- Monorepo `Ilex_Logistica` clonado localmente com a estrutura `apps/api`, `apps/web` e `infra/`.

## Configuração

1. Copie o template principal de ambiente:

```bash
cp .env.example .env
```

2. Para execução fora do compose, use também os templates específicos:

```bash
cp env/api.env.example ../apps/api/.env
cp env/web.env.example ../apps/web/.env.local
```

3. Substitua valores `change-me-local-only` por valores locais não produtivos.

4. Não commite `.env`, `.env.local` nem secrets reais.

## Variáveis obrigatórias

| Variável | Serviço | Secret | Uso | Exemplo local |
|---|---|---:|---|---|
| `POSTGRES_DB` | DB | Não | Nome do banco PostgreSQL | `ilex` |
| `POSTGRES_USER` | DB | Não | Usuário local do PostgreSQL | `ilex` |
| `POSTGRES_PASSWORD` | DB | Sim | Senha local do PostgreSQL | `change-me-local-only` |
| `ILEX_DATABASE_URL` | API | Sim | URL SQLAlchemy usada pela API | `postgresql+psycopg2://ilex:change-me-local-only@db:5432/ilex` |
| `ILEX_JWT_SECRET` | API | Sim | Chave de assinatura JWT local | `change-me-local-only-replace-with-local-secret` |
| `NEXT_PUBLIC_API_URL` | Web | Não | URL pública da API para o frontend | `http://127.0.0.1:8000/api/v1` |

## Variáveis opcionais

| Variável | Serviço | Secret | Uso | Default |
|---|---|---:|---|---|
| `POSTGRES_PORT` | DB | Não | Porta exposta do banco no host | `5432` |
| `API_PORT` | API | Não | Porta exposta da API no host | `8000` |
| `ILEX_APP_NAME` | API | Não | Nome da aplicação FastAPI | `Ilex API` |
| `ILEX_ENVIRONMENT` | API | Não | Ambiente lógico da API | `dev` |
| `ILEX_JWT_ALGORITHM` | API | Não | Algoritmo JWT | `HS256` |
| `ILEX_JWT_ACCESS_MINUTES` | API | Não | Expiração do access token | `30` |
| `ILEX_JWT_REFRESH_MINUTES` | API | Não | Expiração do refresh token | `1440` |

## Execução prevista

```bash
docker compose up --build
```

Se a porta `5432` já estiver em uso no host, ajuste `POSTGRES_PORT` no `infra/.env` para uma porta livre, como `5433`.

## Parada do ambiente

```bash
docker compose down
```

## Limpeza de ambiente local

```bash
docker compose down --volumes --remove-orphans
```

## Validação prevista

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/health
```

Verificação dos serviços:

```bash
docker compose ps
docker compose logs --tail=100 api db
docker compose logs api
docker compose logs db
```

Diagnóstico detalhado de saúde, logs e falha simulada do DB está em `OBSERVABILITY.md`.

Verificação de acesso do banco para migrations:

```bash
docker compose exec api alembic current
docker compose exec api alembic upgrade head
```

## Troubleshooting

Se a API não subir:

```bash
docker compose logs api
```

Se o banco estiver indisponível:

```bash
docker compose logs db
docker compose ps
```

Se migrations falharem:

```bash
docker compose exec api alembic current
docker compose exec api alembic upgrade head
```

Se precisar reiniciar tudo sem preservar dados locais:

```bash
docker compose down --volumes --remove-orphans
docker compose up --build
```

## Segurança

- Use apenas placeholders no repositório.
- Configure secrets reais somente no ambiente de deploy ou GitHub Actions secrets.
- Rotacione qualquer valor real exposto por acidente antes de abrir PR.
- Mantenha `.env`, `.env.local` e arquivos derivados fora do Git.
- Versione apenas `.env.example` e `env/*.env.example`.

## Checklist de setup local

- [ ] Docker com plugin Compose disponível no terminal.
- [ ] Monorepo `Ilex_Logistica` clonado com `apps/api`, `apps/web` e `infra/`.
- [ ] Arquivo `.env` criado a partir de `.env.example`.
- [ ] Secrets locais substituídos por valores não produtivos.
- [ ] Nenhum `.env` real aparece em `git status --short`.
- [ ] `docker compose config` executado sem erro.
- [ ] `docker compose up --build` executado.
- [ ] API validada em `http://127.0.0.1:8000/health`.
- [ ] DB validado com `docker compose exec api alembic current`.
