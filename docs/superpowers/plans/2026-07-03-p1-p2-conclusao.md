# Conclusão de P1 e P2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconciliar indicadores e concluir o endurecimento operacional de P1/P2 com contratos, políticas e evidências automatizadas.

**Architecture:** Um módulo compartilhado delimita o universo de shipments e calcula métricas antes de dashboard, eficiência e listagem consumirem os resultados. P2 mantém os módulos existentes, substitui testes vazios, adiciona fixtures/E2E e formaliza políticas por configuração e specs.

**Tech Stack:** FastAPI, SQLAlchemy, Pydantic, pytest, Next.js 16, React 19, TypeScript, Vitest e Playwright.

---

### Task 1: Universo filtrado e reconciliação P1

**Files:**
- Create: `apps/api/app/modules/shipments/metrics.py`
- Create: `apps/api/tests/fixtures/homologation_efficiency.csv`
- Create: `apps/api/tests/test_p1_metrics_reconciliation.py`
- Modify: `apps/api/app/modules/shipments/analytics_service.py`
- Modify: `apps/api/app/modules/dashboard/service.py`
- Modify: `apps/api/app/modules/shipments/service.py`

- [ ] Escrever testes que montam um dataset com no prazo, atraso, extravio, NF zero e frete ausente e exigem o mesmo total sob filtros equivalentes.
- [ ] Executar `python -m pytest -q tests/test_p1_metrics_reconciliation.py` e confirmar RED por divergência das populações.
- [ ] Implementar filtro compartilhado e agregador decimal com `lost` explícito e população financeira válida.
- [ ] Fazer dashboard e eficiência consumirem o universo comum; manter a listagem server-side no mesmo contrato.
- [ ] Executar testes focados e suíte API; commitar `feat(dashboard): reconcilia indicadores por janela de filtros`.

### Task 2: Ranking determinístico e contrato Web

**Files:**
- Modify: `apps/api/app/modules/shipments/analytics_service.py`
- Modify: `apps/api/app/modules/shipments/analytics_schemas.py`
- Modify: `apps/web/src/lib/types.ts`
- Modify: `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/page.tsx`
- Modify: `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page.test.tsx`

- [ ] Criar RED para empate resolvido por extravio, custo e nome e para média calculada apenas sobre linhas válidas.
- [ ] Implementar chave `(-on_time_percentage, lost_percentage, average_freight_percentage, carrier_name)` e expor população válida.
- [ ] Atualizar a Web para explicar fórmula/população sem recalcular o domínio.
- [ ] Executar testes API/Web focados e commitar `feat(shipments): torna ranking de eficiência determinístico`.

### Task 3: Exceções e tratativas reais

**Files:**
- Rewrite: `apps/api/tests/test_exceptions_panel_sla.py`
- Modify: `apps/api/app/modules/shipments/exceptions_service.py`
- Modify: `apps/api/tests/test_exceptions_panel_api.py`

- [ ] Substituir cada `pass` por casos com fixtures reais para SLA, prioridade, filtros, totais e alterações refletidas.
- [ ] Executar o arquivo e confirmar RED nos comportamentos ausentes, não em placeholders sintáticos.
- [ ] Corrigir somente divergências comprovadas no serviço/API.
- [ ] Cobrir `404`, `401` e `403`; executar testes focados e commitar `test(shipments): cobre painel de exceções e tratativas`.

### Task 4: XLSX, Braspress e E2E de importação

**Files:**
- Modify: `apps/web/e2e/fixtures/test-data.ts`
- Create: `apps/web/e2e/fixtures/import-valid.xlsx`
- Modify: `apps/web/e2e/import-csv.spec.ts`
- Create: `apps/web/e2e/import-xlsx.spec.ts`
- Modify: `apps/api/tests/fixtures/imports/braspress_valid.csv`
- Modify: `docs/BRASPRESS_IMPORTACAO_ASSISTIDA.md`
- Modify: `docs/specs/03-importacoes-braspress.md`

- [ ] Gerar fixture XLSX sanitizada a partir do contrato atual e validar cabeçalhos no teste.
- [ ] Criar fluxo Playwright upload → preview → confirmação → resultado, interceptando apenas o limite HTTP quando backend real não estiver disponível.
- [ ] Versionar layout Braspress e testar a amostra sanitizada na API.
- [ ] Executar testes de importação API/Web/E2E disponíveis e commitar `test(imports): cobre fluxo XLSX e homologa layout Braspress`.

### Task 5: E2E de exceções até histórico

**Files:**
- Modify: `apps/web/e2e/exceptions-sla.spec.ts`
- Modify: `apps/web/src/app/(private)/shipments/[id]/page.tsx`
- Modify: testes do detalhe de shipment aplicáveis.

- [ ] Escrever E2E RED para painel → detalhe → nova tratativa → histórico ordenado.
- [ ] Ajustar seletores/feedback somente se o fluxo real não oferecer contratos acessíveis.
- [ ] Executar Vitest e Playwright focados; commitar `test(shipments): cobre tratativa ponta a ponta`.

### Task 6: Matriz completa de RBAC

**Files:**
- Create: `apps/api/tests/test_private_routes_matrix.py`
- Modify: arquivos `test_rbac_*_api.py` somente para remover duplicação coberta.

- [ ] Catalogar rotas privadas registradas pelo FastAPI e definir método, permissão e payload mínimo.
- [ ] Criar teste parametrizado de sucesso, sem credencial `401` e sem permissão `403` para os domínios P2.
- [ ] Corrigir dependências de permissão inconsistentes sem ampliar acesso.
- [ ] Executar matriz e suíte API; commitar `test(auth): completa matriz de rotas privadas`.

### Task 7: Política de senha e ciclo de tokens

**Files:**
- Modify: `apps/api/app/core/config.py`
- Modify: `apps/api/app/core/security.py`
- Modify: `apps/api/app/modules/auth/service.py`
- Modify: `apps/api/app/modules/auth/schemas.py`
- Modify: `apps/api/app/modules/users/models.py`
- Create: nova migration Alembic para versão/revogação de sessão
- Create: `apps/api/tests/test_auth_policies.py`
- Modify: `docs/specs/01-autenticacao-usuarios-rbac.md`

- [ ] Criar RED para senha mínima/complexidade, access de 15 minutos, refresh de 7 dias, rotação e revogação.
- [ ] Implementar validação na entrada e versão de sessão persistida, sem armazenar tokens crus.
- [ ] Fazer refresh emitir novo par e invalidar o refresh anterior; verificar usuário ativo.
- [ ] Validar migration upgrade/downgrade, suíte auth e commitar `feat(auth): endurece senhas e rotação de tokens`.

### Task 8: Políticas de alertas, relatórios e auditoria

**Files:**
- Modify: `apps/api/app/core/config.py`
- Modify: `apps/api/app/modules/alerts/service.py`
- Modify: `apps/api/app/modules/reports/service.py`
- Modify: specs 09, 10 e 11
- Create: `apps/api/tests/test_operational_policies.py`
- Modify: infraestrutura/agendamento aplicável em `infra/`

- [ ] Criar RED para canal externo desabilitado sem destinatário, três tentativas, estado final e escalonamento interno.
- [ ] Formalizar geração diária às 06:00 `America/Sao_Paulo`, retenção de relatório por 365 dias e auditoria por 5 anos.
- [ ] Implementar apenas mecanismos existentes/configuráveis; registrar descarte futuro sem apagar logs automaticamente.
- [ ] Executar testes focados/infra e commitar `feat(alerts): formaliza políticas operacionais`.

### Task 9: UAT técnico e encerramento documental

**Files:**
- Create: `docs/uat/P1_P2_UAT.md`
- Modify: specs 01, 03, 05–11 e índice
- Modify: `ROADMAP.md`, `ESCOPO.md`, `CONTEXTO.md`, `RELATORIO.md`, `BANCO_DADOS.md` se houver migration

- [ ] Executar dataset controlado e registrar resultados reproduzíveis, distinguindo UAT técnico de aceite humano.
- [ ] Executar API, Ruff, Web, lint, build, E2E disponível, migrations, infra, docs, secrets e `git diff --check`.
- [ ] Atualizar estados somente com evidência fresca; manter aceite do cliente pendente onde não houver assinatura.
- [ ] Commitar `docs(docs): registra UAT técnico de P1 e P2`.
- [ ] Revisar todos os commits, confirmar worktree e fazer um único `git push origin main`.
