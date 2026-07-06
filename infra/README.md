# Infra

Camada de infraestrutura do Ilex Logistica para ambientes consistentes, CI/CD e operacao monitoravel.

## Sprint 1 oficial (12/05/2026 a 23/05/2026)

Objetivo da trilha C: garantir ambiente reproduzivel, CI minimo e governanca de execucao.

### Backlog da trilha C

- C-01 a C-10 (referencia em `Docs/sprints/2026-05-12_2026-05-23/`)

### Evidencias de execucao

- PR fundacional mergeada: `https://github.com/ilex-logistica/Infra/pull/1`
- Issues de execucao: `#2`, `#3`, `#4`
- Milestones oficiais aplicadas: Sprint 01..Sprint 05

## Responsabilidades

- ambiente local/homologacao
- padrao de variaveis e secrets
- pipelines GitHub Actions
- observabilidade inicial e healthchecks

## Regra de rastreio obrigatoria

Toda issue/PR deve informar:

- Epic (Docs)
- Issue de origem (Docs)
- Sprint/Milestone

## Convencao de commits

`<tipo>(infra): <ID> <resumo em pt-BR>`

## Produção e continuidade

Produção usa `docker-compose.prod.yml`, Caddy/TLS e redes privadas para PostgreSQL/Redis. Backup, restore, deploy e rollback estão descritos em `CONTINUITY.md`; os scripts correspondentes ficam em `infra/scripts/`.
