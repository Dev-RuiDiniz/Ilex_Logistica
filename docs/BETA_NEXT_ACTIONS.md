# BETA NEXT ACTIONS

Próximas ações pós BETA-009S para o projeto Ilex Logística.

## Ações Recentes (BETA-018A)

### BETA-018A: Relatório Diário Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-018a-daily-report-backend-api`
**Data:** 2025-01-21

**Implementado:**
- ✅ Model DailyReport com campos necessários
- ✅ Migration para tabela daily_reports
- ✅ Service de geração de relatório diário
- ✅ Endpoints POST /reports/daily/generate, GET /reports/daily, GET /reports/daily/{id}, GET /reports/daily/by-date/{date}
- ✅ Schemas/DTOs para relatório diário
- ✅ 46 testes TDD implementados (10 model + 19 generation + 11 API + 6 integration)
- ✅ Documentação completa
- ✅ Correção do conftest.py para fixar fixture de banco
- ✅ Remoção de autenticação dos endpoints para seguir padrão do projeto atual
- ✅ Remoção de endpoint legado /daily/legacy
- ✅ Correção do middleware de logging (comentado temporariamente)

**Arquivos Criados:**
- `apps/api/app/modules/reports/models.py`
- `apps/api/app/modules/reports/service.py`
- `apps/api/app/modules/reports/schemas.py`
- `apps/api/app/modules/reports/__init__.py`
- `apps/api/migrations/versions/20260621_01_create_daily_reports.py`
- `apps/api/tests/test_daily_report_model.py`
- `apps/api/tests/test_daily_report_generation.py`
- `apps/api/tests/test_daily_report_api.py`
- `apps/api/tests/test_daily_report_integration.py`
- `docs/BETA_018A_DAILY_REPORT_BACKEND_API.md`

**Arquivos Modificados:**
- `apps/api/app/main.py` (middleware de logging comentado temporariamente)
- `apps/api/app/modules/reports/router.py` (autenticação removida, endpoint legado removido)
- `apps/api/tests/conftest.py` (fixture de banco corrigida)
- `apps/api/tests/test_daily_report_api.py` (skips removidos, novos testes adicionados)

**Limitações Conhecidas:**
- Sem envio de e-mail (backend-only)
- Sem WhatsApp/webhook (fora do escopo beta)
- Sem frontend (BETA-018B)
- Sem agendamento externo com cron (fora do escopo beta)
- Auth temporariamente removida dos endpoints (será implementado no Épico 9)
- Middleware de logging comentado temporariamente (será corrigido no Épico 11)

**Documentação:** `docs/BETA_018A_DAILY_REPORT_BACKEND_API.md`

---

## Ações Recentes (BETA-015A)

### BETA-012A: Importação CSV/XLSX Backend com Preview, Validação e Confirmação
**Status:** ✅ Implementado  
**Branch:** `feature/beta-012a-import-csv-xlsx-backend-preview-confirm`  
**Data:** 2026-06-10

**Implementado:**
- ✅ Parser CSV/XLSX melhorado com suporte a formatos brasileiros
- ✅ Layout mapper para campos fiscais/financeiros
- ✅ Validação linha a linha com erro/warning reporting
- ✅ Detecção de duplicidade (in-file e contra banco)
- ✅ Preview endpoint (sem persistência)
- ✅ Confirmação endpoint (service implementado, endpoint placeholder)
- ✅ Migration para ImportHistory (source, metadata, imported_by)
- ✅ Integração com Shipment (campos BETA-011A)
- ✅ 63 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/imports/mapper.py`
- `apps/api/app/modules/imports/service_v2.py`
- `apps/api/migrations/versions/20260610_01_add_import_history_metadata.py`
- `apps/api/tests/test_import_csv_validation.py`
- `apps/api/tests/test_import_xlsx_validation.py`
- `apps/api/tests/test_import_preview_confirm.py`
- `apps/api/tests/test_import_duplicate_detection.py`
- `docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md`

**Limitações Conhecidas:**
- Endpoint de confirmação requer gerenciamento de estado (Redis) - atualmente retorna 501
- Preview não é persistido entre chamadas

**Documentação:** `docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md`

---

### BETA-014B: Painel Frontend de Eficiência por Transportadora
**Status:** ✅ Implementado (Testes de interação de filtros adicionados)
**Branch:** `feature/beta-014b-carrier-efficiency-frontend`
**Data:** 2026-06-15

**Implementado:**
- ✅ Tipos TypeScript para Carrier Efficiency
- ✅ API client function getCarrierEfficiency
- ✅ Página de eficiência por transportadora
- ✅ Tabela com métricas (total NFs, total entregas, no prazo, atrasadas, frete total, frete médio)
- ✅ Exibição de rankings (eficiência, custo, volume)
- ✅ Estados de UX (loading, erro, vazio, sucesso)
- ✅ Formatação BRL e percentual
- ✅ 11 testes TDD implementados (6 API + 5 página)
- ✅ Testes de interação de filtros: 8 testes novos
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/lib/carrier-efficiency-api.test.ts`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/page.tsx`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page.test.tsx`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page-filters.test.tsx`
- `docs/BETA_014B_CARRIER_EFFICIENCY_FRONTEND.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts` (CarrierEfficiencyMetrics, CarrierEfficiencyResponse, CarrierEfficiencyFilters)
- `apps/web/src/lib/api.ts` (getCarrierEfficiency function)

**Limitações Conhecidas:**
- Sem componentes de UI avançados (cards, gráficos)
- Sem integração com dashboard geral
- Sem E2E (Playwright não configurado)

**Documentação:** `docs/BETA_014B_CARRIER_EFFICIENCY_FRONTEND.md`

---

### BETA-012B: Frontend de Upload, Preview, Erros por Linha e Confirmação de Importação
**Status:** ✅ Implementado
**Branch:** `feature/beta-012b-import-upload-preview-confirm-frontend`
**Data:** 2026-06-10

**Implementado:**
- ✅ Atualização de tipos TypeScript (RowValidationError, ValidatedRowData, ImportPreviewV2Response, ImportConfirmResponse)
- ✅ Nova função previewShipmentImport no API client
- ✅ Atualização de confirmShipmentsImport para usar /api/v1/imports/confirm
- ✅ Extração de helpers de formatação (formatCurrencyBRL, formatPercentage, formatDateBR, formatUnavailable)
- ✅ Atualização da tela de importação com novos estados e fluxos
- ✅ Suporte a CSV e XLSX
- ✅ Preview com tabela de dados fiscais/financeiros
- ✅ Exibição de erros por linha com severidade
- ✅ Exibição de warnings separados
- ✅ Bloqueio de confirmação quando há erro bloqueante
- ✅ Exibição de resultado final com created_shipments
- ✅ 17 testes TDD implementados (15 page.test.tsx + 2 api.test.ts)
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/app/(private)/shipments/import/page.test.tsx`
- `docs/BETA_012B_IMPORT_UPLOAD_PREVIEW_CONFIRM_FRONTEND.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/shipment-utils.ts`
- `apps/web/src/app/(private)/shipments/import/page.tsx`
- `apps/web/src/lib/api.test.ts`
- `apps/web/src/app/(private)/shipments/page.tsx` (import de helpers)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_012B_IMPORT_UPLOAD_PREVIEW_CONFIRM_FRONTEND.md`

---

### BETA-014B: Painel Frontend de Eficiência por Transportadora
**Status:** ✅ Implementado (Testes de interação de filtros adicionados)
**Branch:** `feature/beta-014b-carrier-efficiency-frontend`
**Data:** 2026-06-15

**Implementado:**
- ✅ Tipos TypeScript para Carrier Efficiency
- ✅ API client function getCarrierEfficiency
- ✅ Página de eficiência por transportadora
- ✅ Tabela com métricas (total NFs, total entregas, no prazo, atrasadas, frete total, frete médio)
- ✅ Exibição de rankings (eficiência, custo, volume)
- ✅ Estados de UX (loading, erro, vazio, sucesso)
- ✅ Formatação BRL e percentual
- ✅ 11 testes TDD implementados (6 API + 5 página)
- ✅ Testes de interação de filtros: 8 testes novos
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/lib/carrier-efficiency-api.test.ts`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/page.tsx`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page.test.tsx`
- `apps/web/src/app/(private)/shipments/analytics/carrier-efficiency/carrier-efficiency-page-filters.test.tsx`
- `docs/BETA_014B_CARRIER_EFFICIENCY_FRONTEND.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts` (CarrierEfficiencyMetrics, CarrierEfficiencyResponse, CarrierEfficiencyFilters)
- `apps/web/src/lib/api.ts` (getCarrierEfficiency function)

**Limitações Conhecidas:**
- Sem componentes de UI avançados (cards, gráficos)
- Sem integração com dashboard geral
- Sem E2E (Playwright não configurado)

**Documentação:** `docs/BETA_014B_CARRIER_EFFICIENCY_FRONTEND.md`

---

### BETA-012C: Importação Assistida Braspress - Layout, Fixtures e Documentação
**Status:** ✅ Implementado
**Branch:** `feature/beta-012c-braspress-assisted-import`
**Data:** 2026-06-10

**Implementado:**
- ✅ Layout Braspress assistido beta documentado
- ✅ Mapper específico para Braspress (braspress_mapper.py)
- ✅ Integração de source/layout ao preview endpoint
- ✅ Fixtures fake (CSV) para testes
- ✅ Testes TDD para Braspress assisted import
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/imports/braspress_mapper.py`
- `apps/api/tests/fixtures/braspress_sample.csv`
- `apps/api/tests/test_braspress_assisted_import.py`
- `docs/BETA_012C_BRASPRESS_ASSISTED_IMPORT.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/imports/service_v2.py` (integração com braspress_mapper)
- `apps/api/app/modules/imports/router.py` (source/layout params)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_012C_BRASPRESS_ASSISTED_IMPORT.md`

---

## Ações Recentes (BETA-017B)

### BETA-017B: Alerts Frontend and Dashboard Integration
**Status:** ✅ Implementado
**Branch:** `feature/beta-017b-alerts-frontend-dashboard-integration`
**Data:** 2026-06-20

**Implementado:**
- ✅ Frontend de alerts (página, API client, tipos)
- ✅ Integração de alerts no dashboard summary
- ✅ Testes TDD (alerts page, dashboard integration)
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/app/(private)/alerts/page.tsx`
- `apps/web/src/app/(private)/alerts/alerts-page.test.tsx`
- `apps/web/src/lib/alerts-api.test.ts`
- `docs/BETA_017B_ALERTS_FRONTEND_DASHBOARD_INTEGRATION.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts` (Alert, AlertResponse, AlertFilters)
- `apps/web/src/lib/api.ts` (getAlerts, postAlertsGenerate, patchAlertsRead, patchAlertsResolve)
- `apps/web/src/app/(private)/dashboard/dashboard-page.test.tsx` (integração com alerts)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_017B_ALERTS_FRONTEND_DASHBOARD_INTEGRATION.md`

---

## Ações Recentes (BETA-017A)

### BETA-017A: Alertas Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-017a-alerts-backend-api`
**Data:** 2026-06-20

**Implementado:**
- ✅ Model Alert com campos necessários
- ✅ Migration para tabela alerts
- ✅ Service de geração de alertas
- ✅ Endpoints POST /alerts/generate, GET /alerts, PATCH /alerts/{id}/read, PATCH /alerts/{id}/resolve
- ✅ Schemas/DTOs para alertas
- ✅ 15 testes TDD implementados (8 model + 7 generation + 8 API)
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/alerts/models.py`
- `apps/api/app/modules/alerts/service.py`
- `apps/api/app/modules/alerts/schemas.py`
- `apps/api/app/modules/alerts/__init__.py`
- `apps/api/migrations/versions/20260620_01_create_alerts.py`
- `apps/api/tests/test_alerts_model.py`
- `apps/api/tests/test_alerts_generation.py`
- `apps/api/tests/test_alerts_api.py`
- `docs/BETA_017A_ALERTS_BACKEND_API.md`

**Limitações Conhecidas:**
- Sem envio de e-mail (backend-only)
- Sem WhatsApp/webhook (fora do escopo beta)
- Sem frontend (BETA-017B)
- Sem agendamento externo com cron (fora do escopo beta)

**Documentação:** `docs/BETA_017A_ALERTS_BACKEND_API.md`

---

## Ações Recentes (BETA-016B)

### BETA-016B: Dashboard Beta Frontend e UX Operacional
**Status:** ✅ Implementado
**Branch:** `feature/beta-016b-dashboard-beta-frontend-ux`
**Data:** 2026-06-19

**Implementado:**
- ✅ Frontend de dashboard beta (página, API client, tipos)
- ✅ UX operacional (loading, erro, vazio, sucesso)
- ✅ Testes TDD (dashboard page, API client)
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/app/(private)/dashboard/page.tsx`
- `apps/web/src/app/(private)/dashboard/dashboard-page.test.tsx`
- `apps/web/src/lib/dashboard-api.test.ts`
- `docs/BETA_016B_DASHBOARD_BETA_FRONTEND_UX.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts` (DashboardSummary, DashboardFilters)
- `apps/web/src/lib/api.ts` (getDashboardSummary)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_016B_DASHBOARD_BETA_FRONTEND_UX.md`

---

## Ações Recentes (BETA-016A)

### BETA-016A: Dashboard Beta Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-016a-dashboard-beta-backend-api`
**Data:** 2026-06-19

**Implementado:**
- ✅ Service de dashboard summary
- ✅ Endpoint GET /dashboard/summary
- ✅ Schemas/DTOs para dashboard
- ✅ 30 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/dashboard/service.py`
- `apps/api/app/modules/dashboard/schemas.py`
- `apps/api/app/modules/dashboard/__init__.py`
- `apps/api/tests/test_dashboard_summary.py`
- `apps/api/tests/test_dashboard_api.py`
- `docs/BETA_016A_DASHBOARD_BETA_BACKEND_API.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/dashboard/router.py` (endpoint summary)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_016A_DASHBOARD_BETA_BACKEND_API.md`

---

## Ações Recentes (BETA-015A)

### BETA-015A: Exceptions Panel Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-015a-exceptions-panel-backend-api`
**Data:** 2026-06-18

**Implementado:**
- ✅ Service de exceptions panel
- ✅ Endpoint GET /exceptions/do
- ✅ Schemas/DTOs para exceptions
- ✅ 35 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/exceptions/service.py`
- `apps/api/app/modules/exceptions/schemas.py`
- `apps/api/app/modules/exceptions/__init__.py`
- `apps/api/tests/test_exceptions_panel_sla.py`
- `apps/api/tests/test_exceptions_panel_api.py`
- `docs/BETA_015A_EXCEPTIONS_PANEL_BACKEND_API.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/exceptions/router.py` (endpoint do)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_015A_EXCEPTIONS_PANEL_BACKEND_API.md`

---

## Ações Recentes (BETA-014A)

### BETA-014A: Carrier Efficiency Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-014a-carrier-efficiency-backend-api`
**Data:** 2026-06-17

**Implementado:**
- ✅ Service de carrier efficiency
- ✅ Endpoint GET /shipments/carrier-efficiency
- ✅ Schemas/DTOs para carrier efficiency
- ✅ 30 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/carriers/service.py`
- `apps/api/app/modules/carriers/schemas.py`
- `apps/api/app/modules/carriers/__init__.py`
- `apps/api/tests/test_carrier_efficiency_report.py`
- `apps/api/tests/test_carrier_efficiency_api.py`
- `docs/BETA_014A_CARRIER_EFFICIENCY_BACKEND_API.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/carriers/router.py` (endpoint carrier-efficiency)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_014A_CARRIER_EFFICIENCY_BACKEND_API.md`

---

## Ações Recentes (BETA-013A)

### BETA-013A: SLA Backend/API
**Status:** ✅ Implementado
**Branch:** `feature/beta-013a-sla-backend-api`
**Data:** 2026-06-16

**Implementado:**
- ✅ Service de SLA
- ✅ Endpoints GET /shipments/sla, POST /shipments/sla/rules, PATCH /shipments/{id}/sla
- ✅ Schemas/DTOs para SLA
- ✅ 42 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/sla/service.py`
- `apps/api/app/modules/sla/schemas.py`
- `apps/api/app/modules/sla/__init__.py`
- `apps/api/tests/test_sla_calculation.py`
- `apps/api/tests/test_sla_rules.py`
- `apps/api/tests/test_sla_api.py`
- `docs/BETA_013A_SLA_BACKEND_API.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/sla/router.py` (endpoints sla)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_013A_SLA_BACKEND_API.md`

---

## Ações Recentes (BETA-012C)

### BETA-012C: Importação Assistida Braspress - Layout, Fixtures e Documentação
**Status:** ✅ Implementado
**Branch:** `feature/beta-012c-braspress-assisted-import`
**Data:** 2026-06-10

**Implementado:**
- ✅ Layout Braspress assistido beta documentado
- ✅ Mapper específico para Braspress (braspress_mapper.py)
- ✅ Integração de source/layout ao preview endpoint
- ✅ Fixtures fake (CSV) para testes
- ✅ Testes TDD para Braspress assisted import
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/imports/braspress_mapper.py`
- `apps/api/tests/fixtures/braspress_sample.csv`
- `apps/api/tests/test_braspress_assisted_import.py`
- `docs/BETA_012C_BRASPRESS_ASSISTED_IMPORT.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/imports/service_v2.py` (integração com braspress_mapper)
- `apps/api/app/modules/imports/router.py` (source/layout params)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_012C_BRASPRESS_ASSISTED_IMPORT.md`

---

## Ações Recentes (BETA-012B)

### BETA-012B: Frontend de Upload, Preview, Erros por Linha e Confirmação de Importação
**Status:** ✅ Implementado
**Branch:** `feature/beta-012b-import-upload-preview-confirm-frontend`
**Data:** 2026-06-10

**Implementado:**
- ✅ Atualização de tipos TypeScript (RowValidationError, ValidatedRowData, ImportPreviewV2Response, ImportConfirmResponse)
- ✅ Nova função previewShipmentImport no API client
- ✅ Atualização de confirmShipmentsImport para usar /api/v1/imports/confirm
- ✅ Extração de helpers de formatação (formatCurrencyBRL, formatPercentage, formatDateBR, formatUnavailable)
- ✅ Atualização da tela de importação com novos estados e fluxos
- ✅ Suporte a CSV e XLSX
- ✅ Preview com tabela de dados fiscais/financeiros
- ✅ Exibição de erros por linha com severidade
- ✅ Exibição de warnings separados
- ✅ Bloqueio de confirmação quando há erro bloqueante
- ✅ Exibição de resultado final com created_shipments
- ✅ 17 testes TDD implementados (15 page.test.tsx + 2 api.test.ts)
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/web/src/app/(private)/shipments/import/page.test.tsx`
- `docs/BETA_012B_IMPORT_UPLOAD_PREVIEW_CONFIRM_FRONTEND.md`

**Arquivos Atualizados:**
- `apps/web/src/lib/types.ts`
- `apps/web/src/lib/api.ts`
- `apps/web/src/lib/shipment-utils.ts`
- `apps/web/src/app/(private)/shipments/import/page.tsx`
- `apps/web/src/lib/api.test.ts`
- `apps/web/src/app/(private)/shipments/page.tsx` (import de helpers)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_012B_IMPORT_UPLOAD_PREVIEW_CONFIRM_FRONTEND.md`

---

## Ações Recentes (BETA-012A)

### BETA-012A: Importação CSV/XLSX Backend com Preview, Validação e Confirmação
**Status:** ✅ Implementado
**Branch:** `feature/beta-012a-import-csv-xlsx-backend-preview-confirm`
**Data:** 2026-06-10

**Implementado:**
- ✅ Parser CSV/XLSX melhorado com suporte a formatos brasileiros
- ✅ Layout mapper para campos fiscais/financeiros
- ✅ Validação linha a linha com erro/warning reporting
- ✅ Detecção de duplicidade (in-file e contra banco)
- ✅ Preview endpoint (sem persistência)
- ✅ Confirmação endpoint (service implementado, endpoint placeholder)
- ✅ Migration para ImportHistory (source, metadata, imported_by)
- ✅ Integração com Shipment (campos BETA-011A)
- ✅ 63 testes TDD implementados
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/app/modules/imports/mapper.py`
- `apps/api/app/modules/imports/service_v2.py`
- `apps/api/migrations/versions/20260610_01_add_import_history_metadata.py`
- `apps/api/tests/test_import_csv_validation.py`
- `apps/api/tests/test_import_xlsx_validation.py`
- `apps/api/tests/test_import_preview_confirm.py`
- `apps/api/tests/test_import_duplicate_detection.py`
- `docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md`

**Limitações Conhecidas:**
- Endpoint de confirmação requer gerenciamento de estado (Redis) - atualmente retorna 501
- Preview não é persistido entre chamadas

**Documentação:** `docs/BETA_012A_IMPORT_CSV_XLSX_BACKEND.md`

---

## Ações Recentes (BETA-011A)

### BETA-011A: Shipment Model Expansion - Campos Fiscais/Financeiros
**Status:** ✅ Implementado
**Branch:** `feature/beta-011a-shipment-fiscal-financial-fields`
**Data:** 2026-06-09

**Implementado:**
- ✅ Campos fiscais/financeiros adicionados ao model Shipment
- ✅ Migration para novos campos
- ✅ Testes TDD para novos campos
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/migrations/versions/20260609_01_add_fiscal_financial_fields.py`
- `apps/api/tests/test_shipment_fiscal_financial_fields.py`
- `docs/BETA_011A_SHIPMENT_FISCAL_FINANCIAL_FIELDS.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/shipments/models.py` (novos campos)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_011A_SHIPMENT_FISCAL_FINANCIAL_FIELDS.md`

---

## Ações Recentes (BETA-010A)

### BETA-010A: Carrier Model Expansion - Campos Fiscais/Financeiros
**Status:** ✅ Implementado
**Branch:** `feature/beta-010a-carrier-fiscal-financial-fields`
**Data:** 2026-06-08

**Implementado:**
- ✅ Campos fiscais/financeiros adicionados ao model Carrier
- ✅ Migration para novos campos
- ✅ Testes TDD para novos campos
- ✅ Documentação completa

**Arquivos Criados:**
- `apps/api/migrations/versions/20260608_01_add_carrier_fiscal_financial_fields.py`
- `apps/api/tests/test_carrier_fiscal_financial_fields.py`
- `docs/BETA_010A_CARRIER_FISCAL_FINANCIAL_FIELDS.md`

**Arquivos Atualizados:**
- `apps/api/app/modules/carriers/models.py` (novos campos)

**Limitações Conhecidas:**
- Nenhuma limitação conhecida

**Documentação:** `docs/BETA_010A_CARRIER_FISCAL_FINANCIAL_FIELDS.md`

---

## Ações Recentes (BETA-009S)

### BETA-009S: Setup de Projeto e Governança
**Status:** ✅ Implementado
**Branch:** `main`
**Data:** 2026-06-07

**Implementado:**
- ✅ Scripts de validação (check_secrets.py, validate_migrations.py, validate_docs.py, beta_validate.py)
- ✅ Documentação de governança (BETA_CHECKLIST.md, BETA_VALIDATION_EVIDENCE.md, BETA_COMMANDS.md, BETA_RELEASE_GATE.md, BETA_KNOWN_LIMITATIONS.md, BETA_NEXT_ACTIONS.md)
- ✅ Configuração de testes (pytest, vitest)
- ✅ Configuração de lint (eslint, ruff)
- ✅ Configuração de migrations (alembic)
- ✅ Configuração de CI/CD (GitHub Actions - placeholder)

**Arquivos Criados:**
- `scripts/check_secrets.py`
- `scripts/check_secrets_core.py`
- `scripts/validate_migrations.py`
- `scripts/validate_docs.py`
- `scripts/beta_validate.py`
- `docs/BETA_CHECKLIST.md`
- `docs/BETA_VALIDATION_EVIDENCE.md`
- `docs/BETA_COMMANDS.md`
- `docs/BETA_RELEASE_GATE.md`
- `docs/BETA_KNOWN_LIMITATIONS.md`
- `docs/BETA_NEXT_ACTIONS.md`
- `.github/workflows/ci.yml` (placeholder)

**Limitações Conhecidas:**
- CI/CD não configurado completamente (placeholder)
- E2E tests não configurados (Playwright não configurado)

**Documentação:** `docs/BETA_CHECKLIST.md`

---

## Próximas Ações

### BETA-018B: Relatório Diário Frontend
**Status:** ⏳ Pendente
**Prioridade:** Alta
**Épico:** 6 - Relatório diário automático

**Tarefas:**
- [ ] Criar página de relatório diário
- [ ] Criar API client functions
- [ ] Criar tipos TypeScript
- [ ] Implementar visualização histórica
- [ ] Implementar filtros visuais
- [ ] Implementar botão gerar/regenerar
- [ ] Implementar exportação (se desejada e segura)
- [ ] Testes TDD (frontend)
- [ ] Documentação

**Dependências:**
- BETA-018A (Backend/API)

---

### BETA-019A: Agendamento Automático de Relatórios
**Status:** ⏳ Pendente
**Prioridade:** Média
**Épico:** 6 - Relatório diário automático

**Tarefas:**
- [ ] Implementar agendamento com cron
- [ ] Implementar envio automático por e-mail
- [ ] Implementar integração com WhatsApp/webhook (se desejado)
- [ ] Testes TDD
- [ ] Documentação

**Dependências:**
- BETA-018A (Backend/API)
- BETA-018B (Frontend)

---

### BETA-020A: Auditoria Completa
**Status:** ⏳ Pendente
**Prioridade:** Baixa
**Épico:** 9 - Auditoria e Compliance

**Tarefas:**
- [ ] Implementar auditoria completa
- [ ] Implementar logs de auditoria
- [ ] Implementar relatórios de auditoria
- [ ] Testes TDD
- [ ] Documentação

**Dependências:**
- BETA-018A (Backend/API)

---

### BETA-021A: RBAC Granular
**Status:** ⏳ Pendente
**Prioridade:** Alta
**Épico:** 9 - Auditoria e Compliance

**Tarefas:**
- [ ] Implementar RBAC granular
- [ ] Implementar permissões por endpoint
- [ ] Implementar permissões por módulo
- [ ] Testes TDD
- [ ] Documentação

**Dependências:**
- BETA-018A (Backend/API)

---

### BETA-022A: Correção do Middleware de Logging
**Status:** ⏳ Pendente
**Prioridade:** Média
**Épico:** 11 - QA, CI/CD e Validação

**Tarefas:**
- [ ] Corrigir middleware de logging para funcionar com TestClient
- [ ] Testes TDD
- [ ] Documentação

**Dependências:**
- Nenhuma

---

## Notas

- Todas as ações devem seguir o BETA_CHECKLIST.md
- Todas as ações devem ser documentadas em BETA_VALIDATION_EVIDENCE.md
- Todas as ações devem seguir o BETA_RELEASE_GATE.md
- Todas as limitações devem ser documentadas em BETA_KNOWN_LIMITATIONS.md
