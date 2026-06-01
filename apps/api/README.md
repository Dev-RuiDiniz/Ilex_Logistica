# Api

Camada de backend do Ilex Logistica para autenticacao, autorizacao por perfil, cadastro de transportadoras e evolucao do core logistico.

## Sprint 1 oficial (12/05/2026 a 23/05/2026)

Objetivo da trilha A: entregar fundacao tecnica da API com rastreabilidade Scrum ativa.

### Backlog da trilha A

- A-01 a A-10 (referencia em `Docs/sprints/2026-05-12_2026-05-23/`)

### Evidencias de execucao

- PR fundacional mergeada: `https://github.com/ilex-logistica/Api/pull/1`
- Issues de execucao derivadas de Docs: `#2` a `#9`
- Milestones oficiais aplicadas: Sprint 01..Sprint 05

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- PyJWT

## Estrutura

```text
app/
  core/
  database/
  modules/
migrations/
tests/
```

## Como executar

```bash
python -m pip install -e .[dev]
uvicorn app.main:app --reload
```

## Testes

```bash
python -m pytest -q
```

## Regra de rastreio obrigatoria

Toda issue/PR deve informar:

- Epic (Docs)
- Issue de origem (Docs)
- Sprint/Milestone

## CI local

Comandos equivalentes ao workflow `API CI`:

```bash
python -m pip install -e .[dev]
python -m ruff check .
python -m pytest -q
```

O workflow executa em `pull_request` e em `push` para `main`.

## Convencao de commits

`<tipo>(api): <ID> <resumo em pt-BR>`
