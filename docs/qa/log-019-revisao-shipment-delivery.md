# LOG-019 — Revisão Arquitetural Shipment vs Delivery

## Data/Hora
2026-06-05

## Branch
feature/revisao-shipment-delivery

## Branch Base
feature/relatorio-diario

## Commit Base
3f62e0e (docs(qa): registra status runtime Docker e atualizacoes de PR)

## Validação de Ambiente
- **Python**: 3.11.9
- **venv**: Recriado com sucesso
- **pytest**: 9.0.3
- **ruff**: 0.15.15
- **Backend pytest**: 105 passed, 1 warning
- **Backend ruff**: All checks passed
- **Frontend npm run lint**: Passou
- **Frontend npm run test**: 58 passed
- **Frontend npm run build**: Sucesso

## Resumo Executivo
O LOG-019 identificou uma duplicidade conceitual entre duas entidades no sistema: **Delivery** (módulo imports) e **Shipment** (módulo shipments). Ambas representam "entregas" no domínio, mas com escopos, responsabilidades e ciclos de vida diferentes. Não há conexão técnica documentada entre elas, o que cria riscos operacionais e de UX.

## Entidades Analisadas

### Delivery (imports)
- **Módulo**: app/modules/imports
- **Tabela**: deliveries
- **Propósito**: Dado bruto importado via CSV/Excel
- **Ciclo de vida**: Importação → Persistência → Listagem/Detalhe (sem evolução)

### Shipment (shipments)
- **Módulo**: app/modules/shipments
- **Tabela**: shipments
- **Propósito**: Entidade operacional com rastreabilidade completa
- **Ciclo de vida**: Importação/Manual → Operação → Exceções → Tratativas → Relatórios

## Matriz Delivery vs Shipment

| Aspecto | Delivery | Shipment |
|---------|----------|----------|
| **Módulo** | imports | shipments |
| **Tabela** | deliveries | shipments |
| **Campos principais** | nf, transportadora, data_coleta, valor_frete, percentual_frete | tracking_code, carrier_id, status, estimated_delivery, actual_delivery, recipient_name, recipient_phone, origin_address, destination_address, invoice_number, invoice_key, fiscal_document, amount, due_date, delay_days, criticality |
| **Endpoints** | POST /imports/upload, GET /imports/history, GET /imports/deliveries, GET /imports/deliveries/{id} | GET /shipments, GET /shipments/exceptions, POST /shipments/upload, POST /shipments/import, GET /shipments/{id}, GET /shipments/{id}/treatments, POST /shipments/{id}/treatments |
| **Telas frontend** | /shipments/deliveries, /shipments/deliveries/{id} | /shipments, /shipments/{id}, /exceptions, /reports/daily |
| **Tipos TypeScript** | DeliveryListItem, DeliveryDetail | Shipment, ShipmentListItem, ShipmentDetail |
| **Testes** | test_imports.py | test_exceptions.py, test_shipment_detail_treatments_report_users.py |
| **Responsabilidades** | Importação de dados brutos | Operação logística completa |
| **Relação com importação** | Persiste dados brutos do CSV/Excel | Tem fluxo próprio de importação (upload/confirm) |
| **Relação com exceções** | ❌ Não aplicável | ✅ Painel de exceções (/shipments/exceptions) |
| **Relação com tratativas** | ❌ Não aplicável | ✅ Tratativas por shipment (/shipments/{id}/treatments) |
| **Relação com relatório diário** | ❌ Não aplicável | ✅ Relatório diário (/reports/daily) |
| **Riscos** | Dados isolados, sem rastreabilidade operacional | Duplicidade conceitual com Delivery |

## Endpoints/Telas por Entidade

### Delivery
**Endpoints Backend:**
- POST /imports/upload
- GET /imports/history
- GET /imports/deliveries
- GET /imports/deliveries/{delivery_id}

**Funções API Client:**
- listDeliveries(token, params)
- getDeliveryDetail(token, deliveryId)

**Telas Frontend:**
- /shipments/deliveries (listagem de entregas importadas)
- /shipments/deliveries/{id} (detalhe da entrega)

**Tipos TypeScript:**
- DeliveryListItem
- DeliveryDetail
- DeliveryListParams
- DeliveryListResponse

**Testes:**
- test_imports.py

### Shipment
**Endpoints Backend:**
- GET /shipments
- GET /shipments/exceptions
- POST /shipments/upload
- POST /shipments/import
- GET /shipments/{shipment_id}
- GET /shipments/{shipment_id}/treatments
- POST /shipments/{shipment_id}/treatments

**Funções API Client:**
- listShipments(token, params)
- listExceptionShipments(token, params)
- uploadShipmentsCsv(token, file)
- confirmShipmentsImport(token, importId)
- getShipmentDetail(token, shipmentId)
- listShipmentTreatments(token, shipmentId)
- createShipmentTreatment(token, shipmentId, payload)

**Telas Frontend:**
- /shipments (listagem de shipments)
- /shipments/{id} (detalhe do shipment)
- /exceptions (painel de exceções)
- /reports/daily (relatório diário)

**Tipos TypeScript:**
- Shipment
- ShipmentListItem
- ShipmentDetail
- ShipmentListParams
- ShipmentListResponse
- ShipmentTreatment
- CreateShipmentTreatmentRequest

**Testes:**
- test_exceptions.py
- test_shipment_detail_treatments_report_users.py

## Lacunas Encontradas

### Relacionamento Técnico
- ❌ **FK Delivery → Shipment**: Não existe
- ❌ **FK Shipment → Delivery**: Não existe
- ❌ **Conversão automática**: Não existe
- ❌ **Fluxo de promoção**: Não existe

### Importação
- ❌ **Importador cria Shipment**: Não (importador cria Delivery)
- ✅ **Importador cria Delivery**: Sim (persist_deliveries em imports/service.py)
- ⚠️ **Shipments tem fluxo próprio**: Sim (upload/confirm em shipments/router.py)

### Relatórios
- ❌ **Relatórios consideram Delivery**: Não
- ✅ **Relatórios consideram Shipment**: Sim (/reports/daily)

### Exceções
- ❌ **Exceções consideram Delivery**: Não
- ✅ **Exceções consideram Shipment**: Sim (/shipments/exceptions)

### Tratativas
- ❌ **Tratativas podem ser aplicadas a Delivery**: Não
- ✅ **Tratativas podem ser aplicadas a Shipment**: Sim (/shipments/{id}/treatments)

### Duplicidade
- ⚠️ **Duplicação entre /shipments/deliveries e /shipments**: Sim (duas listagens de "entregas")
- ⚠️ **Risco de dois conceitos de "entrega" para o usuário**: Sim (confusão UX)

## Riscos Principais

### 1. Confusão de UX
- Usuário pode não entender a diferença entre /shipments/deliveries e /shipments
- Ambas telas mostram "entregas", mas com dados diferentes
- Risco de erro operacional ao usar a tela errada

### 2. Isolamento de Dados
- Dados importados via CSV/Excel ficam isolados em Delivery
- Não fluem para o ciclo operacional (exceções, tratativas, relatórios)
- Perda de rastreabilidade

### 3. Duplicidade de Importação
- Dois fluxos de importação diferentes:
  - imports/upload → persist_deliveries (cria Delivery)
  - shipments/upload → process_import (cria Shipment)
- Risco de inconsistência de dados

### 4. Falta de Fonte de Verdade
- Não há entidade única que representa "entrega operacional"
- Ambas Delivery e Shipment podem ser consideradas "entrega"
- Dificulta decisões de arquitetura para próximos LOGs

### 5. Manutenção Futura
- Qual entidade deve ser usada para novos features?
- Qual entidade deve ser exposta em APIs externas?
- Qual entidade deve ser usada em relatórios customizados?

## Opções Arquiteturais

### Opção A — Manter Delivery e Shipment Separados
**Descrição:**
- Delivery = dado bruto/importado (staging/auditoria)
- Shipment = entidade operacional (fonte de verdade)

**Benefícios:**
- Separação clara de responsabilidades
- Delivery como auditoria de importação
- Shipment como entidade operacional consolidada

**Riscos:**
- Requer documentação clara
- Pode criar confusão UX se não explicado
- Futuro fluxo de "promoção" Delivery → Shipment não definido

**Impacto:**
- Baixo (nenhuma alteração de código)
- Documentação e governança necessárias

### Opção B — Importador Criar Shipment Diretamente
**Descrição:**
- Alterar importador para criar Shipment em vez de Delivery
- Remover ou descontinuar Delivery

**Benefícios:**
- Elimina duplicidade
- Simplifica arquitetura
- Fonte de verdade única

**Riscos:**
- Exige alteração em persistência, testes e talvez migration
- Pode quebrar relatórios existentes
- Perda de auditoria de importação bruta

**Impacto:**
- Alto (alteração significativa de código)
- Requer testes completos
- Requer migration

### Opção C — Criar Vínculo Delivery → Shipment
**Descrição:**
- Adicionar FK delivery_id em Shipment
- Criar fluxo de "promoção" Delivery → Shipment
- Manter ambos com relação clara

**Benefícios:**
- Mantém rastreabilidade completa
- Permite fluxo de aprovação/conversão
- Auditoria de importação preservada

**Riscos:**
- Existe FK/migration
- Complexidade adicional no fluxo
- Efeitos em relatórios e exceções

**Impacto:**
- Médio (alteração moderada de código)
- Requer migration
- Requer testes de integração

### Opção D — Unificar Listagens em Shipment
**Descrição:**
- Migrar telas /shipments/deliveries para /shipments
- Manter Delivery apenas como staging/import audit
- Simplificar UX

**Benefícios:**
- Simplifica UX (única listagem de entregas)
- Reduz confusão do usuário
- Mantém auditoria de importação

**Riscos:**
- Exige migração de telas e endpoints
- Pode quebrar fluxos existentes
- Compatibilidade com usuários acostumados com /shipments/deliveries

**Impacto:**
- Médio (alteração de frontend e backend)
- Requer testes de UX
- Requer documentação de migração

## Recomendação Técnica

### Recomendação Conservadora
**Não alterar código agora.**

**Definição de papéis:**
- **Delivery**: Staging/auditoria de importação (dado bruto)
- **Shipment**: Entidade operacional (fonte de verdade)

**Ações imediatas:**
1. Documentar claramente a diferença entre Delivery e Shipment
2. Adicionar aviso nas telas /shipments/deliveries explicando que são dados brutos
3. Evitar novas features sobre Delivery até decisão do supervisor

**Ações futuras (se aprovado):**
1. Criar LOG técnico para "promoção Delivery → Shipment" ou vínculo Delivery/Shipment
2. Implementar Opção C (vínculo Delivery → Shipment) ou Opção D (unificar listagens)
3. Migration para adicionar FK delivery_id em Shipment
4. Testes de integração completos

**Justificativa:**
- Não há urgência operacional para alterar a arquitetura
- O sistema está funcionando com ambos os conceitos
- Alterações arquiteturais significativas exigem planejamento cuidadoso
- Risco de quebrar funcionalidades existentes

## Decisão Pendente de Rafael/Supervisor
- [ ] Aprovar definição de papéis (Delivery = staging, Shipment = operacional)
- [ ] Aprovar documentação adicional nas telas
- [ ] Decidir sobre implementação futura de vínculo/unificação
- [ ] Priorizar próxima etapa do roadmap

## Confirmação de Governança
- ✅ Nenhum código funcional foi alterado
- ✅ Nenhum backend foi alterado
- ✅ Nenhum frontend foi alterado
- ✅ Nenhum teste foi alterado
- ✅ Nenhuma migration foi criada
- ✅ Apenas documentação de discovery foi criada

## Próximo Passo
Aguardar decisão arquitetural de Rafael/supervisor para:
- Aprovar definição de papéis
- Autorizar implementação de vínculo/unificação
- Ou definir próxima etapa do roadmap
