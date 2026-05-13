# Api

Camada de backend fundacional do Ilex Logistica para autenticação, perfis e cadastro de transportadoras.

## Sprint A (11/05/2026 a 21/05/2026) - Entregas

- A-01: estrutura FastAPI modular + `/health`
- A-02: configuração de banco e sessão SQLAlchemy
- A-03: migrations iniciais (`users`, `roles`, `user_roles`, `carriers`)
- A-04: autenticação JWT (`/auth/login` e `/auth/refresh`)
- A-05: RBAC por perfil (`admin`, `logistica`, `gestor`, `auditoria`)
- A-06: CRUD de transportadoras com inativação lógica
- A-07: validações Pydantic e erro 422 padronizado
- A-08: suíte mínima automatizada para auth e carriers

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (produção/local), SQLite (testes)
- PyJWT

## Estrutura

```text
app/
  core/
  database/
  modules/
    auth/
    carriers/
    health/
    users/
  main.py
migrations/
tests/
```

## Configuração

Variáveis (prefixo `ILEX_`):

- `ILEX_DATABASE_URL` (ex.: `postgresql+psycopg2://postgres:postgres@localhost:5432/ilex`)
- `ILEX_JWT_SECRET`
- `ILEX_JWT_ALGORITHM` (default `HS256`)
- `ILEX_JWT_ACCESS_MINUTES` (default `30`)
- `ILEX_JWT_REFRESH_MINUTES` (default `1440`)

## Como executar

```bash
python -m pip install -e .[dev]
uvicorn app.main:app --reload
```

Healthcheck:

```bash
curl http://127.0.0.1:8000/health
```

## Banco e migrations

```bash
alembic upgrade head
alembic downgrade base
```

## Testes

```bash
pytest -q
```

Suite mínima da fundação:
- `tests/test_auth.py`
- `tests/test_rbac.py`
- `tests/test_carriers.py`

## Contrato técnico (A-09)

Documentado em `Docs/sprints/2026-05-11_2026-05-21/CONTRATO_API_FUNDACIONAL_A09.md`.

## Convenção de commits

`<tipo>(api): A-0X resumo em pt-BR`
