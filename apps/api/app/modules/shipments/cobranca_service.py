"""Rotina de cobrança de remessas atrasadas via WhatsApp (MCP).

Segue o padrão de funções livres que recebem `db: Session` (modules/shipments).
Reutiliza AlertDeliveryLog (channel="whatsapp") para auditoria do envio e
degrada para log interno quando o MCP não está configurado.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.integrations.mcp_whatsapp import McpWhatsAppClient, McpWhatsAppError
from app.modules.alerts.models import AlertDeliveryLog
from app.modules.alerts.service import create_delivery_log
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment

logger = logging.getLogger(__name__)

IDEMPOTENCY_WINDOW_HOURS = 24
TIER_1_MAX_DAYS = 3
TIER_2_MAX_DAYS = 7

TEMPLATES_BY_TIER = {
    1: "cobranca_remessa_aviso",
    2: "cobranca_remessa_formal",
    3: "cobranca_remessa_critical",
}


def escalation_tier(delay_days: int) -> int:
    """Patamar de escalonamento conforme dias de atraso."""
    if delay_days <= TIER_1_MAX_DAYS:
        return 1
    if delay_days <= TIER_2_MAX_DAYS:
        return 2
    return 3


def list_overdue_for_collection(
    db: Session,
    *,
    carrier_id: int | None = None,
    destination_uf: str | None = None,
    dias_min: int = 1,
    dias_max: int = 999,
) -> list[Shipment]:
    """Envios elegíveis para cobrança: não entregues, sem data real e com atraso no intervalo."""
    query = db.query(Shipment).join(Carrier, Shipment.carrier_id == Carrier.id)
    query = query.filter(
        Shipment.actual_delivery.is_(None),
        Shipment.status.notin_(["delivered", "cancelled", "canceled"]),
        Shipment.delay_days >= dias_min,
        Shipment.delay_days <= dias_max,
    )
    if carrier_id is not None:
        query = query.filter(Shipment.carrier_id == carrier_id)
    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf.upper())
    return query.all()


def _is_idempotent(db: Session, shipment_id: int, tier: int) -> bool:
    """True se já houve envio whatsapp/sucesso para o mesmo shipment+tier nas últimas 24h."""
    since = datetime.now(UTC) - timedelta(hours=IDEMPOTENCY_WINDOW_HOURS)
    existing = (
        db.query(AlertDeliveryLog)
        .filter(
            AlertDeliveryLog.channel == "whatsapp",
            AlertDeliveryLog.delivery_status == "success",
            AlertDeliveryLog.source_type == "shipment",
            AlertDeliveryLog.source_id == shipment_id,
            AlertDeliveryLog.created_at >= since,
        )
        .all()
    )
    return any(_log_tier(log) == tier for log in existing)


def _log_tier(log: AlertDeliveryLog) -> int:
    try:
        import json

        meta = json.loads(log.metadata_json or "{}")
        return int(meta.get("tier", 0))
    except (ValueError, TypeError):
        return 0


def _build_message(shipment: Shipment, carrier: Carrier, tier: int) -> str:
    return (
        f"Transportadora {carrier.name}: a remessa {shipment.tracking_code} "
        f"(cliente {shipment.customer_name or shipment.recipient_name}) está atrasada "
        f"há {shipment.delay_days} dias (UF {shipment.destination_uf or 'N/A'})."
    )


def _mark_log(db: Session, log: AlertDeliveryLog, delivery_status: str, error_message: str | None = None) -> None:
    """Atualiza status de entrega e interno do log de cobrança."""
    log.delivery_status = delivery_status
    log.status = "sent" if delivery_status == "success" else "failed"
    log.attempts += 1
    if delivery_status == "success":
        log.sent_at = datetime.now(UTC)
    if error_message:
        log.error_message = error_message
    db.commit()
    db.refresh(log)


def run_cobranca(
    db: Session,
    *,
    carrier_id: int | None = None,
    destination_uf: str | None = None,
    dias_min: int = 1,
    dias_max: int = 999,
    client: McpWhatsAppClient | None = None,
) -> dict:
    """Executa a rotina de cobrança em lote.

    Retorna contadores: enviadas, puladas_sem_whatsapp, falhas, critico_escalonado.
    """
    client = client or McpWhatsAppClient()
    shipments = list_overdue_for_collection(
        db,
        carrier_id=carrier_id,
        destination_uf=destination_uf,
        dias_min=dias_min,
        dias_max=dias_max,
    )
    result = {
        "enviadas": 0,
        "puladas_sem_whatsapp": 0,
        "falhas": 0,
        "critico_escalonado": 0,
    }
    for shipment in shipments:
        carrier = db.get(Carrier, shipment.carrier_id)
        if carrier is None or not carrier.whatsapp:
            result["puladas_sem_whatsapp"] += 1
            continue
        tier = escalation_tier(shipment.delay_days)
        if _is_idempotent(db, shipment.id, tier):
            continue
        message = _build_message(shipment, carrier, tier)
        log = create_delivery_log(
            db,
            alert_id=0,
            channel="whatsapp",
            recipient=carrier.whatsapp,
            message=message,
            subject="cobranca_remessa",
        )
        try:
            client.send_message(
                carrier.whatsapp,
                TEMPLATES_BY_TIER[tier],
                {
                    "tracking_code": shipment.tracking_code,
                    "cliente": shipment.customer_name or shipment.recipient_name,
                    "uf": shipment.destination_uf,
                    "dias_atraso": shipment.delay_days,
                },
            )
            _mark_log(db, log, "success")
            result["enviadas"] += 1
            if tier == 3:
                result["critico_escalonado"] += 1
        except McpWhatsAppError as exc:
            _mark_log(db, log, "failed", error_message=str(exc)[:500])
            result["falhas"] += 1
            if tier == 3:
                result["critico_escalonado"] += 1
            logger.warning("Falha ao enviar cobranca WhatsApp para %s: %s", carrier.whatsapp, exc)
    return result
