# CONTEXTO.md — Estado Vivo do Ilex Logística

**Atualizado em:** 2026-07-02

## 2026-07-02 — Consolidação de governança

### Estado atual

- Monorepo com API FastAPI/SQLAlchemy/Alembic e Web Next.js/React.
- Domínios presentes: autenticação, usuários/RBAC, transportadoras, entregas/importações, envios/tratativas, SLA, dashboard, alertas, relatórios e auditoria.
- PostgreSQL 16 está configurado no Docker Compose; a configuração da aplicação também admite SQLite em desenvolvimento/testes.
- O Apêndice 1 foi incorporado como fonte de requisitos complementares.
- Os documentos raiz de arquitetura, banco, escopo, roadmap e relatório foram consolidados a partir do código atual.
- `ESCOPO.md` passou a consolidar o escopo completo e `docs/specs/` contém 12 especificações SDD por domínio, com índice e rastreabilidade LOG-027 a LOG-041.

### Decisões

- Código, migrations e testes prevalecem sobre alegações históricas de documentação.
- Requisitos do apêndice sem evidência ficam como planejados ou pendentes, nunca como concluídos.
- Cotação de frete por pedido será tratada como evolução separada, iniciando por importação assistida.
- Credenciais de ERP e transportadoras não serão persistidas em documentação ou frontend.
- `RELATORIO.md` substitui o arquivo histórico `RELATORIO_DIA.md` removido.
- Toda mudança funcional deve atualizar primeiro a spec do domínio e seus critérios de aceite antes do ciclo TDD.

### Dependências e bloqueios

- Contrato, autenticação, campos e ambiente de homologação do ERP: **A CONFIRMAR**.
- APIs e tabelas negociadas das transportadoras: **A CONFIRMAR**.
- Regra operacional de SLA/no prazo/extravio: requer homologação do cliente.
- Aderência integral dos filtros e métricas financeiras do Apêndice 1: requer teste funcional ponta a ponta.

### Próximos passos

1. Homologar LOG-027 a LOG-035 contra dados reais e fechar lacunas de filtros/indicadores.
2. Especificar contrato mínimo de pedidos do ERP (LOG-038).
3. Implementar o MVP assistido de cotação (LOG-036/037/039/040) via SDD e TDD.
4. Preservar e validar o fluxo Braspress sem credenciais (LOG-041).

## Histórico preservado

### 2026-06-24 — Segurança e RBAC frontend

Foi registrado tratamento de `401/403`, helpers de permissões, navegação condicional, componente `AccessDenied` e adaptação de páginas. O repositório atual contém testes de permissões, middleware, navegação e páginas privadas.

### 2026-06 — Beta operacional

O histórico Git e as migrations demonstram evolução incremental de fundação, imports, deliveries, shipments, campos fiscais, SLA, alertas, relatórios, auditoria e permissões. Documentos históricos detalhados foram removidos em 2026-07-02 por decisão explícita do usuário; as evidências permanentes continuam no Git.

## Notas técnicas

- Backend: Python >=3.11, FastAPI, SQLAlchemy 2, Alembic, Pydantic Settings, pytest.
- Frontend: Next.js 16, React 19, TypeScript 5, Tailwind 4, Vitest, Testing Library e Playwright.
- Validadores: `validate_docs.py`, `validate_migrations.py`, `check_secrets.py` e `beta_validate.py`.
- Não registrar números de testes como permanentes sem executar as suítes na mesma sessão.
