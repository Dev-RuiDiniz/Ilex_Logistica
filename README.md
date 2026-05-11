# Ilex Logística - Organização GitHub

Plataforma web para rastreio automatizado de entregas, identificação de atrasos e tratamento de exceções operacionais.

## Visão executiva

O projeto Ilex Logística será entregue como MVP avançado em 45 dias, com foco em:

- Centralização de dados logísticos
- Monitoramento de atrasos e criticidade
- Painel de exceções para ação humana
- Relatório diário matinal para operação e gestão

## Mapa de repositórios

| Repositório | Responsabilidade | Stack principal |
|---|---|---|
| `Api` | API principal, regras de prazo/SLA, exceções, alertas e relatórios | FastAPI, SQLAlchemy, PostgreSQL |
| `Web` | Dashboard e operação logística web responsiva | Next.js, TypeScript, Tailwind |
| `Infra` | Ambientes, containerização, CI/CD e observabilidade | Docker, Nginx, GitHub Actions |
| `Integrations` | Conectores de transportadoras, bots e adaptadores | Python workers, clients de API |
| `Docs` | Escopo, sprints, guias técnicos e materiais de operação | Markdown |
| `.github` | Governança, visão organizacional e padrões globais | GitHub Templates/Docs |

## Stack macro

- Backend: Python, FastAPI, SQLAlchemy, Pydantic, jobs assíncronos
- Frontend: Next.js, TypeScript, Tailwind CSS
- Banco de dados: PostgreSQL
- Infra: Docker, Nginx, GitHub Actions
- Integrações: APIs de transportadoras, importação Excel/CSV e bots controlados

## Cronograma macro (45 dias)

- Sprint 1: 11/05/2026 a 21/05/2026 - Fundação
- Sprint 2: 22/05/2026 a 01/06/2026 - Core Logístico
- Sprint 3: 02/06/2026 a 13/06/2026 - Exceções e Relatório
- Sprint 4: 14/06/2026 a 24/06/2026 - Integrações, QA e Deploy

## Convenção de commits

Padrão adotado:

`<tipo>(<repo>): <ID> <resumo em pt-BR>`

Exemplos:

- `docs(api): LOG-007 detalha validacao de colunas obrigatorias`
- `feat(web): LOG-016 cria painel inicial de excecoes`
- `chore(infra): LOG-001 ajusta base de organizacao`

## Referência do escopo

Documento base: `ESCOPO_PROJETO_ILEX_LOGISTICA.pdf` (DB Tecnologia, 11/05/2026).
