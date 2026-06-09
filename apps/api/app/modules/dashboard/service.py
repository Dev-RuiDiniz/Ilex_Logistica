"""Service de dashboard summary para BETA-016A."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.imports.models import ImportHistory
from app.modules.shipments.analytics_service import calculate_carrier_efficiency
from app.modules.shipments.exceptions_service import (
    calculate_exception_priority,
    classify_exception_type,
)
from app.modules.shipments.models import Shipment


def calculate_dashboard_summary(
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
    exception_type: str | None = None,
) -> dict[str, Any]:
    """Calcula resumo do dashboard com KPIs operacionais.

    Reaproveita services existentes:
    - SLA service (BETA-013A)
    - Carrier efficiency (BETA-014A)
    - Exceptions panel (BETA-015A)

    Args:
        db: Database session
        estimated_delivery_from: Data inicial do período
        estimated_delivery_to: Data final do período
        month: Mês para filtro
        year: Ano para filtro
        customer_name: Nome do cliente para filtro
        destination_uf: UF de destino para filtro
        carrier_id: ID da transportadora para filtro
        status: Status para filtro
        criticality: Criticidade para filtro
        sla_status: Status SLA para filtro
        is_late: Se está atrasado para filtro
        exception_type: Tipo de exceção para filtro

    Returns:
        Dicionário com KPIs, top transportadoras e top exceções
    """
    # Build query base
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

    # Calculate SLA for each shipment
    from app.modules.sla.service import calculate_shipment_sla

    sla_results = []
    for shipment in shipments:
        sla_result = calculate_shipment_sla(db, shipment.id)

        # Apply SLA filters
        if sla_status and sla_result.get("sla_status") != sla_status:
            continue
        if is_late is not None and sla_result.get("is_late") != is_late:
            continue

        # Apply exception_type filter
        if exception_type:
            exc_type = classify_exception_type(
                sla_result.get("sla_status"),
                shipment.criticality,
                sla_result.get("is_late"),
            )
            if exc_type != exception_type:
                continue

        sla_results.append({
            "shipment": shipment,
            "sla": sla_result,
        })

    # Calculate KPIs
    total_shipments = len(sla_results)
    on_time_count = sum(1 for r in sla_results if r["sla"].get("sla_status") == "on_time")
    late_count = sum(1 for r in sla_results if r["sla"].get("sla_status") == "late")
    critical_count = sum(1 for r in sla_results if r["sla"].get("sla_status") == "critical")
    warning_count = sum(1 for r in sla_results if r["sla"].get("sla_status") == "warning")
    unknown_sla_count = sum(1 for r in sla_results if r["sla"].get("sla_status") == "unknown")

    # Calculate exceptions (late + critical + warning)
    exceptions_count = late_count + critical_count + warning_count

    # Get import failure count (soma de rejected_count)
    import_failure_result = (
        db.query(ImportHistory)
        .filter(ImportHistory.status == "SUCCESS")
        .first()
    )
    import_failure_count = 0
    if import_failure_result:
        import_failure_count = import_failure_result.rejected_count

    # Active alerts count - módulo não existe, sempre 0
    active_alerts_count = 0

    # Get carriers count
    carriers_count = db.query(Carrier).count()

    # Get top carriers by efficiency (reaproveitar BETA-014A)
    efficiency_result = calculate_carrier_efficiency(
        db,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        month=month,
        year=year,
        customer_name=customer_name,
        destination_uf=destination_uf,
        carrier_id=carrier_id,
        status=status,
        criticality=criticality,
        sla_status=sla_status,
        is_late=is_late,
    )

    # Top 5 carriers by efficiency
    top_carriers_by_efficiency = (
        efficiency_result["carriers"][:5]
        if efficiency_result["carriers"]
        else []
    )

    # Get top exceptions (reaproveitar BETA-015A)
    # Nota: get_exceptions_panel requer relationship carrier que não existe no modelo
    # Vamos implementar uma versão simplificada que busca carrier_name separadamente
    top_exceptions = []
    for sla_result in sla_results:
        shipment = sla_result["shipment"]
        sla = sla_result["sla"]

        exc_type = classify_exception_type(
            sla.get("sla_status"),
            shipment.criticality,
            sla.get("is_late"),
        )

        if exc_type:
            # Buscar carrier name
            carrier = db.query(Carrier).filter(Carrier.id == shipment.carrier_id).first()
            carrier_name = carrier.name if carrier else None

            priority = calculate_exception_priority(
                exc_type,
                sla.get("delay_days", 0),
                shipment.estimated_delivery,
                shipment.id,
            )

            top_exceptions.append({
                "shipment_id": shipment.id,
                "tracking_code": shipment.tracking_code,
                "invoice_number": shipment.invoice_number,
                "carrier_id": shipment.carrier_id,
                "carrier_name": carrier_name,
                "customer_name": shipment.customer_name,
                "destination_uf": shipment.destination_uf,
                "status": shipment.status,
                "sla_status": sla.get("sla_status"),
                "criticality": shipment.criticality,
                "delay_days": sla.get("delay_days", 0),
                "sla_due_date": sla.get("sla_due_date"),
                "exception_type": exc_type,
                "exception_reason": f"{exc_type} - {sla.get('sla_status')}",
                "priority": priority,
                "last_update_at": shipment.updated_at,
            })

    # Ordenar por priority e pegar top 10
    top_exceptions.sort(key=lambda x: x["priority"])
    top_exceptions = top_exceptions[:10]

    # Build response
    return {
        "total_shipments": total_shipments,
        "on_time_count": on_time_count,
        "late_count": late_count,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "unknown_sla_count": unknown_sla_count,
        "resolved_count": 0,  # Campo não existe no modelo
        "no_update_count": 0,  # Campo não existe no modelo
        "exceptions_count": exceptions_count,
        "import_failure_count": import_failure_count,
        "active_alerts_count": active_alerts_count,
        "carriers_count": carriers_count,
        "top_carriers_by_efficiency": top_carriers_by_efficiency,
        "top_exceptions": top_exceptions,
        "generated_at": datetime.now(UTC).isoformat(),
        "filters_applied": {
            "estimated_delivery_from": estimated_delivery_from,
            "estimated_delivery_to": estimated_delivery_to,
            "month": month,
            "year": year,
            "customer_name": customer_name,
            "destination_uf": destination_uf,
            "carrier_id": carrier_id,
            "status": status,
            "criticality": criticality,
            "sla_status": sla_status,
            "is_late": is_late,
            "exception_type": exception_type,
        },
    }
