# SPEC-13 — Integração WhatsApp (MCP) e Rotina de Cobrança de Remessas

**Estado:** Em implementação (TDD em curso)
**Criado em:** 2026-07-03
**Atualizado em:** 2026-07-16
**LOG-IDs:** LOG-042 (integração MCP WhatsApp), LOG-043 (rotina de cobrança)

## Objetivo e contexto

Permitir que a Ilex Logística envie **mensagens WhatsApp** para transportadoras (usando o número `whatsapp` já cadastrado em `carriers`) quando uma **remessa (lote de envios) não foi entregue** dentro do prazo, e executar uma **rotina de cobrança** que escalona lembretes conforme a idade da pendência.

Atualmente o modelo `Shipment` (`modules/shipments/models.py`) já possui `estimated_delivery`, `actual_delivery`, `status`, `delay_days`, `carrier_id` e `recipient_phone`. O modelo `Carrier` já possui `whatsapp`. O `AlertDeliveryLog` (`modules/alerts/models.py`) já registra `channel`/`recipient`/`delivery_status` como `String` livres (não há enum no banco), então **o canal `whatsapp` é suportado sem migration de schema** — basta passar `channel="whatsapp"` em `create_delivery_log`.

## Decisão de arquitetura: usar um MCP server de WhatsApp

Em vez de acoplar a SDK da Meta/Twilio diretamente na API, a integração deve usar um **Model Context Protocol (MCP) server** externo (ex.: servidor que expõe a ferramenta `send_whatsapp_message`), seguindo o padrão do repositório de manter conectores externos desacoplados (ver `AGENTS.md` seção 7.2: *"Conectores externos precisam de timeout, retry controlado, idempotência, observabilidade e sanitização"*).

- A API chama o MCP server via **cliente MCP** (configurado por `ILEX_MCP_WHATSAPP_URL` / `ILEX_MCP_WHATSAPP_TOKEN`).
- O canal `whatsapp` no `AlertDeliveryLog` registra `recipient = <whatsapp da transportadora>`, `channel = "whatsapp"`.
- Nunca se armazena token de API no log; falha de canal não apaga alerta interno (regra já existente em SPEC-09).

## Estado atual e evidências

- `Carrier.whatsapp`: `String(30)`, nullable (cadastrável na tela de transportadoras — já validado no navegador).
- `Shipment`: campos de prazo/entrega/SLA presentes; `delay_days` calculado.
- `AlertDeliveryLog`: `channel`, `recipient`, `delivery_status` — `String` livres; `create_delivery_log(db, alert_id, channel, recipient, message, ...)` aceita qualquer canal (ponto de extensão natural, sem migration).
- `alerts/service.py`: `create_delivery_log` e `update_delivery_log_status` reutilizados para registrar envio WhatsApp e falha.

## Entradas, saídas e fluxo

### 13.1 Envio de mensagem WhatsApp (por envio atrasado)

- *Entrada:* evento de envio com `status != "delivered"` E `actual_delivery IS NULL` E `now() > estimated_delivery + tolerância_SLA`.
- *Saída:* chamada ao MCP `send_whatsapp_message(to=<carrier.whatsapp>, template="cobranca_remessa", vars={tracking, cliente, uf, prazo, dias_atraso})` → `AlertDeliveryLog(channel="whatsapp", recipient=<número>, delivery_status="success"|"failed")`.

### 13.2 Rotina de cobrança (batch)

- *Entrada:* `POST /api/v1/shipments/cobranca/run` (sob demanda) **e** `BackgroundScheduler` recorrente (cron `ILEX_COBRANCA_CRON`, default `0 9 * * *`, habilitado por `ILEX_COBRANCA_SCHEDULER_ENABLED`) com filtro opcional por `carrier_id`, `uf`, `dias_min`, `dias_max`.
- *Regra de escalonamento:*
  - Atraso 1–3 dias → 1ª mensagem (aviso amigável).
  - Atraso 4–7 dias → 2ª mensagem (cobrança formal + prazo de resposta).
  - Atraso > 7 dias → 3ª mensagem (escalonamento p/ gestão + alerta interno `critical`).
- *Idempotência:* não reenvia se já houve `AlertDeliveryLog` `whatsapp`/`success` para aquele `shipment_id` no mesmo "patamar" nas últimas 24h.
- *Saída:* resumo `{ enviadas, puladas_sem_whatsapp, falhas, critico_escalonado }`.

## Regras de negócio e invariantes

- Mensagem **só é enviada se `Carrier.whatsapp` estiver preenchido**; caso contrário, o envio é pulado e contabilizado em `puladas_sem_whatsapp` (não quebra o batch).
- **Sanitização:** números são normalizados para E.164 (`+55...`); template é servidor-side (nunca se monta Markdown livre com dados do envio — evita injeção).
- **Retry controlado:** máx. 3 tentativas com backoff; após esgotamento, `delivery_status="failed"` e alerta interno `critical` (reusa infra de SPEC-09).
- **RBAC:** `POST /cobranca/run` exige `require_permission("shipments:write")` + `require_permission("shipments:read")` (strings de permissão do backend, em `modules/auth/dependencies.py`); o Web usa `canWriteShipments(role)` para exibir o botão.
- **Auditoria:** cada envio WhatsApp gera `AuditLog` (canal, alvo, resultado) — sem dados pessoais além do necessário.
- **Não automatizar captcha** nem contornar portal (AGENTS.md 7.2).

## Contratos (esboço)

```python
# modules/alerts/schemas.py (extensão)
class AlertDeliveryLogCreate(AlertDeliveryLogBase):
    channel: str   # "in_app" | "whatsapp" | "email"
    recipient: str # número E.164 ou "internal"

# modules/shipments/schemas.py (novo)
class CobrancaRunRequest(BaseModel):
    carrier_id: int | None = None
    destination_uf: str | None = None
    dias_min: int = 1
    dias_max: int = 999

class CobrancaRunResult(BaseModel):
    enviadas: int
    puladas_sem_whatsapp: int
    falhas: int
    critico_escalonado: int
```

## Falhas esperadas

| Condição | Comportamento |
|---|---|
| `carrier.whatsapp` nulo | pulado, contabilizado, não interrompe batch |
| MCP indisponível / timeout | retry 3x → `failed`, alerta `critical` interno |
| Resposta não-2xx do MCP | tratado como falha, log rastreável, sem token no log |
| Envio duplicado (mesmo patamar <24h) | idempotente, não reenvia |
| `dias_max` inválido | 422 com mensagem clara |

## Critérios de aceite (verificáveis)

- [ ] `send_whatsapp` via MCP cria `AlertDeliveryLog` com `channel="whatsapp"` e status correto.
- [ ] Rotina pula transportadora sem `whatsapp` e contabiliza em `puladas_sem_whatsapp`.
- [ ] Patamares de escalonamento (1–3 / 4–7 / >7 dias) disparam templates diferentes.
- [ ] Idempotência: não reenvia no mesmo patamar em 24h.
- [ ] Falha de MCP → retry + alerta `critical`, sem perder o alerta interno.
- [ ] RBAC: `viewer`/`auditoria` recebem 403 no `POST /cobranca/run`.
- [ ] Auditoria registra cada tentativa (canal/alvo/resultado).

## Cenários TDD (RED → GREEN → REFACTOR)

1. **Envio feliz:** envio atrasado + carrier com WhatsApp → `AlertDeliveryLog` `whatsapp`/`success`.
2. **Sem WhatsApp:** carrier sem número → pulado + contabilizado.
3. **Escalonamento:** envio com 5 dias → 2ª mensagem; com 10 dias → 3ª + alerta `critical`.
4. **Idempotência:** 2ª chamada no mesmo patamar → 0 envios novos.
5. **MCP falha:** mock do MCP retorna 500 → 3 retries → `failed` + alerta interno.
6. **RBAC:** `viewer` → 403; `gestor` → 200.
7. **Web:** tela de transportadoras mostra `whatsapp`; nova tela/modal "Disparar cobrança" com filtros e resumo.

## Riscos, dependências e rastreabilidade

- **Dependência externa:** MCP server de WhatsApp deve estar configurado (`ILEX_MCP_WHATSAPP_URL`); se ausente, rotina opera em modo "só registro interno" (canal `in_app`).
- **Custo/limite:** templates Meta têm aprovação prévia — usar apenas templates aprovados.
- **LGPD:** mensagem contém dados de envio (rastreio, cliente); minimizar exposição, registrar apenas o necessário na auditoria.
- **Rastreabilidade:** LOG-042 (MCP WhatsApp), LOG-043 (rotina cobrança) → referenciam SPEC-04 (envios), SPEC-09 (alertas/entrega), SPEC-02 (transportadoras).
