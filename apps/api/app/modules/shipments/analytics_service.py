from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.sla.service import calculate_shipment_sla


def calculate_carrier_efficiency(
    db: Session,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    month: int | None = None,
    year: int | None = None,
    customer_name: str | None = None,
    destination_uf: str | None = None,
    carrier_id: int | None = None,
    status: str | None = None,
    criticality: str | None = None,
    sla_status: str | None = None,
    is_late: bool | None = None,
) -> dict[str, Any]:
    """Calcula métricas de eficiência por transportadora."""
    # Build query
    query = db.query(Shipment)

    # Apply filters
    if estimated_delivery_from:
        try:
            from_date = datetime.fromisoformat(estimated_delivery_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery >= from_date)
        except (ValueError, AttributeError):
            pass

    if estimated_delivery_to:
        try:
            to_date = datetime.fromisoformat(estimated_delivery_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery <= to_date)
        except (ValueError, AttributeError):
            pass

    if month:
        query = query.filter(extract('month', Shipment.estimated_delivery) == month)

    if year:
        query = query.filter(extract('year', Shipment.estimated_delivery) == year)

    if customer_name:
        query = query.filter(Shipment.customer_name.ilike(f"%{customer_name}%"))

    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf)

    if carrier_id:
        query = query.filter(Shipment.carrier_id == carrier_id)

    if status:
        query = query.filter(Shipment.status == status)

    if criticality:
        query = query.filter(Shipment.criticality == criticality)

    # Get all shipments matching filters
    shipments = query.all()

    # Group by carrier
    carrier_metrics = {}
    for shipment in shipments:
        # Calculate SLA on-demand
        sla_result = calculate_shipment_sla(db, shipment.id)

        # Apply SLA filters
        if sla_status and sla_result.get("sla_status") != sla_status:
            continue
        if is_late is not None and sla_result.get("is_late") != is_late:
            continue

        carrier_id = shipment.carrier_id
        if carrier_id not in carrier_metrics:
            carrier_metrics[carrier_id] = {
                "carrier_id": carrier_id,
                "carrier_name": None,
                "total_invoices": 0,
                "total_shipments": 0,
                "on_time_count": 0,
                "late_count": 0,
                "critical_count": 0,
                "lost_count": 0,
                "total_freight_value": Decimal("0"),
                "total_invoice_value": Decimal("0"),
            }

        carrier_metrics[carrier_id]["total_shipments"] += 1
        if shipment.invoice_number:
            carrier_metrics[carrier_id]["total_invoices"] += 1

        if sla_result.get("sla_status") == "on_time":
            carrier_metrics[carrier_id]["on_time_count"] += 1
        elif sla_result.get("sla_status") in ["late", "critical"]:
            carrier_metrics[carrier_id]["late_count"] += 1

        if shipment.criticality == "alta":
            carrier_metrics[carrier_id]["critical_count"] += 1

        # Extraviadas: status não existe no domínio, sempre 0
        carrier_metrics[carrier_id]["lost_count"] = 0

        if shipment.freight_value:
            carrier_metrics[carrier_id]["total_freight_value"] += Decimal(str(shipment.freight_value))
        if shipment.invoice_value:
            carrier_metrics[carrier_id]["total_invoice_value"] += Decimal(str(shipment.invoice_value))

    # Calculate percentages and averages
    results = []
    for carrier_id, metrics in carrier_metrics.items():
        carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
        if carrier:
            metrics["carrier_name"] = carrier.name

        total = metrics["total_shipments"]
        if total > 0:
            metrics["on_time_percentage"] = (metrics["on_time_count"] / total) * 100
            metrics["late_percentage"] = (metrics["late_count"] / total) * 100
            metrics["lost_percentage"] = (metrics["lost_count"] / total) * 100
        else:
            metrics["on_time_percentage"] = 0
            metrics["late_percentage"] = 0
            metrics["lost_percentage"] = 0

        if metrics["total_invoice_value"] > 0:
            metrics["average_freight_percentage"] = (
                (metrics["total_freight_value"] / metrics["total_invoice_value"]) * 100
            )
        else:
            metrics["average_freight_percentage"] = 0

        if total > 0:
            metrics["average_freight_value"] = metrics["total_freight_value"] / total
        else:
            metrics["average_freight_value"] = 0

        results.append(metrics)

    # Calculate rankings
    results.sort(key=lambda x: x["on_time_percentage"], reverse=True)
    for i, result in enumerate(results):
        result["ranking_by_efficiency"] = i + 1

    results.sort(key=lambda x: x["average_freight_percentage"])
    for i, result in enumerate(results):
        result["ranking_by_cost"] = i + 1

    results.sort(key=lambda x: x["total_shipments"], reverse=True)
    for i, result in enumerate(results):
        result["ranking_by_volume"] = i + 1

    return {
        "carriers": results,
        "generated_at": datetime.now(UTC).isoformat(),
    }
