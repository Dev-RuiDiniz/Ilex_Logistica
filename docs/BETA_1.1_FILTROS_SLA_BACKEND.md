# BETA-1.1: Filtros por Criticidade no Backend

**Status:** Concluído  
**Data:** 2026-06-23  
**Épico:** 1 - SLA, atraso e criticidade

---

## Especificação SDD

### Objetivo
Implementar filtros `sla_status` e `is_late` no endpoint GET /shipments para permitir filtragem de remessas por status de SLA e indicador de atraso.

### Backend

**Endpoint:** GET /shipments com parâmetros de filtro

**Parâmetros de filtro:**
- `sla_status`: enum ['critical', 'warning', 'normal', 'unknown']
- `is_late`: boolean

**Query SQLAlchemy:**
- Filtrar por `sla_status` e `is_late` no modelo Shipment
- Como `sla_status` e `is_late` são calculados dinamicamente (não são colunas no banco), a filtragem é feita em memória após cálculo do SLA
- Limite de 1000 registros para performance

**Validação:**
- Valores inválidos de `sla_status` devem retornar 422 com mensagem clara

**Paginação:**
- Manter paginação existente (page, page_size)
- Paginação aplicada manualmente na lista filtrada quando filtros SLA são usados

**Ordenação:**
- Manter ordenação existente (default: created_at desc)
- Sorting aplicado manualmente na lista filtrada quando filtros SLA são usados

### Critérios de Aceite

- [x] Endpoint aceita filtros `sla_status` e `is_late` individualmente
- [x] Endpoint aceita filtros combinados (sla_status + is_late)
- [x] Valores inválidos retornam erro 422 com mensagem clara
- [x] Filtros funcionam com paginação existente
- [x] Performance: query com filtros executa em <2000ms para 100 registros

---

## Implementação

### Arquivos Modificados

1. **apps/api/app/modules/shipments/router.py**
   - Adicionados parâmetros `sla_status` e `is_late` ao endpoint
   - Adicionada validação de `sla_status` (422 para valores inválidos)
   - Parâmetros passados para função `list_shipments`

2. **apps/api/app/modules/shipments/service.py**
   - Adicionados parâmetros `sla_status` e `is_late` à função `list_shipments`
   - Implementada lógica de filtragem em memória:
     - Busca até 1000 registros
     - Calcula SLA para cada shipment usando `recalculate_shipment_sla`
     - Filtra baseado em `sla_status` e `is_late`
     - Aplica sorting manual
     - Aplica paginação manual

3. **apps/api/tests/test_shipments_sla_filters.py** (novo)
   - 10 testes de backend para validar filtros SLA

### Decisões Arquiteturais

**Filtragem em memória vs banco de dados:**
- `sla_status` e `is_late` são valores calculados dinamicamente pelo serviço SLA
- Não são colunas persistidas no modelo Shipment
- Solução: Filtragem em memória após cálculo do SLA
- Limite de 1000 registros para garantir performance
- Paginação aplicada manualmente na lista filtrada

**Alternativas consideradas:**
- Adicionar colunas `sla_status` e `is_late` ao modelo Shipment (requer migration)
- Usar subquery SQL complexa (difícil de manter)
- Filtragem em memória (escolhida por simplicidade e performance aceitável)

---

## Critérios TDD

### Backend Tests

**Testes implementados:**
1. `test_filtro_sla_status_critical` - Filtrar por sla_status=critical
2. `test_filtro_sla_status_warning` - Filtrar por sla_status=warning
3. `test_filtro_sla_status_normal` - Filtrar por sla_status=normal (on_time)
4. `test_filtro_sla_status_unknown` - Filtrar por sla_status=unknown
5. `test_filtro_is_late_true` - Filtrar por is_late=true
6. `test_filtro_is_late_false` - Filtrar por is_late=false
7. `test_filtro_combinado_sla_status_is_late` - Filtros combinados
8. `test_filtro_sla_status_invalido` - Valor inválido retorna 422
9. `test_filtro_sem_resultados` - Filtro sem resultados retorna empty list
10. `test_performance_100_registros` - Performance <2000ms para 100 registros

**Resultado:** 10/10 testes passando

---

## Limitações Conhecidas

1. **Performance:** Filtragem em memória pode ser lenta para grandes volumes de dados
   - Limite de 1000 registros aplicado
   - Para volumes maiores, considerar persistir `sla_status` e `is_late` no banco

2. **Cálculo de SLA:** Depende de regras SLA configuradas
   - Sem regras SLA, shipments retornam `sla_status=unknown`
   - Requer `collection_departure_date` para cálculo correto

3. **Ordenação:** Quando filtros SLA são usados, sorting é aplicado em memória
   - Pode ser menos eficiente que sorting no banco
   - Aceitável para volumes pequenos/medianos

---

## Como Usar

### Exemplo de Requisição

```bash
# Filtrar por sla_status=critical
GET /api/v1/shipments?sla_status=critical

# Filtrar por is_late=true
GET /api/v1/shipments?is_late=true

# Filtros combinados
GET /api/v1/shipments?sla_status=critical&is_late=true

# Com paginação
GET /api/v1/shipments?sla_status=warning&page=1&page_size=20
```

### Valores Válidos de sla_status

- `critical` - Atraso crítico (acima do threshold crítico)
- `warning` - Atraso moderado (acima do warning threshold)
- `normal` - No prazo (on_time)
- `unknown` - Sem regra SLA ou dados insuficientes

### Resposta de Erro

```json
{
  "detail": "sla_status inválido. Valores válidos: critical, warning, normal, unknown"
}
```

---

## Próximos Passos

1. **Tarefa 1.2:** Implementar filtros SLA no frontend
2. **Tarefa 1.3:** Implementar tela de gestão de regras SLA
3. **Otimização futura:** Considerar persistir `sla_status` e `is_late` no banco para performance em grandes volumes

---

## Validação

**Backend:**
```bash
cd apps/api
python -m pytest tests/test_shipments_sla_filters.py -v
# Resultado: 10 passed
```

**Secret scan:**
```bash
python scripts/check_secrets.py --repo-root . --self-test
# Resultado: OK
```

**Migrations:**
```bash
python scripts/validate_migrations.py
# Resultado: OK
```
