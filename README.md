# Web

Camada frontend do Ilex Logística para operação diária, acompanhamento gerencial e tratamento de exceções logísticas.

## Objetivo no MVP

Entregar uma aplicação web responsiva com visão executiva e operacional, priorizando ações sobre entregas críticas.

## Responsabilidades do repositório

- Login e controle de sessão no frontend
- Dashboard logístico com KPIs
- Fluxo de importação e validação de dados
- Listagem e detalhe de entregas
- Painel de exceções com priorização
- Registro de tratativas
- Consulta de relatórios e auditoria

## Stack prevista

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- Recharts

## Estrutura sugerida

```text
src/
  app/
  components/
  features/
    auth/
    dashboard/
    carriers/
    imports/
    shipments/
    exceptions/
    reports/
    settings/
    audit/
lib/
services/
public/
```

## Backlog prioritário (LOG-*)

- LOG-003: Criar autenticação JWT (integração front)
- LOG-004: Criar perfis de acesso
- LOG-006: Criar importador Excel/CSV
- LOG-008: Criar prévia de importação
- LOG-011: Criar listagem de entregas
- LOG-012: Criar detalhe da entrega
- LOG-017: Criar painel de exceções
- LOG-018: Criar registro de tratativas
- LOG-023: Criar dashboard logístico final

## Critérios de aceite iniciais

- Acesso protegido por perfil
- Telas principais com filtros operacionais
- Painel de exceções destacando criticidade
- Fluxo de tratativa auditável na interface

## Convenção de commits

`<tipo>(web): <ID> <resumo em pt-BR>`

Exemplo: `docs(web): LOG-001 define escopo funcional do frontend`
