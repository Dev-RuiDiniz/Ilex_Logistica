# BETA-027 — Alertas e Notificações

**Data:** 2026-06-17  
**Branch:** `feature/beta-027-alerts-notifications`

## Objetivo

Concluir o Épico 5 com a camada operacional de alertas, notificações e registro de entrega, mantendo a integração com dashboard, exceções e frontend de alertas.

## Entregas realizadas

### Backend
- Adicionado `AlertDeliveryLog` para registrar geração, leitura, resolução, resolução automática e duplicidades ignoradas.
- Implementada geração de alertas para:
  - `sla_critical`
  - `sla_late`
  - `sla_warning`
  - `unknown_sla`
  - `no_update`
  - `import_failure`
- Implementada deduplicação por origem, preservando apenas um alerta ativo por `source_type`/`source_id`.
- Integrado o fluxo de leitura e resolução com logs de entrega.
- Corrigidos filtros do painel de exceções para `sla_status` e `is_late`.
- Corrigido o cálculo do `delay_days` no payload do painel de exceções para usar o valor calculado pelo SLA.
- Ajustado o dashboard para usar contadores reais de alertas e falhas de importação.

### Frontend
- Atualizado o client de alertas para incluir o tipo `no_update`.
- Atualizada a página de alertas com filtro para `no_update`.
- Mantida a compatibilidade dos testes da página e do client.

### Testes
- Backend validado com:
  - `./venv/bin/pytest tests/test_alerts_generation.py tests/test_alerts_api.py tests/test_dashboard_summary.py tests/test_dashboard_alerts_integration.py tests/test_exceptions_panel_sla.py tests/test_exceptions_panel_api.py tests/test_rbac_alerts_api.py`
- Frontend validado com:
  - `npm test -- "src/lib/alerts-api.test.ts" "src/app/(private)/alerts/alerts-page.test.tsx"`

### Resultado
- Backend: **88 passed**
- Frontend: **19 passed**

## Observações

- As integrações por e-mail e SMS continuam como pós-beta.
- Não houve merge nesta etapa; a entrega foi preparada para PR.
- O registro vivo do projeto foi atualizado em `CONTEXTO.md` e `RELATORIO_DIA.md`.
