# LOG-018 — Relatório Diário — Discovery Gate

## Data/Hora
2026-06-04

## Branch
- **Branch**: feature/relatorio-diario
- **Branch base**: feature/tratativas-excecoes
- **Commit base**: 96dea5d docs(qa): registra discovery gate de tratativas

## Dependência dos LOGs anteriores
- **LOG-016 Backend/API**: Validado como já existente (endpoint /api/v1/shipments/exceptions)
- **LOG-016 Web**: Validado como já existente (tela /exceptions)
- **LOG-017 Tratativas**: Validado como já existente (endpoints e frontend de tratativas)

## Arquitetura Encontrada

### Backend — Endpoint de Relatório Diário
- **Arquivo**: apps/api/app/modules/reports/router.py
- **Endpoint**: GET /reports/daily (linha 12-17)
- **Autenticação**: require_roles("admin", "logistica", "gestor", "auditoria")
- **Service**: build_daily_report (importado de app.modules.shipments.service)
- **Resposta**: dict (sem schema Pydantic específico)

### Backend — Service de Relatório Diário
- **Arquivo**: apps/api/app/modules/shipments/service.py
- **Função**: build_daily_report (linha 664-679)
- **Lógica**:
  - Consulta todos os Shipment do banco
  - Calcula total de shipments
  - Calcula total de exceções (delay_days > 0 OR criticality != "normal")
  - Agrupa por criticality (normal, baixa, media, alta)
  - Agrupa por carrier_id
  - Retorna data atual no formato ISO
- **Métricas retornadas**:
  - report_date: string (data atual)
  - total_shipments: int
  - total_exceptions: int
  - by_criticality: dict[str, int]
  - by_carrier: Array<{carrier_id: number, count: number}>

### Frontend — Página de Relatório Diário
- **Arquivo**: apps/web/src/app/(private)/reports/daily/page.tsx
- **Status**: ✅ Já implementada
- **Funcionalidades**:
  - Carrega relatório diário (getDailyReport)
  - Exibe métricas principais (total_shipments, total_exceptions, report_date)
  - Exibe distribuição por criticality
  - Exportação CSV (gerado no frontend)
  - Estados de UI (loading, erro, sucesso)
- **Exportação CSV**:
  - Gerado no frontend (não no backend)
  - Formato: metric,value
  - Campos: report_date, total_shipments, total_exceptions, criticality_*

### Frontend — API Client
- **Arquivo**: apps/web/src/lib/api.ts
- **Função**: getDailyReport (linha 187-191)
- **Endpoint**: /reports/daily
- **Tipo de retorno**: DailyReportResponse

### Frontend — Tipos
- **Arquivo**: apps/web/src/lib/types.ts
- **DailyReportResponse** (linha 118-124):
  - report_date: string
  - total_shipments: number
  - total_exceptions: number
  - by_criticality: Record<string, number>
  - by_carrier: Array<{carrier_id: number, count: number}>

### Testes Backend
- **Arquivo**: apps/api/tests/test_shipment_detail_treatments_report_users.py
- **Teste relatório diário**: test_w10_daily_report (linha 103-112)
  - Cria usuário com role "gestor"
  - Chama endpoint /reports/daily
  - Verifica se total_shipments >= 1
  - Verifica se by_criticality existe na resposta

## Respostas às Perguntas de Discovery

1. **Já existe endpoint de relatório diário?**
   ✅ Sim, GET /reports/daily em apps/api/app/modules/reports/router.py

2. **Já existe tela de relatório diário?**
   ✅ Sim, apps/web/src/app/(private)/reports/daily/page.tsx

3. **Quais métricas são exibidas?**
   ✅ total_shipments, total_exceptions, report_date, by_criticality

4. **A tela consome endpoint real ou dados mockados?**
   ✅ Consome endpoint real via getDailyReport

5. **Existe exportação CSV?**
   ✅ Sim, gerado no frontend (não no backend)

6. **Existem testes backend ou frontend?**
   ✅ Teste backend: test_w10_daily_report

7. **O relatório usa Shipment, Delivery ou ambos?**
   ✅ Usa apenas Shipment (não Delivery)

8. **Há risco de conceito misto entre imports/Delivery e shipments/Shipment?**
   ✅ Sim, há risco de conceito misto
   - Shipment (remessas): tracking_code, carrier_id, delay_days, criticality
   - Delivery (entregas fiscais): nf, transportadora, data_coleta, valor_frete, percentual_frete
   - O relatório diário está baseado em Shipment, não em Delivery
   - A cadeia LOG-007 a LOG-012 está baseada em Delivery
   - Não há conexão clara entre as duas cadeias

## Estratégia Escolhida

**Caso A — relatório diário já existe e está funcional**

**Justificativa:**
- Endpoint /reports/daily já existe
- Service build_daily_report já existe
- Frontend /reports/daily já existe
- Exportação CSV já existe (gerado no frontend)
- Teste backend já existe e passa
- Métricas já estão implementadas

**Ação:**
- Validar com testes existentes
- Validar frontend
- Documentar discovery
- Não alterar código funcional

**Observação importante:**
- O relatório diário está baseado em Shipment, não em Delivery
- A cadeia LOG-007 a LOG-012 está baseada em Delivery
- Não há conexão clara entre as duas cadeias
- Isso pode ser uma lacuna arquitetural a ser revisada no futuro

## Testes Red
**Não aplicável (Caso A)**

Como o relatório diário já existe e está funcional, não há necessidade de criar testes Red. A validação será feita com os testes existentes.

## Implementação Green
**Não aplicável (Caso A)**

Como o relatório diário já existe e está funcional, não há necessidade de implementar Green. A validação será feita com os testes existentes.

## Validação com Testes Existentes

### Backend
- **Comando**: pytest tests -k "report or daily or shipment" -v
- **Resultado**: ✅ Teste específico de relatório diário passando
- **Teste validado**:
  - test_w10_daily_report: PASSED

### Pytest Completo
- **Comando**: pytest --tb=short -q
- **Resultado**: ✅ 105 passed, 1 warning in 26.18s

### Ruff
- **Comando**: ruff check .
- **Resultado**: ✅ All checks passed!

### Frontend
- **npm run lint**: ✅ All checks passed
- **npm run test**: ✅ 58 passed (8 test files)
- **npm run build**: ✅ Compiled successfully (12 routes geradas)

## Checklist de Validação (Manual)
Como o projeto não permite teste de componente sem refatoração grande, foi criado checklist reprodutível:

1. **Endpoint de relatório diário existe**: ✅ GET /reports/daily
2. **Service de relatório diário existe**: ✅ build_daily_report
3. **Página de relatório diário existe**: ✅ /reports/daily
4. **API client existe**: ✅ getDailyReport
5. **Tipos corretos**: ✅ DailyReportResponse
6. **Métricas exibidas**: ✅ total_shipments, total_exceptions, report_date, by_criticality
7. **Exportação CSV existe**: ✅ Gerado no frontend
8. **Teste backend passa**: ✅ test_w10_daily_report
9. **Autenticação exigida**: ✅ require_roles
10. **Conceito misto**: ⚸️ Relatório baseado em Shipment, cadeia LOG-007 a LOG-012 baseada em Delivery

## Arquivos Inspecionados
- apps/api/app/modules/reports/router.py
- apps/api/app/modules/shipments/service.py
- apps/api/tests/test_shipment_detail_treatments_report_users.py
- apps/web/src/app/(private)/reports/daily/page.tsx
- apps/web/src/lib/api.ts
- apps/web/src/lib/types.ts

## Arquivos Alterados
- **Nenhum arquivo funcional alterado**
- Apenas documentação criada: docs/qa/log-018-relatorio-diario.md

## Comandos Executados
```bash
cd C:\Users\LENOVO\Ilex_Logistica
git checkout feature/tratativas-excecoes
git checkout -b feature/relatorio-diario
cd apps/api
pytest --tb=short -q  # 105 passed, 1 warning
ruff check .  # All checks passed!
cd ..\web
npm run lint  # All checks passed
npm run test  # 58 passed (8 test files)
npm run build  # Compiled successfully (12 routes geradas)
```

## Riscos
- **Risco de validação manual**: Smoke manual não foi executado por limitação de ambiente
- **Risco de conceito misto**: Relatório diário baseado em Shipment, cadeia LOG-007 a LOG-012 baseada em Delivery
- **Risco de lacuna arquitetural**: Não há conexão clara entre as duas cadeias (Shipment vs Delivery)

## Pendências
- Smoke manual não executado (limitação de ambiente)
- Revisão arquitetural da conexão entre Shipment e Delivery (futura)
- Integração entre as duas cadeias (futura, se o roadmap exigir)

## Limite Claro entre LOG-018 e Filtros Avançados da Fase 3
- **LOG-018**: Relatório diário (consolidação operacional) — ✅ Validado como já existente
- **Filtros avançados da Fase 3**: Não implementados (fora do escopo atual)

## Conclusão
✅ **LOG-018 validado como já existente**
- Endpoint /reports/daily já existe
- Service build_daily_report já existe
- Frontend /reports/daily já existe
- Exportação CSV já existe (gerado no frontend)
- Teste backend já existe e passa
- Métricas já estão implementadas
- Nenhuma alteração funcional necessária
- Nenhum código funcional foi alterado

**Observação arquitetural:**
- O relatório diário está baseado em Shipment, não em Delivery
- A cadeia LOG-007 a LOG-012 está baseada em Delivery
- Não há conexão clara entre as duas cadeias
- Isso pode ser uma lacuna arquitetural a ser revisada no futuro
