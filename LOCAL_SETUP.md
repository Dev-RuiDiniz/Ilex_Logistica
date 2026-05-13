# Local setup - Ilex Logística

## Objetivo

Padronizar variáveis locais para executar API e banco com `docker compose` durante a Sprint C.

## Pré-requisitos

- Docker com plugin Compose disponível no terminal.
- Repositórios `Api` e `Infra` clonados lado a lado dentro da pasta `ilex-logistica`.

## Configuração

1. Copie o template de ambiente:

```bash
cp .env.example .env
```

2. Substitua valores `change-me-local-only` por valores locais não produtivos.

3. Não commite `.env` nem secrets reais.

## Variáveis

| Variável | Uso | Exemplo local |
|---|---|---|
| `POSTGRES_DB` | Nome do banco PostgreSQL | `ilex` |
| `POSTGRES_USER` | Usuário local do PostgreSQL | `ilex` |
| `POSTGRES_PASSWORD` | Senha local do PostgreSQL | `change-me-local-only` |
| `POSTGRES_PORT` | Porta exposta do banco | `5432` |
| `API_PORT` | Porta exposta da API | `8000` |
| `ILEX_DATABASE_URL` | URL SQLAlchemy da API | `postgresql+psycopg2://ilex:change-me-local-only@db:5432/ilex` |
| `ILEX_JWT_SECRET` | Secret JWT local | `change-me-local-only` |
| `ILEX_JWT_ALGORITHM` | Algoritmo JWT | `HS256` |
| `ILEX_JWT_ACCESS_MINUTES` | Expiração do access token | `30` |
| `ILEX_JWT_REFRESH_MINUTES` | Expiração do refresh token | `1440` |
| `NEXT_PUBLIC_API_URL` | URL pública da API para o Web | `http://127.0.0.1:8000/api/v1` |

## Execução prevista

```bash
docker compose up --build
```

## Validação prevista

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/health
```

## Segurança

- Use apenas placeholders no repositório.
- Configure secrets reais somente no ambiente de deploy ou GitHub Actions secrets.
- Rotacione qualquer valor real exposto por acidente antes de abrir PR.
