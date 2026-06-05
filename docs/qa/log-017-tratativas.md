# LOG-017 — Tratativas de Exceções/Entregas — Discovery Gate

## Data/Hora
2026-06-04

## Branch
- **Branch**: feature/tratativas-excecoes
- **Branch base**: feature/painel-excecoes-web
- **Commit base**: 8c60bb3 docs(qa): registra validacao web do painel de excecoes

## Dependência do LOG-016
- **LOG-016 Backend/API**: Validado como já existente (endpoint /api/v1/shipments/exceptions)
- **LOG-016 Web**: Validado como já existente (tela /exceptions)

## Arquitetura Encontrada

### Backend — Modelo de Tratativa
- **Arquivo**: apps/api/app/modules/shipments/models.py
- **Modelo**: ShipmentTreatment (linha 52-60)
- **Campos**:
  - id (Integer, primary key)
  - shipment_id (Integer, ForeignKey para shipments.id)
  - status (String, nullable=False)
  - comment (Text, nullable=False)
  - created_by (Integer, ForeignKey para users.id)
  - created_at (DateTime, nullable=False)
- **Associação**: Tratativa está associada a Shipment (não Delivery)

### Backend — Endpoints de Tratativa
- **Arquivo**: apps/api/app/modules/shipments/router.py
- **Endpoint listar tratativas**: GET /{shipment_id}/treatments (linha 147-153)
  - Autenticação: require_roles("admin", "logistica", "gestor", "auditoria")
  - Resposta: list[ShipmentTreatmentResponse]
- **Endpoint criar tratativa**: POST /{shipment_id}/treatments (linha 156-166)
  - Autenticação: require_roles("admin", "logistica", "gestor")
  - Payload: ShipmentTreatmentCreate (status, comment)
  - Resposta: ShipmentTreatmentResponse (status 201)

### Backend — Schemas de Tratativa
- **Arquivo**: apps/api/app/modules/shipments/schemas.py
- **ShipmentTreatmentCreate** (linha 108-110):
  - status: String (min_length=1, max_length=50)
  - comment: String (min_length=1)
- **ShipmentTreatmentResponse** (linha 113-119):
  - id: int
  - shipment_id: int
  - status: str
  - comment: str
  - created_by: int
  - created_at: datetime

### Backend — Testes de Tratativa
- **Arquivo**: apps/api/tests/test_shipment_detail_treatments_report_users.py
- **Teste criar e listar tratativas**: test_w11_create_and_list_treatments (linha 68-88)
  - Cria tratativa com status "em_tratativa" e comment
  - Lista tratativas e verifica se foi criada
- **Teste permissão de escrita**: test_w11_treatment_write_blocked_for_auditoria (linha 90-100)
  - Verifica que role "auditoria" não pode criar tratativa (403)

### Frontend — Página de Detalhe
- **Arquivo**: apps/web/src/app/(private)/shipments/[id]/page.tsx
- **Status**: ✅ Já implementada
- **Funcionalidades**:
  - Carrega detalhe do shipment (getShipmentDetail)
  - Carrega tratativas (listShipmentTreatments)
  - Exibe tratativas em lista
  - Formulário para criar tratativa (condicional por permissão)
  - Recarrega dados após criar tratativa
- **Permissões**: canEditShipments (baseado em role)
- **Campos do formulário**:
  - status: select (em_tratativa, resolvido, escalado)
  - comment: input text

### Frontend — API Client
- **Arquivo**: apps/web/src/lib/api.ts
- **Função listar tratativas**: listShipmentTreatments (linha 169-173)
  - Endpoint: /shipments/{shipmentId}/treatments
  - Tipo de retorno: ShipmentTreatment[]
- **Função criar tratativa**: createShipmentTreatment (linha 175-185)
  - Endpoint: /shipments/{shipmentId}/treatments
  - Payload: CreateShipmentTreatmentRequest
  - Tipo de retorno: ShipmentTreatment

### Frontend — Tipos
- **Arquivo**: apps/web/src/lib/types.ts
- **ShipmentTreatment** (linha 104-111):
  - id: number
  - shipment_id: number
  - status: string
  - comment: string
  - created_by: number
  - created_at: string
- **CreateShipmentTreatmentRequest** (linha 113-116):
  - status: string
  - comment: string

## Respostas às Perguntas de Discovery

1. **Já existe modelo de tratativa?**
   ✅ Sim, ShipmentTreatment em apps/api/app/modules/shipments/models.py

2. **Já existe endpoint para adicionar/listar tratativas?**
   ✅ Sim, GET /{shipment_id}/treatments e POST /{shipment_id}/treatments

3. **A página de detalhe já exibe timeline/tratativas?**
   ✅ Sim, apps/web/src/app/(private)/shipments/[id]/page.tsx exibe tratativas

4. **Existe formulário de nova tratativa?**
   ✅ Sim, formulário com status e comment (condicional por permissão)

5. **Quais testes já cobrem isso?**
   ✅ test_w11_create_and_list_treatments e test_w11_treatment_write_blocked_for_auditoria

6. **Tratativa está associada a Shipment ou Delivery?**
   ✅ Tratativa está associada a Shipment (não Delivery)

7. **Existe diferença entre Shipment e Delivery nesse contexto?**
   ✅ Sim, Shipment (remessas) e Delivery (entregas fiscais) são conceitos diferentes
   - Shipment: tracking_code, carrier_id, delay_days, criticality
   - Delivery: nf, transportadora, data_coleta, valor_frete, percentual_frete

## Estratégia Escolhida

**Caso A — tratativas já existem e estão funcionais**

**Justificativa:**
- Modelo ShipmentTreatment já existe
- Endpoints de tratativa já existem e funcionam
- Testes de tratativa já passam
- Frontend já exibe e cria tratativas
- Permissões já estão implementadas

**Ação:**
- Validar com testes existentes
- Rodar smoke/checklist
- Documentar discovery
- Não alterar código funcional

## Testes Red
**Não aplicável (Caso A)**

Como as tratativas já existem e estão funcionais, não há necessidade de criar testes Red. A validação será feita com os testes existentes.

## Implementação Green
**Não aplicável (Caso A)**

Como as tratativas já existem e estão funcionais, não há necessidade de implementar Green. A validação será feita com os testes existentes.

## Validação com Testes Existentes

### Backend
- **Comando**: pytest tests -k "treatment or tratativa or shipment" -v
- **Resultado**: ✅ Testes específicos de tratativa passando
- **Testes validados**:
  - test_w11_create_and_list_treatments: PASSED
  - test_w11_treatment_write_blocked_for_auditoria: PASSED

### Pytest Completo
- **Comando**: pytest --tb=short -q
- **Resultado**: ✅ 105 passed, 1 warning in 26.02s

### Ruff
- **Comando**: ruff check .
- **Resultado**: ✅ All checks passed!

### Frontend
- **npm run lint**: ✅ All checks passed
- **npm run test**: ✅ 58 passed (8 test files)
- **npm run build**: ✅ Compiled successfully (12 routes geradas)

## Checklist de Validação (Manual)
Como o projeto não permite teste de componente sem refatoração grande, foi criado checklist reprodutível:

1. **Modelo de tratativa existe**: ✅ ShipmentTreatment
2. **Endpoint listar tratativas existe**: ✅ GET /{shipment_id}/treatments
3. **Endpoint criar tratativa existe**: ✅ POST /{shipment_id}/treatments
4. **Página de detalhe exibe tratativas**: ✅ /shipments/[id]
5. **Formulário de nova tratativa existe**: ✅ Com status e comment
6. **Permissões implementadas**: ✅ require_roles
7. **Testes backend passam**: ✅ test_w11_create_and_list_treatments
8. **Autenticação exigida**: ✅ require_roles
9. **Associação correta**: ✅ Tratativa associada a Shipment
10. **Tipos corretos**: ✅ ShipmentTreatment e CreateShipmentTreatmentRequest

## Arquivos Inspecionados
- apps/api/app/modules/shipments/models.py
- apps/api/app/modules/shipments/router.py
- apps/api/app/modules/shipments/schemas.py
- apps/api/tests/test_shipment_detail_treatments_report_users.py
- apps/web/src/app/(private)/shipments/[id]/page.tsx
- apps/web/src/lib/api.ts
- apps/web/src/lib/types.ts

## Arquivos Alterados
- **Nenhum arquivo funcional alterado**
- Apenas documentação criada: docs/qa/log-017-tratativas.md

## Comandos Executados
```bash
cd C:\Users\LENOVO\Ilex_Logistica
git checkout feature/painel-excecoes-web
git checkout -b feature/tratativas-excecoes
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
- **Risco de conceito misto**: Shipment e Delivery são conceitos diferentes sem conexão clara

## Pendências
- Smoke manual não executado (limitação de ambiente)
- Integração entre Shipment e Delivery não está no escopo (conceitos diferentes)

## Limite Claro entre LOG-017 e LOG-018
- **LOG-017**: Tratativas (ação sobre exceções) — ✅ Validado como já existente
- **LOG-018**: Relatório diário (consolidação operacional) — Observação: Endpoint /reports/daily já existe

## Conclusão
✅ **LOG-017 validado como já existente**
- Modelo ShipmentTreatment já existe
- Endpoints de tratativa já existem e funcionam
- Testes de tratativa já passam
- Frontend já exibe e cria tratativas
- Permissões já estão implementadas
- Nenhuma alteração funcional necessária
- Nenhum código funcional foi alterado
