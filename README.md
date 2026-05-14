# Web

Aplicacao administrativa do Ilex Logistica para autenticacao, controle por perfil e operacao de transportadoras.

## Sprint 1 oficial (12/05/2026 a 23/05/2026)

Objetivo da trilha B: habilitar fluxo web fundacional com login, guardas de rota e CRUD inicial de transportadoras.

### Backlog da trilha B

- B-01 a B-10 (referencia em `Docs/sprints/2026-05-12_2026-05-23/`)

### Evidencias de execucao

- PR fundacional mergeada: `https://github.com/ilex-logistica/Web/pull/1`
- Issues de execucao derivadas de Docs: `#2` a `#7`
- Milestones oficiais aplicadas: Sprint 01..Sprint 05

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Vitest + Testing Library

## Configuracao

- `NEXT_PUBLIC_API_URL` (default `http://127.0.0.1:8000/api/v1`)

## Comandos

```bash
npm install
npm run dev
npm run lint
npm run test
npm run build
```

## CI local

Comandos equivalentes ao workflow `Web CI`:

```bash
npm ci
npm run lint
npm run build
```

O workflow executa em `pull_request` e em `push` para `main`.

## Regra de rastreio obrigatoria

Toda issue/PR deve informar:

- Epic (Docs)
- Issue de origem (Docs)
- Sprint/Milestone

## Convencao de commits

`<tipo>(web): <ID> <resumo em pt-BR>`
