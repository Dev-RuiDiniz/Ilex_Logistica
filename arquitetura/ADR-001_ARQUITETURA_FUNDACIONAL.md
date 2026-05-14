# ADR-001 - Arquitetura fundacional do Ilex Logística

## Status

Proposto para revisão técnica na Sprint 1.

## Contexto

O MVP do Ilex Logística precisa sustentar desenvolvimento incremental em 45 dias, com separação clara entre API, Web, Infra, Integrações e documentação. A Sprint C estabelece a base de ambiente reproduzível, CI mínimo, observabilidade inicial e governança Scrum.

## Decisão

Adotar arquitetura distribuída por repositórios especializados:

| Repositório | Responsabilidade | Stack |
|---|---|---|
| `Api` | Backend, autenticação, regras de negócio, cadastro de transportadoras e endpoints | FastAPI, SQLAlchemy, Alembic, PostgreSQL |
| `Web` | Interface administrativa, autenticação, rotas privadas e operação diária | Next.js, TypeScript, Tailwind CSS |
| `Infra` | Docker Compose, variáveis, deploy, CI/CD e observabilidade | Docker, PostgreSQL, GitHub Actions |
| `Integrations` | Conectores, clients externos, bots e normalização de dados | Python workers, APIs, Playwright quando necessário |
| `Docs` | Escopo, sprints, ADRs, QA, riscos e operação | Markdown |
| `.github` | Templates e governança organizacional | GitHub templates |

## Alternativas consideradas

| Alternativa | Motivo para não adotar agora |
|---|---|
| Monorepo único | Aumentaria acoplamento e risco de mudanças cruzadas no início do projeto. |
| Deploy manual sem Docker | Reduziria reprodutibilidade e dificultaria onboarding/QA. |
| CI apenas no final da Sprint 1 | Aumentaria risco de regressões em API/Web durante as próximas trilhas. |
| Kubernetes desde o início | Complexidade operacional incompatível com o estágio atual do MVP. |

## Consequências

- Cada repositório mantém responsabilidades claras e commits rastreáveis por tarefa.
- O ambiente local deve ser documentado e reproduzível via `Infra`.
- API e Web passam a ter validação automática mínima em PR/push.
- Secrets reais devem ficar fora do Git e ser tratados por ambiente.
- A integração entre repositórios exige disciplina de documentação e versionamento de contratos.

## Critérios de aceite

- Decisão registra contexto, alternativas, escolha e consequências.
- Decisão referencia os repositórios oficiais do projeto.
- Decisão fica disponível para revisão técnica antes do merge da Sprint C.

## Evidência de validação

- Documento versionado no repositório `Docs`.
- Revisão esperada na Pull Request da Sprint C.
