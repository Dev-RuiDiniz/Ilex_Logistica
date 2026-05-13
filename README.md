# Web

Aplicação administrativa da Ilex Logística para autenticação, controle por perfil e gestão de transportadoras.

## Sprint B (11/05/2026 a 21/05/2026)

- B-01: scaffold Next.js + TypeScript + lint
- B-02: layout autenticado responsivo
- B-03: tela de login integrada à API
- B-04: proteção de rotas privadas
- B-05: visibilidade de ações por perfil
- B-06: listagem de transportadoras com filtro
- B-07: formulário de cadastro/edição
- B-08: inativação com confirmação

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Vitest + Testing Library

## Estrutura principal

```text
src/
  app/
    (private)/
    login/
  components/
  features/auth/
  lib/
```

## Configuração

Variáveis de ambiente:

- `NEXT_PUBLIC_API_URL` (default: `http://127.0.0.1:8000/api/v1`)

## Comandos

```bash
npm install
npm run dev
npm run lint
npm run test
```

## Fluxo de acesso

1. Login em `/login`.
2. Sessão salva localmente + cookie de autenticação.
3. Rotas privadas protegidas por middleware.
4. Controle de ações por perfil em `carriers`.

## Convenção de commits

`<tipo>(web): B-0X resumo em pt-BR`
