from datetime import UTC, datetime

from app.modules.carriers.models import Carrier
from app.modules.dashboard.service import calculate_dashboard_summary
from app.modules.shipments.analytics_service import calculate_carrier_efficiency
from app.modules.shipments.models import Shipment
from app.modules.shipments.service import list_shipments


def test_listagem_dashboard_e_eficiencia_reconciliam_mesmo_universo(db_session):
    carrier = Carrier(name="Transportadora UAT", external_code="UAT-1", integration_metadata={})
    db_session.add(carrier)
    db_session.flush()
    for index, customer in enumerate(("Cliente UAT", "Cliente UAT", "Outro Cliente")):
        db_session.add(Shipment(
            tracking_code=f"UAT-{index}", carrier_id=carrier.id,
            status="lost" if index == 1 else "delivered",
            estimated_delivery=datetime(2026, 7, 10 + index, tzinfo=UTC),
            actual_delivery=datetime(2026, 7, 10 + index, tzinfo=UTC) if index != 1 else None,
            recipient_name=customer, recipient_phone="11999999999",
            origin_address="Origem", destination_address="Destino", meta_data="{}",
            is_active=True, customer_name=customer, destination_uf="SP",
            invoice_number=f"NF-{index}", invoice_value=1000,
            freight_value=100 if index == 0 else None,
        ))
    db_session.commit()
    filters = dict(month=7, year=2026, customer_name="Cliente UAT", destination_uf="SP")

    listing = list_shipments(db_session, page=1, page_size=100, **filters)
    dashboard = calculate_dashboard_summary(db_session, **filters)
    efficiency = calculate_carrier_efficiency(db_session, **filters)

    assert listing["total"] == 2
    assert dashboard["total_shipments"] == listing["total"]
    assert sum(item["total_shipments"] for item in efficiency["carriers"]) == listing["total"]
    assert sum(item["lost_count"] for item in efficiency["carriers"]) == 1
    assert sum(item["total_freight_value"] for item in efficiency["carriers"]) == 100
    assert sum(item["financial_valid_count"] for item in efficiency["carriers"]) == 1
