"""Testes do CobrancaService (TDD RED)."""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

from app.modules.alerts.models import AlertDeliveryLog
from app.modules.carriers.models import Carrier
from app.modules.shipments.cobranca_service import (
    escalation_tier,
    list_overdue_for_collection,
    run_cobranca,
)
from app.modules.shipments.models import Shipment


def _make_shipment(db, *, carrier_id, delay_days, status="in_transit", destination_uf="SP"):
    ship = Shipment(
        tracking_code=f"TRK{delay_days}-{carrier_id}-{int(datetime.now(UTC).timestamp())}",
        carrier_id=carrier_id,
        status=status,
        estimated_delivery=datetime.now(UTC) - timedelta(days=delay_days),
        actual_delivery=None,
        recipient_name="Cliente Teste",
        recipient_phone="+5511999999999",
        origin_address="Origem",
        destination_address="Destino",
        destination_uf=destination_uf,
        customer_name="Cliente Teste",
        delay_days=delay_days,
    )
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return ship


def test_escalation_tier() -> None:
    assert escalation_tier(1) == 1
    assert escalation_tier(3) == 1
    assert escalation_tier(4) == 2
    assert escalation_tier(7) == 2
    assert escalation_tier(8) == 3


def test_list_overdue_for_collection_filters(db_session) -> None:
    carrier = Carrier(name="C1", whatsapp="+5511911111111")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=2)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=10)
    # entregue não deve aparecer
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=5, status="delivered")

    result = list_overdue_for_collection(db_session, dias_min=1, dias_max=999)
    assert len(result) == 2


def test_run_cobranca_happy_path(db_session) -> None:
    carrier = Carrier(name="C2", whatsapp="+5511922222222")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=2)

    fake_client = MagicMock()
    fake_client.send_message.return_value = {"status": "sent"}
    result = run_cobranca(db_session, client=fake_client)

    assert result["enviadas"] == 1
    assert result["puladas_sem_whatsapp"] == 0
    assert result["falhas"] == 0
    fake_client.send_message.assert_called_once()
    log = db_session.query(AlertDeliveryLog).filter(AlertDeliveryLog.channel == "whatsapp").first()
    assert log is not None
    assert log.delivery_status == "success"


def test_run_cobranca_skips_without_whatsapp(db_session) -> None:
    carrier = Carrier(name="C3")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=2)

    fake_client = MagicMock()
    result = run_cobranca(db_session, client=fake_client)

    assert result["puladas_sem_whatsapp"] == 1
    assert result["enviadas"] == 0
    fake_client.send_message.assert_not_called()


def test_run_cobranca_escalation_tier3_critical(db_session) -> None:
    carrier = Carrier(name="C4", whatsapp="+5511944444444")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=10)

    fake_client = MagicMock()
    fake_client.send_message.return_value = {"status": "sent"}
    result = run_cobranca(db_session, client=fake_client)

    assert result["enviadas"] == 1
    assert result["critico_escalonado"] == 1


def test_run_cobranca_idempotent(db_session) -> None:
    carrier = Carrier(name="C5", whatsapp="+5511955555555")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    ship = _make_shipment(db_session, carrier_id=carrier.id, delay_days=2)

    # registra envio anterior bem-sucedido no mesmo patamar
    db_session.add(
        AlertDeliveryLog(
            channel="whatsapp",
            recipient=carrier.whatsapp,
            message="anterior",
            status="sent",
            delivery_status="success",
            source_type="shipment",
            source_id=ship.id,
            metadata_json='{"tier": 1}',
        )
    )
    db_session.commit()

    fake_client = MagicMock()
    result = run_cobranca(db_session, client=fake_client)
    assert result["enviadas"] == 0
    fake_client.send_message.assert_not_called()


def test_run_cobranca_mcp_failure(db_session) -> None:
    carrier = Carrier(name="C6", whatsapp="+5511966666666")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    _make_shipment(db_session, carrier_id=carrier.id, delay_days=10)

    from app.integrations.mcp_whatsapp import McpWhatsAppError

    fake_client = MagicMock()
    fake_client.send_message.side_effect = McpWhatsAppError("boom")
    result = run_cobranca(db_session, client=fake_client)

    assert result["falhas"] == 1
    assert result["critico_escalonado"] == 1
    log = db_session.query(AlertDeliveryLog).filter(AlertDeliveryLog.channel == "whatsapp").first()
    assert log.delivery_status == "failed"
