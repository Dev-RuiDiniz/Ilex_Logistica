# LOG-020 — Especificação Técnica do Vínculo/Promoção Delivery → Shipment

## Data/Hora
2026-06-05

## Branch
feature/especificacao-delivery-shipment

## Branch Base
feature/revisao-shipment-delivery

## Commit Base
a17de8e (docs(qa): registra revisao arquitetural Shipment vs Delivery)

## Decisão Arquitetural de Rafael
- **Delivery**: Será tratado como staging/auditoria de importação
- **Shipment**: Será tratado como entidade operacional e fonte de verdade
- **Não vamos unificar entidades agora**
- **Não vamos migrar dados agora**
- **Não vamos alterar telas agora**
- **O próximo passo será especificar tecnicamente como Delivery poderá ser promovido/vinculado a Shipment no futuro**

## Validação de Ambiente
- **Backend pytest**: 105 passed, 1 warning
- **Backend ruff**: All checks passed
- **Frontend npm run lint**: Passou
- **Frontend npm run test**: 58 passed
- **Frontend npm run build**: Sucesso

## Mapeamento Delivery → Shipment

### Tabela de Mapeamento de Campos

| Campo Delivery | Tipo | Campo Shipment | Tipo | Mapeamento | Observação |
|----------------|------|----------------|------|------------|------------|
| nf | String(64) | tracking_code | String(100) | ❌ Não direto | NF não é tracking code |
| transportadora | String(255) | carrier_id | Integer (FK) | ❌ Não direto | Transportadora é nome, carrier_id é FK |
| data_coleta | Date | estimated_delivery | DateTime | ⚠️ Parcial | data_coleta pode ser usada como estimated_delivery |
| valor_frete | Numeric(12, 2) | amount | Numeric(10, 2) | ✅ Direto | valor_frete → amount |
| percentual_frete | Numeric(5, 2) | ❌ Não existe | - | ❌ Sem equivalente | percentual_frete não existe em Shipment |
| created_at | DateTime | created_at | DateTime | ✅ Direto | timestamps podem ser preservados |

### Lacunas de Campos

#### Campos Obrigatórios em Shipment que Não Existem em Delivery
- **tracking_code**: String(100) - obrigatório, único
- **carrier_id**: Integer (FK para carriers.id) - obrigatório
- **status**: String(50) - obrigatório
- **estimated_delivery**: DateTime - obrigatório
- **recipient_name**: String(255) - obrigatório
- **recipient_phone**: String(50) - obrigatório
- **origin_address**: Text - obrigatório
- **destination_address**: Text - obrigatório

#### Campos Obrigatórios em Delivery que Não Existem em Shipment
- **percentual_frete**: Numeric(5, 2) - obrigatório em Delivery, não existe em Shipment

#### Campos Opcionais em Shipment que Não Existem em Delivery
- **actual_delivery**: DateTime
- **invoice_number**: String(50)
- **invoice_key**: String(100)
- **fiscal_document**: String(50)
- **due_date**: DateTime
- **delay_days**: Integer
- **criticality**: String(20)

## Contrato de Promoção Proposto

### Pré-condições para Promoção
1. **Delivery deve existir**: ID válido de Delivery
2. **Carrier deve existir**: Transportadora deve ter correspondência em carriers
3. **Dados mínimos obrigatórios**: Delivery deve ter todos os campos obrigatórios preenchidos
4. **Permissões**: Usuário deve ter permissão de "logistica" ou "admin"
5. **Idempotência**: Não permitir promoção duplicada da mesma Delivery

### Campos Obrigatórios para Promoção
Para promover uma Delivery para Shipment, os seguintes dados devem ser fornecidos manualmente ou via configuração:

1. **tracking_code**: Gerado automaticamente ou fornecido manualmente
2. **carrier_id**: Mapeado a partir de transportadora (requer lookup em carriers)
3. **status**: Valor padrão "pending"
4. **estimated_delivery**: Mapeado a partir de data_coleta
5. **recipient_name**: Obrigatório (não existe em Delivery)
6. **recipient_phone**: Obrigatório (não existe em Delivery)
7. **origin_address**: Obrigatório (não existe em Delivery)
8. **destination_address**: Obrigatório (não existe em Delivery)

### Regra de Idempotência
- **Verificação**: Antes de promover, verificar se já existe Shipment vinculado à Delivery
- **Comportamento**: Se já existir, retornar erro ou o Shipment existente (configurável)
- **Implementação**: Adicionar campo delivery_id em Shipment (requer migration) ou tabela de vínculo

### Comportamento se NF/Tracking Já Existir
- **Verificação**: Verificar se tracking_code já existe em Shipment
- **Comportamento**: Se existir, retornar erro informando conflito
- **Solução**: Permitir geração de tracking_code alternativo ou rejeitar promoção

### Comportamento se Transportadora Não Existir
- **Verificação**: Verificar se transportadora existe em carriers
- **Comportamento**: Se não existir, retornar erro informando carrier não encontrado
- **Solução**: Exigir criação prévia de carrier ou permitir criação automática

### Comportamento se Dados Obrigatórios Estiverem Incompletos
- **Verificação**: Validar todos os campos obrigatórios antes da promoção
- **Comportamento**: Se incompletos, retornar erro listando campos faltantes
- **Solução**: Exigir preenchimento manual ou rejeitar promoção

### Status Inicial do Shipment Criado
- **Status padrão**: "pending"
- **Configurável**: Permitir configuração de status inicial via parâmetro
- **Comportamento**: Após promoção, Shipment entra no ciclo operacional normal

### Relação de Auditoria com ImportHistory/Delivery
- **Preservação**: Delivery original deve ser preservada como auditoria
- **Vínculo**: Shipment deve ter referência à Delivery original
- **Implementação**: Adicionar campo delivery_id em Shipment (requer migration)

### Permissões Exigidas
- **Permissões mínimas**: "logistica" ou "admin"
- **Validação**: Verificar permissões do usuário antes de permitir promoção
- **Comportamento**: Se sem permissão, retornar erro 403

### Tipo de Promoção
- **Manual**: Promoção via endpoint específico (recomendado)
- **Automática**: Promoção automática no importador (não recomendado inicialmente)

## Opções de Implementação

### Opção A — Promoção Manual por Endpoint
**Descrição:**
POST /imports/deliveries/{id}/promote
Cria Shipment a partir de Delivery com dados complementares fornecidos manualmente.

**Payload:**
```json
{
  "tracking_code": "string",
  "recipient_name": "string",
  "recipient_phone": "string",
  "origin_address": "string",
  "destination_address": "string",
  "estimated_delivery": "datetime",
  "status": "pending"
}
```

**Benefícios:**
- Controle manual do processo
- Validação explícita de dados
- Permite correção antes da promoção
- Não altera fluxo existente

**Riscos:**
- Requer esforço manual do usuário
- Pode criar gargalo operacional
- Exige interface adicional

**Necessidade de migration:**
- Opcional (se não adicionar delivery_id em Shipment)

**Testes necessários:**
- Teste de promoção com dados válidos
- Teste de promoção com dados inválidos
- Teste de idempotência
- Teste de permissões
- Teste de carrier não encontrado

**Compatibilidade com PR #1:**
- ✅ Totalmente compatível (não altera código existente)

### Opção B — Promoção Automática no Importador
**Descrição:**
Importação já cria Shipment.
Delivery permanece como auditoria.

**Benefícios:**
- Elimina esforço manual
- Fluxo unificado
- Dados sempre sincronizados

**Riscos:**
- Perda de controle manual
- Pode criar Shipment inválidos
- Difícil corrigir erros de importação
- Complexidade adicional no importador

**Necessidade de migration:**
- Sim (adicionar delivery_id em Shipment)

**Testes necessários:**
- Teste de importação com dados válidos
- Teste de importação com dados inválidos
- Teste de carrier não encontrado
- Teste de dados obrigatórios faltantes
- Teste de rollback em caso de erro

**Compatibilidade com PR #1:**
- ⚠️ Requer alteração em imports/service.py (pode conflitar)

### Opção C — Vínculo Explícito
**Descrição:**
Adicionar shipment_id em Delivery.
Requer migration.
Permite rastreabilidade bidirecional.

**Benefícios:**
- Rastreabilidade completa
- Auditoria preservada
- Permite consultas cruzadas

**Riscos:**
- Requer migration
- Complexidade adicional
- Pode impactar performance

**Necessidade de migration:**
- Sim (adicionar shipment_id em Delivery)

**Testes necessários:**
- Teste de migration
- Teste de vínculo Delivery → Shipment
- Teste de vínculo Shipment → Delivery
- Teste de integridade referencial

**Compatibilidade com PR #1:**
- ⚠️ Requer migration (pode impactar PR #1)

### Opção D — Sem Vínculo Técnico por Enquanto
**Descrição:**
Apenas documentação e separação de telas.
Nenhuma alteração técnica.

**Benefícios:**
- Risco zero
- Não altera código existente
- Permite validação operacional

**Riscos:**
- Não resolve duplicidade
- Continua confusão UX
- Posterga solução

**Necessidade de migration:**
- Não

**Testes necessários:**
- Não

**Compatibilidade com PR #1:**
- ✅ Totalmente compatível

## Recomendação Técnica

### Estratégia Conservadora Recomendada
**LOG-020 apenas especifica.**

**Futuro LOG-021 implementaria endpoint manual de promoção (Opção A).**

**Migration só deve ser feita se Rafael aprovar vínculo explícito (Opção C).**

**Não mudar importador automaticamente antes de validar regra operacional (evitar Opção B).**

### Justificativa
1. **Risco mínimo**: Opção A tem menor risco de quebrar funcionalidades existentes
2. **Controle manual**: Permite validação operacional antes de automação
3. **Compatibilidade**: Totalmente compatível com PR #1
4. **Incremental**: Permite evolução gradual sem grandes mudanças
5. **Validação**: Permite testar fluxo de promoção antes de automação

### Plano Incremental de Implementação
1. **LOG-020**: Especificação técnica (atual)
2. **LOG-021**: Implementação de endpoint manual de promoção (Opção A)
3. **LOG-022**: Testes TDD completos para promoção
4. **LOG-023**: Interface frontend para promoção (se aprovado)
5. **LOG-024**: Migration para vínculo explícito (se aprovado Opção C)
6. **LOG-025**: Validação operacional e ajustes

## Riscos

### Riscos de Migration
- **Downtime**: Migration pode requerer downtime
- **Rollback**: Rollback complexo se migration falhar
- **Performance**: FK pode impactar performance
- **Dados**: Migração de dados existentes pode ser complexa

### Riscos de Implementação
- **Dados incompletos**: Delivery não tem todos os campos obrigatórios de Shipment
- **Carrier não encontrado**: Transportadora pode não existir em carriers
- **Tracking code conflito**: NF pode não ser único como tracking code
- **Perda de dados**: percentual_frete seria perdido na promoção

### Riscos Operacionais
- **Confusão UX**: Usuário pode não entender diferença entre promoção manual e automática
- **Gargalo operacional**: Promoção manual pode criar gargalo
- **Erro humano**: Dados manuais podem conter erros

## Próximos LOGs Sugeridos
1. **LOG-021**: Implementação de endpoint manual de promoção (Opção A)
2. **LOG-022**: Testes TDD completos para promoção
3. **LOG-023**: Interface frontend para promoção (se aprovado)
4. **LOG-024**: Migration para vínculo explícito (se aprovado Opção C)
5. **LOG-025**: Validação operacional e ajustes

## Confirmação de Governança
- ✅ Nenhum código funcional foi alterado
- ✅ Nenhum backend foi alterado
- ✅ Nenhum frontend foi alterado
- ✅ Nenhum teste foi alterado
- ✅ Nenhuma migration foi criada
- ✅ Apenas especificação técnica documental foi criada

## Conclusão
O LOG-020 especificou tecnicamente o vínculo/promoção Delivery → Shipment, identificando lacunas de campos, definindo contrato de promoção e recomendando estratégia conservadora. A implementação deve ser feita incrementalmente, começando por endpoint manual de promoção (Opção A) e evoluindo para vínculo explícito (Opção C) se aprovado pelo supervisor humano.
