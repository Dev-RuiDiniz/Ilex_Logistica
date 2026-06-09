# Ilex Logística Monorepo

Monorepositório oficial da plataforma Ilex Logística, consolidando API, frontend web, infraestrutura, integrações e documentação técnica em uma única base versionada.

## Visão Geral

Este repositório centraliza os módulos que antes estavam distribuídos em múltiplos repositórios da organização.  
Objetivo: simplificar colaboração, rastreabilidade, evolução arquitetural e governança técnica.

## Arquitetura do Monorepo

```text
.
├── .github/         # Workflows, templates e configurações de automação
├── apps/
│   ├── api/         # Backend/API (Python)
│   └── web/         # Frontend (Next.js/TypeScript)
├── infra/           # Docker, ambiente local, observabilidade e checks
├── integrations/    # Guias e artefatos de integrações
└── docs/            # ADRs, arquitetura, QA, atas, sprints e roadmaps
```

## Pré-requisitos

- Git 2.40+
- Python 3.12+ (para `apps/api` e scripts Python)
- Node.js 20+ e npm 10+ (para `apps/web`)
- Docker e Docker Compose (para `infra`)

## Setup Local

### 1) Clonar o monorepo

```bash
git clone https://github.com/Dev-RuiDiniz/Ilex_Logistica.git
cd Ilex_Logistica
```

### 2) API (`apps/api`)

```bash
cd apps/api
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate
pip install -e .
pytest
```

### 3) Web (`apps/web`)

```bash
cd apps/web
npm install
npm run dev
```

Comandos úteis:

```bash
npm run test
npm run build
npm run lint
```

### 4) Infra (`infra`)

```bash
cd infra
cp .env.example .env
docker compose up -d
```

Para detalhes adicionais:

- `infra/LOCAL_SETUP.md`
- `infra/OBSERVABILITY.md`

## Comandos por Módulo

- API: `pytest`
- Web: `npm run test`, `npm run build`, `npm run lint`
- Infra: `docker compose up -d`, checks locais em `infra/infra_checks.py`
- Docs: atualização de artefatos em `docs/` conforme governança interna

## Fluxo de Contribuição

1. Crie branch a partir de `main`:
   - `feature/<tema>`
   - `fix/<tema>`
   - `chore/<tema>`
2. Faça commits pequenos e orientados por tarefa.
3. Abra PR com descrição objetiva, contexto e evidências (logs, screenshots, links).
4. Aguarde validações e revise antes do merge.

### Convenção de Commit

Padrão recomendado (pt-BR + escopo):

- `feat(api): adiciona endpoint de ...`
- `fix(web): corrige validação de ...`
- `chore(infra): ajusta compose para ...`
- `docs(readme): atualiza guia de setup`

## Validação Beta

Para validação automatizada da fase beta, consulte:

- [Comandos Oficiais](docs/BETA_COMMANDS.md)
- [Checklist Beta](docs/BETA_CHECKLIST.md)
- [Gates de Liberação](docs/BETA_RELEASE_GATE.md)

### Comandos Rápidos

```bash
# Secret scan
python scripts/check_secrets.py --repo-root .

# Migrations
python scripts/validate_migrations.py

# Validação beta agregada
python scripts/beta_validate.py
```

Para detalhes completos, veja a documentação beta em `docs/`.

## Status Atual

- Monorepo consolidado com histórico preservado dos domínios:
  - `.github`
  - `Api` → `apps/api`
  - `Web` → `apps/web`
  - `Infra` → `infra`
  - `Integrations` → `integrations`
  - `Docs` → `docs`
- Estrutura pronta para evolução incremental de CI e automações por domínio.

## Roadmap Macro

- Fase 1 (concluída): consolidação estrutural e documental do monorepo.
- Fase 2: adaptação de CI/CD por path e validações por domínio.
- Fase 3: otimização de pipelines, versionamento e automações de release.

## Origem dos Módulos (Rastreabilidade)

Este monorepo foi formado a partir dos seguintes repositórios:

- `https://github.com/ilex-logistica/.github`
- `https://github.com/ilex-logistica/Api`
- `https://github.com/ilex-logistica/Web`
- `https://github.com/ilex-logistica/Infra`
- `https://github.com/ilex-logistica/Integrations`
- `https://github.com/ilex-logistica/Docs`

O histórico de commits foi preservado durante a migração via `git subtree`.
